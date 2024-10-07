import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.category import Category
from schemas.category_schema import CategorySchema

CATEGORIES_ENDPOINT = "/api/categories"
logger = logging.getLogger(__name__)


class CategoriesResource(Resource):
    def get(self, id=None):
        """
        UsersResource GET method. Retrieves all categories found in the mamaput
        database, unless the id path parameter is provided. If this id
        is provided then the category with the associated id is retrieved.

        :param id: category ID to retrieve, this path parameter is optional
        :return: User, 200 HTTP status code
        """
        if not id:
            logger.info(
                f"Retrieving all categories{id}")
            return self._get_all_categories(), 200

        logger.info(f"Retrieving category by id {id}")
        try:
            return self._get_category_by_id(id), 200
        except NoResultFound:
            abort(404, message="category not found")

    def _get_category_by_id(self, category_id):
        """retrieve category by id"""
        category = Category.query.filter_by(category_id=category_id).first()
        category_json = CategorySchema().dump(category)

        if not category_json:
            raise NoResultFound()

        logger.info(f"Category retrieved from database {category_json}")
        return category_json

    def _get_all_categories(self):
        """retrieve all categories"""
        categories = Category.query.all()

        categories_json = [
            CategorySchema().dump(category) for category in categories]

        logger.info("categories successfully retrieved.")
        return categories_json

    def post(self):
        """
        CategoriesResource POST method. Adds a new Category to the database.

        :return: Category.category_id, 201 HTTP status code.
        """
        category = CategorySchema().load(request.get_json())

        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this category is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return category.category_id, 201
