import logging
from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from database import db
from models.review import Review

RATING_ENDPOINT = "/api/rating"
logger = logging.getLogger(__name__)


class RatingsResource(Resource):
    def get(self, menu_id):
        """ Retrieves the average rating for a menu item """
        if not menu_id:
            logger.error("Menu ID is required to retrieve the average rating")
            abort(400, message="Menu ID is required")

        logger.info(f"Retrieving average rating for menu ID {menu_id}")
        try:
            return self._get_average_rating(menu_id), 200
        except NoResultFound:
            abort(404, message="Menu item not found")
        except Exception as e:
            logger.error(f"Error retrieving average rating: {e}")
            return jsonify({"error": str(e)}), 500

    def _get_average_rating(self, menu_id):
        reviews = Review.query.filter_by(menu_id=menu_id).all()
        if not reviews:
            return {"average_rating": 0, "review_count": 0}
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / len(reviews)
        review_count = len(reviews)
        logger.info(f"Average rating retrieved from database {average_rating}")
        return {"average_rating": average_rating, "review_count": review_count}
