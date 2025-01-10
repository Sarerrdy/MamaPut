from marshmallow import Schema, fields, post_load
from models.cart import Cart
from schemas.user_Address_schemas import UserSchema


class CartSchema(Schema):
    """
    CartSchema Marshmallow Schema

    Marshmallow schema used for loading/dumping Cart
    """

    cart_id = fields.Integer()
    date_created = fields.DateTime(allow_none=True)
    user_id = fields.Integer(allow_none=False)

    user = fields.Nested(UserSchema(), dump_only=True)

    @post_load
    def make_Cart(self, data, **kwargs):
        return Cart(**data)
