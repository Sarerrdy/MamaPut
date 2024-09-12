import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.user import User
from schemas.user_schema import UserSchema

USERS_ENDPOINT = "/api/users"
logger = logging.getLogger(__name__)


class UsersResource(Resource):
    def get(self, id=None):
        """
        UsersResource GET method. Retrieves all users found in the mamaput
        database, unless the id path parameter is provided. If this id
        is provided then the user with the associated id is retrieved.

        :param id: User ID to retrieve, this path parameter is optional
        :return: User, 200 HTTP status code
        """
        if not id:
            logger.info(
                f"Retrieving all users{id}")
            return self._get_all_users(), 200

        logger.info(f"Retrieving user by id {id}")
        try:
            return self._get_user_by_id(id), 200
        except NoResultFound:
            abort(404, message="user not found")

    def _get_user_by_id(self, user_id):
        """retrieve user by id"""
        user = User.query.filter_by(user_id=user_id).first()
        user_json = UserSchema().dump(user)

        if not user_json:
            raise NoResultFound()

        logger.info(f"User retrieved from database {user_json}")
        return user_json

    def _get_all_users(self):
        """retrieve all users"""
        users = User.query.all()

        users_json = [UserSchema().dump(user) for user in users]

        logger.info("Users successfully retrieved.")
        return users_json

    def post(self):
        """
        UsersResource POST method. Adds a new User to the database.

        :return: User.user_id, 201 HTTP status code.
        """
        user = UserSchema().load(request.get_json())

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this users are already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return user.user_id, 201
