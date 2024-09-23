from marshmallow import Schema, fields, post_load
from models.user import User


class LoginSchema(Schema):
    """
    User Marshmallow Schema

    Marshmallow schema used for loading/dumping Users
    """

    email = fields.Email(allow_none=False)
    password = fields.String(allow_none=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
