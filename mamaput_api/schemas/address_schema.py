from marshmallow import Schema, fields, post_load
from models.address import Address
from schemas.user_schema import UserSchema


class AddressSchema(Schema):
    """
    Address Marshmallow Schema

    Marshmallow schema used for loading/dumping Addresses
    """

    address_id = fields.Integer()
    address = fields.String(allow_none=False)
    town = fields.String(allow_none=False)
    state = fields.String(allow_none=False)
    lga = fields.String(allow_none=False)
    landmark = fields.String()
    user_id = fields.Integer()

    user = fields.Nested(UserSchema(), dump_only=True)

    @post_load
    def make_Address(self, data, **kwargs):
        return Address(**data)
