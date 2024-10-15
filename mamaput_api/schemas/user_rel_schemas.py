from marshmallow import Schema, fields, post_load
from models.user import User
from models.address import Address
# from schemas.address_schema import AddressSchema
# from schemas.user_schema import UserSchema


class UserSchema(Schema):
    """
    User Marshmallow Schema

    Marshmallow schema used for loading/dumping Users
    """

    user_id = fields.Integer(allow_none=True)
    title = fields.String(allow_none=False)
    first_name = fields.String(allow_none=False)
    last_name = fields.String(allow_none=False)
    gender = fields.String(allow_none=False)
    email = fields.Email(allow_none=False)
    password = fields.String(allow_none=False)
    phone = fields.Integer(allow_none=False)
    join_date = fields.DateTime(allow_none=True)
    user_url = fields.Url(allow_none=True)

    # addresses = fields.Nested(AddressSchema(), dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class AddressSchema(Schema):
    """
    Address Marshmallow Schema

    Marshmallow schema used for loading/dumping Addresses
    """

    address_id = fields.Integer(allow_none=True)
    address = fields.String(allow_none=False)
    town = fields.String(allow_none=False)
    state = fields.String(allow_none=False)
    lga = fields.String(allow_none=False)
    landmark = fields.String()
    user_id = fields.Integer()

    # user = fields.Nested(UserSchema(), dump_only=True)

    @post_load
    def make_Address(self, data, **kwargs):
        return Address(**data)
