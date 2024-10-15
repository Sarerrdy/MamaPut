import logging
from datetime import datetime
import time

from flask import request, jsonify, g
from flask_restful import Resource, current_app, abort
# from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.user import User
from models.address import Address
# from schemas.user_schema import UserSchema
# from schemas.login_schema import LoginSchema
from schemas.user_rel_schemas import UserSchema, AddressSchema


from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
import jwt


USERS_ENDPOINT = "/api/users"
logger = logging.getLogger(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        g.user = user
        return user
    return None


def verify_auth_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])
        logger.info(f"DATA: {data}")
        logger.info(f"DATA_USER.ID: {data['sub']}")
    except:
        return
    return User.query.filter_by(email=data['sub']).first()
    # User.query.filter_by(email=email).first()


def generate_auth_token(self, expires_in=60):
    logger.info(f"USER_ID: {g.user.user_id}")
    return jwt.encode(
        {'sub': g.user.email, 'exp': time.time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256')


class UsersResource(Resource):
    def post(self):
        """
        UsersResource POST method. Adds a new User to the database.

        :return: User.user_id, 201 HTTP status code.
        """
        user_data = request.get_json()

        if request.endpoint == "login":
            return self.login_with_username()
        elif request.endpoint == "token":
            token = user_data['token']
            return self.login_with_token(token)
        elif request.endpoint == "register":
            return self.register()

    def register(self):
        try:
            req = request.get_json()
            data = req["user"]
            email = data['email']
            password = data['password']
            user = User(
                title=data['title'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                gender=data['gender'],
                email=email,
                password=generate_password_hash(password),
                phone=data['phone'],
                join_date=datetime.now(),
                user_url=data['user_url']
            )
            if email is None or password is None:
                # missing arguments
                abort(400, "missing username or password")
            if User.query.filter_by(email=email).first() is not None:
                abort(400, "user already exist")    # existing user
            user_json = UserSchema().dump(user)
            user_json = UserSchema().load(user_json)
            db.session.add(user_json)
            db.session.commit()

            address = Address(
                address=data['address'],
                town=data['town'],
                state=data['state'],
                lga=data['lga'],
                landmark=data['landmark'],
                user_id=user_json.user_id
            )
            address_json = AddressSchema().dump(address)
            address_json = AddressSchema().load(address_json)
            db.session.add(address_json)
            db.session.commit()

            return user.email, 201
        except IntegrityError as e:
            abort(500, message="Unexpected Error: {e}!")

    # Attempt login with email and password

    def login_with_username(self):
        logger.info("LOGIN CALLED")

        req = request.get_json()
        data = req["user"]
        logger.info(f"DATA: {data}")
        email = data['username']
        password = data['password']

        logger.info(
            f"User retrieved from database by email: {email}")
        verified_user = verify_password(email, password)
        token = generate_auth_token(300)
        address = Address.query.filter_by(
            user_id=verified_user.user_id).first()
        address_json = AddressSchema().dump(address)
        user_json = UserSchema().dump(verified_user)

        if not verified_user or not token or not address:
            raise NoResultFound()
        logger.info(f"User retrieved from database {address_json}")
        logger.info(f"Token retrieved from database {token}")
        return [token, user_json, address_json], 200
        # return jsonify({"token": token, "user": user_json, "address": address_json}), 200

    # Attempt login with token
    def login_with_token(self, token):
        logger.info(f"ENTER LOGIN_WITH_TOKEN_FUNCTION")
        if token is not None:
            logger.info(f"TOKEN NOT NON")
            verified_token = verify_auth_token(token)
            # logger.info(f"TOKEN VERIFIED: {verified_token}")
            if verified_token is not None:
                logger.info(f"TOKEN VERIFIED-1: {verified_token}")
                return True
            else:
                logger.info(f"NON-TOKEN-2: {verified_token}")
                return False
        logger.info(f"NON-TOKEN-3")
        return False
