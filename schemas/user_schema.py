from marshmallow import Schema, fields, post_load
from models.user import User
# from schemas.address_schema import AddressSchema


class UserSchema(Schema):
    """
    User Marshmallow Schema

    Marshmallow schema used for loading/dumping Users
    """

    # user_id = fields.Integer()
    # title = fields.String(allow_none=False)
    # first_name = fields.String(allow_none=False)
    # last_name = fields.String(allow_none=False)
    # gender = fields.String(allow_none=False)
    # email = fields.Email(allow_none=False)
    # password = fields.String(allow_none=False)
    # phone = fields.Integer(allow_none=False)
    # join_date = fields.DateTime(allow_none=True)
    # user_url = fields.Url(allow_none=False)

    # addr = fields.Nested(AddressSchema(), dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
