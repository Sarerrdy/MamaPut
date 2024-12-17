import logging
from datetime import datetime
import time

from flask import request, g
from flask_restful import Resource, current_app, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.role import Role
from models.user_role import UserRole
from models.user import User
from models.address import Address
from schemas.user_rel_schemas import UserSchema, AddressSchema
from schemas.role_schema import RoleSchema


from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_jwt_extended import create_access_token
import jwt


USERS_ENDPOINT = "/api/users"
logger = logging.getLogger(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        g.user = user
        print(f"myUSER: {user}")
        return user
    return None


def verify_auth_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])
    except:
        return
    return User.query.filter_by(email=data['sub']).first()
    # User.query.filter_by(email=email).first()

# stay login for 14 days


def generate_auth_token(self, expires_in=1209600):
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

    def put(self, id):
        """
        UsersResource PUT method. Updates existing user in the database.
        :param user_id: ID of the user to be updated.
        :return: Updated user data and HTTP status code.
        """

        try:

            json_data = request.get_json(force=True)
            if not json_data:
                return ("No input data provided")

            if 'currentPassword' not in json_data:
                # Validate and deserialize input
                try:

                    data = UserSchema().load(json_data)
                except ValidationError as err:
                    return err.messages, 422

                # Find existing user
                user = User.query.filter_by(user_id=id).first()
                if not user:
                    return {"message": "User not found!"}, 400
                user.phone = data.phone

                db.session.commit()

                result = UserSchema().dump(user)

                return {'message': "phone update was successful", 'data': result['phone']}, 200
            else:
                return self.changepassword(id, json_data)
        except Exception as e:
            return {"error": str(e)}, 400

    # Add user role assignment in the register method
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
                user_url=""
            )
            if email is None or password is None:
                abort(400, "missing username or password")
            if User.query.filter_by(email=email).first() is not None:
                abort(400, "user already exist")

            # user_json = UserSchema().dump(user)
            # user_json = UserSchema().load(user_json)
            db.session.add(user)
            db.session.commit()

            # Assign default role (User) to the new user
            default_role = Role.query.filter_by(role_name='User').first()
            user_role = UserRole(user_id=user.user_id,
                                 role_id=default_role.role_id)
            # user_role.save()
            db.session.add(user_role)

            address = Address(
                address=data['address'],
                town=data['town'],
                state=data['state'],
                lga=data['lga'],
                landmark=data['landmark'],
                user_id=user.user_id
            )
            address_json = AddressSchema().dump(address)
            address_json = AddressSchema().load(address_json)
            db.session.add(address_json)
            db.session.commit()

            # user_json = UserSchema().dump(user)

            return user.email, 201
        except IntegrityError as e:
            abort(500, message=f"Unexpected Error: {e}!")

    # Method to assign roles (only accessible by Admin)
    def assign_role(self, user_id, role_name):
        admin_email = 'mamaputwebapp@gmail.com'
        admin_user = User.query.filter_by(email=admin_email).first()

        if not admin_user:
            return {"message": "Admin user not found!"}, 400

        if g.user.email != admin_email:
            return {"message": "Only admin can assign roles!"}, 403

        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": "User not found!"}, 400

        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            return {"message": "Role not found!"}, 400

        user_role = UserRole(user_id=user.user_id, role_id=role.role_id)
        user_role.save()

        return {"message": "Role assigned successfully!"}, 200

    def changepassword(self, id, json_data):
        """Change password"""

        try:
            email = json_data['email']
            currentPassword = json_data['currentPassword']
            newPassword = json_data['newPassword']

            verified_user = verify_password(
                email, currentPassword)
            if verified_user is None:
                return {"message": "Current password is not correct!"}, 400

            else:
                # Find existing user
                user = User.query.filter_by(user_id=id).first()
                user.password = generate_password_hash(
                    newPassword)
                print(f"CALL USER: {user}")
                db.session.commit()

                return {'message': "Password change was successful"}, 200

        except Exception as e:
            return {"error": str(e)}, 400

    # Attempt login with email and password

    def login_with_username(self):

        req = request.get_json()
        data = req["user"]

        email = data['username']
        password = data['password']

        logger.info("User retrieved from database by email")
        verified_user = verify_password(email, password)
        token = generate_auth_token(1209600)  # 14 days
        address = Address.query.filter_by(
            user_id=verified_user.user_id).first()
        address_json = AddressSchema().dump(address)
        user_json = UserSchema().dump(verified_user)

        if not verified_user or not token or not address:
            raise NoResultFound()
        return [token, user_json, address_json], 200
        # return jsonify({"token": token, "user": user_json, "address": address_json}), 200

    # Attempt login with token
    def login_with_token(self, token):

        if token is not None:
            verified_token = verify_auth_token(token)
            if verified_token is not None:
                return True
            else:
                return False
        return False
