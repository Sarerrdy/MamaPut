import logging

from flask import request, jsonify
from flask_restful import Resource
# from flask_restful import Resource, abort
# from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

# from database import db
from models.user import User
from schemas.user_schema import UserSchema
# from schemas.login_schema import LoginSchema


from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token


USERS_ENDPOINT = "/api/users"
logger = logging.getLogger(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


class UsersResource(Resource):
    def post(self):
        """
        UsersResource POST method. Adds a new User to the database.

        :return: User.user_id, 201 HTTP status code.
        """

        user_data = request.get_json()
        # login_schema = LoginSchema().load(user_data)
        # user = login_schema.load(user_data)
        email = user_data['email']
        password = user_data['password']

        token = create_access_token(identity=email)

        logger.info(
            f"User retrieved from database by email: {email} and password: {password}")
        verified_user = verify_password(email, password)
        user_json = UserSchema().dump(verified_user)

        if not verified_user:
            raise NoResultFound()
        logger.info(f"User retrieved from database {user_json}")
        logger.info(f"Token retrieved from database {token}")
        return [token, user_json], 200
        # resp = [token, user]
        # return (resp), 200


# class UsersResource(Resource):

    # @auth.login_required
    # def get(self, id=None):
    #     """
    #     UsersResource GET method. Retrieves all users found in the mamaput
    #     database, unless the id path parameter is provided. If this id
    #     is provided then the user with the associated id is retrieved.

    #     :param id: User ID to retrieve, this path parameter is optional
    #     :return: User, 200 HTTP status code
    #     """
    #     if not id:
    #         logger.info(
    #             f"Retrieving all users{id}")
    #         return self._get_all_users(), 200

    #     logger.info(f"Retrieving user by id {id}")
    #     try:
    #         return self._get_user_by_id(id), 200
    #     except NoResultFound:
    #         abort(404, message="user not found")

    # def _get_user_by_id(self, user_id):
    #     """retrieve user by id"""
    #     user = User.query.filter_by(user_id=user_id).first()
    #     user_json = UserSchema().dump(user)

    #     if not user_json:
    #         raise NoResultFound()

    #     logger.info(f"User retrieved from database {user_json}")
    #     return user_json

    # def _get_all_users(self):
    #     """retrieve all users"""
    #     users = User.query.all()

    #     users_json = [UserSchema().dump(user) for user in users]

    #     logger.info("Users successfully retrieved.")
    #     return users_json

    # def post(self):
    #     """
    #     UsersResource POST method. Adds a new User to the database.

    #     :return: User.user_id, 201 HTTP status code.
    #     """
    #     user_data = request.get_json()
    #     user_schema = UserSchema()
    #     user = user_schema.load(user_data)

    #     user['password'] = generate_password_hash(user['password'])

    #     # new_user = User(user_id=user['user_id'], password=user['password'])

    #     try:
    #         db.session.add(user)
    #         db.session.commit()
    #     except IntegrityError as e:
    #         logger.warning(
    #             f"Integrity Error, this user is already in the database. "
    #             f"Error: {e}"
    #         )
    #         abort(500, message="Unexpected Error!")
    #     else:
    #         return user.user_id, 201
