import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.review import Review
from schemas.review_schema import ReviewSchema

REVIEW_ENDPOINT = "/api/review"
logger = logging.getLogger(__name__)


class ReviewsResource(Resource):
    def get(self, id=None):
        """
        ReviewsResource GET method. Retrieves all reviews found in the
        mamaput database. If this id is provided then the review with the
        associated review_id is retrieved.

        :param id: review ID to retrieve, this path parameter is optional
        :return: review, 200 HTTP status code
        """
        if not id:
            user_id = request.args.get("user_id")
            logger.info(
                f"Retrieving all reviews, optionally filtered by "
                f"user_id={user_id}"
            )

            return self._get_all_reviews(user_id), 200

        logger.info(f"Retrieving reviews by id {id}")

        try:
            return self._get_review_by_id(id), 200
        except NoResultFound:
            abort(404, message="review not found")

    def _get_review_by_id(self, review_id):
        """retrieve review by review id"""
        review = Review.query.filter_by(review_id=review_id).first()
        review_json = ReviewSchema().dump(review)

        if not review_json:
            raise NoResultFound()

        logger.info(f"Review retrieved from database {review_json}")
        return review_json

    def _get_all_reviews(self, user_id):
        """retrieve all reviews"""
        if user_id:
            reviews = Review.query.filter_by(user_id=user_id).all()
        else:
            reviews = Review.query.all()
        reviews_json = [ReviewSchema().dump(review) for review in reviews]

        logger.info("Review successfully retrieved.")
        return reviews_json

    def post(self):
        """
        ReviewsResource POST method. Adds a new review to the database.

        :return: Review.rewiew_id, 201 HTTP status code.
        """
        review = ReviewSchema().load(request.get_json())

        try:
            db.session.add(review)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this review is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return review.review_id, 201
