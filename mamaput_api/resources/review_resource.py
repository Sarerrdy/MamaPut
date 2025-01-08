import logging
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from models.review import Review
from database import db
from schemas.review_schema import ReviewSchema

REVIEW_ENDPOINT = '/api/reviews'
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ReviewsResource(Resource):
    def get(self, menu_id):
        reviews = Review.query.filter_by(menu_id=menu_id).all()
        if not reviews:
            return [], 200
        return reviews_schema.dump(reviews), 200

    def post(self, menu_id):
        logger.info("POST request received for menu_id: %s", menu_id)
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            logger.error("User ID is missing in the request")
            abort(400, message="User ID is required")
        logger.debug("User ID from request: %s", user_id)
        existing_review = Review.query.filter_by(
            menu_id=menu_id, user_id=user_id).first()
        if existing_review:
            logger.warning(
                "User %s has already reviewed menu item %s", user_id, menu_id)
            return {'message': 'User has already reviewed this item'}, 400
        try:
            review_data = review_schema.load(data)
            logger.debug("Review data loaded: %s", review_data)
        except ValidationError as err:
            logger.error("Validation error: %s", err.messages)
            return err.messages, 400
        review = Review(**review_data)
        db.session.add(review)
        try:
            db.session.commit()
            logger.info(
                "Review created successfully for user %s and menu item %s", user_id, menu_id)
        except Exception as e:
            logger.error("Error committing to the database: %s", e)
            db.session.rollback()
            return {'message': 'Internal server error'}, 500
        return review_schema.dump(review), 201

    def put(self, menu_id):
        """
        ReviewsResource PUT method. Updates a review in the database.

        :param menu_id: ID of the menu item to update the review for.
        :return: Updated review JSON, 200 HTTP status code if successful,
        404 if not found.
        """
        logger.info("PUT request received for menu_id: %s", menu_id)
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            logger.error("User ID is missing in the request")
            abort(400, message="User ID is required")
        logger.debug("User ID from request: %s", user_id)
        review = Review.query.filter_by(
            menu_id=menu_id, user_id=user_id).first()
        if not review:
            logger.warning(
                "Review not found for user %s and menu item %s", user_id, menu_id)
            abort(404, message="Review not found")
        try:
            review_data = review_schema.load(data, partial=True)
            logger.debug("Review data loaded for update: %s", review_data)
        except ValidationError as err:
            logger.error("Validation error: %s", err.messages)
            abort(400, message=err.messages)
        review.rating = review_data.get('rating', review.rating)
        review.review = review_data.get('review', review.review)
        review.created_at = review_data.get('created_at', review.created_at)
        try:
            db.session.commit()
            logger.info(
                "Review updated successfully for user %s and menu item %s", user_id, menu_id)
        except IntegrityError as e:
            logger.warning(
                "Integrity Error, could not update review. Error: %s", e)
            abort(500, message="Unexpected Error!")
        return review_schema.dump(review), 200

    def delete(self, menu_id):
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            logger.error("User ID is missing in the request")
            abort(400, message="User ID is required")
        logger.debug("User ID from request: %s", user_id)
        review = Review.query.filter_by(
            menu_id=menu_id, user_id=user_id).first()
        if not review:
            return {'message': 'Review not found'}, 404
        db.session.delete(review)
        try:
            db.session.commit()
            logger.info(
                "Review deleted successfully for user %s and menu item %s", user_id, menu_id)
        except Exception as e:
            logger.error("Error committing to the database: %s", e)
            db.session.rollback()
            return {'message': 'Internal server error'}, 500
        return {'message': 'Review deleted'}, 200
