from marshmallow import Schema, fields, post_load
from models.order import Order
from schemas.user_schema import UserSchema


class OrderSchema(Schema):
    """
    Order Marshmallow Schema

    Marshmallow schema used for loading/dumping Orders
    """

    order_id = fields.Integer()
    total_price = fields.Float(allow_none=False)
    date_ordered = fields.DateTime(allow_none=True)
    expected_date_of_delivery = fields.DateTime(allow_none=True)
    status = fields.String(allow_none=False)
    user_id = fields.Integer()

    user = fields.Nested(UserSchema(), dump_only=True)

    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)
