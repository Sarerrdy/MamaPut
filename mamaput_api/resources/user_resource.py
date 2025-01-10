import logging
import time
import json
from datetime import datetime

from flask import request, g
from flask_restful import Resource, current_app
from flask_httpauth import HTTPBasicAuth
from itsdangerous import URLSafeTimedSerializer
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from mailer import send_password_reset_email, send_registration_confirmation
from database import db
from models.role import Role
from models.user_role import UserRole
from models.user import User
from models.address import Address
from schemas.user_Address_schemas import UserSchema, AddressSchema


USERS_ENDPOINT = "/api/users"
logger = logging.getLogger(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            g.user = user
            logger.info(f"User verified successfully: {email}")
            return user
        logger.error(f"Invalid email or password for user: {email}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during password verification: {e}")
        return None


def verify_auth_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return None

    return User.query.filter_by(email=data['sub']).first()


def generate_auth_token(self, expires_in=1209600):
    return jwt.encode(
        {'sub': g.user.email, 'exp': time.time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256')


def format_validation_errors(errors):
    formatted_errors = []
    for field, messages in errors.items():
        for message in messages:
            formatted_errors.append(f"{field}: {message}")
    return formatted_errors


class UsersResource(Resource):
    def get(self, id=None):
        """
        UsersResource GET method. Retrieves user(s) from the database.
        :param id: ID of the user to be retrieved.
        :return: User data or list of users and HTTP status code.
        """
        try:
            if id is None:
                return self.get_all_users()
            return self.get_user_roles(id)
        except Exception as e:
            logger.error(f"Unexpected error during GET request: {e}")
            return {"error": str(e)}, 500

    def get_all_users(self):
        """
        Retrieve all users from the database.
        :return: List of users or an error message.
        """
        try:
            users = User.query.all()
            if not users:
                logger.error("No users found")
                return {"message": "No users found"}, 404

            user_schema = UserSchema(many=True)
            users_data = user_schema.dump(users)
            logger.info("Users retrieved successfully")
            return users_data, 200
        except Exception as e:
            logger.error(f"Error retrieving users: {e}")
            return {"error": str(e)}, 500

    def post(self):
        """
        UsersResource POST method. Adds a new User to the database.

        :return: User.user_id, 201 HTTP status code.
        """
        try:
            user_data = request.get_json()
            if not user_data:
                logger.error("No input data provided")
                return {"message": "No input data provided"}, 400

            if request.endpoint == "login":
                return self.login_with_username()
            elif request.endpoint == "token":
                token = user_data.get('token')
                if not token:
                    logger.error("Token not provided")
                    return {"message": "Token is required"}, 400
                return self.login_with_token(token)
            elif request.endpoint == "register":
                return self.register()
            elif request.endpoint == "forgot_password":
                return self.forgot_password()
            elif request.endpoint == "reset_password":
                return self.reset_password()
            else:
                logger.error("Invalid endpoint")
                return {"message": "Invalid endpoint"}, 400
        except Exception as e:
            logger.error(f"Unexpected error during POST request: {e}")
            return {"error": str(e)}, 500

    def put(self):
        """
        UsersResource PUT method. Updates existing user in the database.
        :param user_id: ID of the user to be updated.
        :return: Updated user data and HTTP status code.
        """
        try:
            json_data = request.get_json(force=True)

            if not json_data:
                logger.error("No input data provided")
                return {"message": "No input data provided"}, 400

            if request.endpoint == "assign_role":
                user_id = json_data['userId']
                role_name = json_data['roleName']
                return self.assign_role(user_id, role_name)

            if request.endpoint == "remove_role":
                user_id = json_data['userId']
                role_name = json_data['roleName']
                return self.remove_role(user_id, role_name)

            if 'currentPassword' not in json_data:
                try:
                    data = UserSchema().load(json_data)
                except ValidationError as err:
                    logger.error(f"Validation error: {err.messages}")
                    return err.messages, 422

                user = User.query.filter_by(user_id=id).first()
                if not user:
                    logger.error(f"User with id {id} not found")
                    return {"message": "User not found!"}, 400

                user.phone = data.phone
                db.session.commit()

                result = UserSchema().dump(user)
                logger.info(f"Phone update was successful for user_id: {id}")
                return {'message': "Phone update was successful",
                        'data': result['phone']}, 200
            else:
                return self.changepassword(id, json_data)
        except Exception as e:
            logger.error(f"Unexpected error during user update: {e}")
            return {"error": str(e)}, 500

    def register(self):
        try:
            req = request.get_json()
            if not req:
                logger.error("No input data provided")
                return {"message": "No input data provided"}, 400

            logger.debug(f"Received request data: {req}")

            data = req.get("user", {})
            if not data:
                logger.error("User data not provided")
                return {"message": "User data not provided"}, 400

            logger.debug(f"User data: {data}")

            # Validate input data
            try:
                logger.debug("Validating user data")
                validated_data = UserSchema().load(data)
                logger.debug(f"Validated user data: {validated_data}")
            except ValidationError as err:
                formatted_errors = format_validation_errors(err.messages)
                logger.error(f"Validation error: {formatted_errors}")
                return {"errors": formatted_errors}, 422

            logger.debug("User data validated successfully")
            email = validated_data.email
            password = validated_data.password
            logger.debug(f"Email: {email}, Password: {password}")

            if User.query.filter_by(email=email).first() is not None:
                logger.error(f"User with email {email} already exists")
                return {"message": "User already exists"}, 400

            user = User(
                title=validated_data.title,
                first_name=validated_data.first_name,
                last_name=validated_data.last_name,
                gender=validated_data.gender,
                email=email,
                password=generate_password_hash(password),
                phone=validated_data.phone,
                join_date=datetime.now(),
                user_url=""
            )

            logger.debug(f"Created user object: {user}")

            db.session.add(user)
            db.session.commit()

            logger.debug(f"User added to database: {user}")

            # Assign default role (User) to the new user
            default_role = Role.query.filter_by(role_name='User').first()
            if not default_role:
                logger.error("Default role 'User' not found")
                return {"message": "Default role 'User' not found"}, 500

            user_role = UserRole(user_id=user.user_id,
                                 role_id=default_role.role_id)
            db.session.add(user_role)

            logger.debug(f"Assigned default role to user: {user_role}")

            # Extract address-related fields from the validated data
            address_data = {
                'address': data.get('address'),
                'town': data.get('town'),
                'state': data.get('state'),
                'lga': data.get('lga'),
                'landmark': data.get('landmark'),
                'user_id': user.user_id
            }

            address = Address(**address_data)

            logger.debug(f"Created address object: {address}")

            try:
                address_json = AddressSchema().dump(address)
                logger.debug(f"Dumped address data: {address_json}")
                address_json = AddressSchema().load(address_json)
                logger.debug(f"Validated address data: {address_json}")
            except ValidationError as err:
                formatted_errors = format_validation_errors(err.messages)
                logger.error(f"Address validation error: {formatted_errors}")
                return {"errors": formatted_errors}, 422
            except Exception as e:
                logger.error(
                    f"Unexpected error during address processing: {e}")
                return {"message": f"Unexpected Error: {e}!"}, 500

            db.session.add(address_json)
            db.session.commit()

            # Send confirmation email
            try:
                send_registration_confirmation(user.email, user.first_name)
                logger.debug(f"Confirmation email sent to: {user.email}")
            except Exception as e:
                logger.error(f"Error sending confirmation email: {e}")
                return {"message": f"Error sending confirmation email: {e}"}, 500

            logger.info(f"User registered successfully with email: {email}")
            return {"email": user.email}, 201
        except IntegrityError as e:
            logger.error(f"Integrity error during registration: {e}")
            return {"message": f"Unexpected Error: {e}!"}, 500
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}")
            return {"message": f"Unexpected Error: {e}!"}, 500

    # Add user role assignment in the register method

    def assign_role(self, user_id, role_name):
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                logger.error(f"User with id {user_id} not found")
                return {"message": "User not found!"}, 400

            role = Role.query.filter_by(role_name=role_name).first()
            if not role:
                logger.error(f"Role with name {role_name} not found")
                return {"message": "Role not found!"}, 400

            user_role = UserRole(user_id=user.user_id, role_id=role.role_id)
            db.session.add(user_role)
            db.session.commit()

            logger.info(f"Role {role_name} assigned successfully to user_id: "
                        f"{user_id}")
            return {"message": "Role assigned successfully!"}, 200
        except Exception as e:
            logger.error(f"Unexpected error during role assignment: {e}")
            return {"error": str(e)}, 500

    def remove_role(self, user_id, role_name):
        try:
            if role_name == 'User':
                logger.error("Default 'User' role cannot be removed")
                return {"message": "Default 'User' role cannot be removed"}, 400

            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                logger.error(f"User with id {user_id} not found")
                return {"message": "User not found!"}, 400

            role = Role.query.filter_by(role_name=role_name).first()
            if not role:
                logger.error(f"Role with name {role_name} not found")
                return {"message": "Role not found!"}, 400

            user_role = UserRole.query.filter_by(
                user_id=user.user_id, role_id=role.role_id).first()
            if user_role:
                db.session.delete(user_role)
                db.session.commit()
                logger.info(f"Role {role_name} removed successfully for user_id: "
                            f"{user_id}")
                return {"message": "Role removed successfully!"}, 200

            logger.error(
                f"Role {role_name} not assigned to user_id: {user_id}")
            return {"message": "Role not assigned to user"}, 404
        except Exception as e:
            logger.error(f"Unexpected error during role removal: {e}")
            return {"error": str(e)}, 500

    def get_user_roles(self, user_id):
        """
        Get the roles of a user by their user_id.
        :param user_id: ID of the user.
        :return: List of roles of the user or an error message.
        """
        try:
            user_roles = UserRole.query.filter_by(user_id=user_id).all()
            if not user_roles:
                logger.error(f"User roles not found for user_id: {user_id}")
                return {"message": "User roles not found!"}, 404

            roles = []
            for user_role in user_roles:
                role = Role.query.filter_by(role_id=user_role.role_id).first()
                if role:
                    roles.append(role.role_name)  # Add role name to the list

            if not roles:
                logger.error(f"Roles not found for user_id: {user_id}")
                return {"message": "Roles not found!"}, 404

            logger.info(f"Roles retrieved successfully for user_id: {user_id}")
            return json.dumps(roles)

        except Exception as e:
            logger.error(f"Unexpected error retrieving user roles: {e}")
            return {"error": str(e)}, 500

    def changepassword(self, id, json_data):
        """Change password"""

        try:
            email = json_data['email']
            current_password = json_data['currentPassword']
            new_password = json_data['newPassword']

            if not email or not current_password or not new_password:
                logger.error(
                    "Email, current password, and new password are required")
                return {"message": "Email, current password, and new password are required"}, 400

            verified_user = verify_password(email, current_password)
            if verified_user is None:
                logger.error("Current password is not correct")
                return {"message": "Current password is not correct!"}, 400

            user = User.query.filter_by(user_id=id).first()
            if not user:
                logger.error(f"User with id {id} not found")
                return {"message": "User not found!"}, 404

            user.password = generate_password_hash(new_password)
            db.session.commit()

            logger.info(f"Password change was successful for user: {email}")
            return {'message': "Password change was successful"}, 200

        except Exception as e:
            logger.error(f"Unexpected error during password change: {e}")
            return {"error": str(e)}, 500

    # Attempt login with email and password

    def login_with_username(self):
        try:
            req = request.get_json()
            data = req.get("user", {})

            email = data.get('username')
            password = data.get('password')

            if not email or not password:
                logger.error("Email or password not provided")
                return {"message": "Email and password are required"}, 400

            logger.info(f"Attempting to retrieve user by email: {email}")
            verified_user = verify_password(email, password)
            if not verified_user:
                logger.error("Invalid email or password")
                return {"message": "Invalid email or password"}, 401

            logger.info(
                f"Generating auth token for user: {verified_user.email}")
            token = generate_auth_token(1209600)  # 14 days

            logger.info(
                f"Retrieving address for user: {verified_user.user_id}")
            address = Address.query.filter_by(
                user_id=verified_user.user_id).first()
            if not address:
                logger.error("Address not found for user")
                return {"message": "Address not found for user"}, 404

            address_json = AddressSchema().dump(address)
            user_json = UserSchema().dump(verified_user)
            roles = self.get_user_roles(verified_user.user_id)

            logger.info(f"Login successful for user: {verified_user.email}")
            return [token, user_json, address_json, roles], 200

        except NoResultFound:
            logger.error("No result found during login process")
            return {"message": "No result found"}, 404

        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            return {"message": "An unexpected error occurred"}, 500

    # Attempt login with token
        # Attempt login with token
    def login_with_token(self, token):
        try:
            if not token:
                logger.error("Token not provided")
                return False

            logger.info("Verifying token")
            verified_token = verify_auth_token(token)
            if verified_token:
                logger.info("Token verified successfully")
                return True
            else:
                logger.error("Invalid token")
                return False
        except Exception as e:
            logger.error(f"Unexpected error during token login: {e}")
            return False

    def forgot_password(self):
        """
        Handle forgot password request.
        Generate a token and send it to the user's email.
        """
        try:
            data = request.get_json()
            email = data.get('email')
            if not email:
                logger.error("Email is required for password reset")
                return {"message": "Email is required"}, 400

            user = User.query.filter_by(email=email).first()
            if not user:
                logger.error(f"User with email {email} not found")
                return {"message": "User not found"}, 404

            serializer = URLSafeTimedSerializer(
                current_app.config['SECRET_KEY'])
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = f"{current_app.config['BASE_URL']}/reset-password?token={token}"

            logger.info(f"Sending password reset email to {email}")
            send_password_reset_email(email, reset_url)

            logger.info(f"Password reset email sent to {email}")
            return {"message": "Password reset email sent"}, 200
        except Exception as e:
            logger.error(
                f"Unexpected error during forgot password process: {e}")
            return {"error": str(e)}, 500

    def reset_password(self):
        """
        Handle password reset using the token.
        """
        try:
            data = request.get_json()
            token = data.get('token')
            new_password = data.get('new_password')

            if not token or not new_password:
                logger.error("Token and new password are required")
                return {"message": "Token and new password are required"}, 400

            serializer = URLSafeTimedSerializer(
                current_app.config['SECRET_KEY'])
            try:
                email = serializer.loads(
                    token, salt='password-reset-salt', max_age=3600)
            except Exception as e:
                logger.error(f"Invalid or expired token: {e}")
                return {"message": "Invalid or expired token"}, 400

            user = User.query.filter_by(email=email).first()
            if not user:
                logger.error(f"User with email {email} not found")
                return {"message": "User not found"}, 404

            user.password = generate_password_hash(new_password)
            db.session.commit()

            logger.info(f"Password reset successful for user: {email}")
            return {"message": "Password reset successful"}, 200
        except Exception as e:
            logger.error(f"Unexpected error during password reset: {e}")
            return {"error": str(e)}, 500
