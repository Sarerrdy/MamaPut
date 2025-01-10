from marshmallow import Schema, fields, post_load
from models.order import Order
from schemas.user_Address_schemas import UserSchema


class OrderSchema(Schema):
    """
    Order Marshmallow Schema

    Marshmallow schema used for loading/dumping Orders
    """

    order_id = fields.Integer()
    total_price = fields.Float(allow_none=False)
    date_ordered = fields.String(allow_none=True)
    expected_date_of_delivery = fields.String(allow_none=True)
    status = fields.String(allow_none=False)
    user_id = fields.Integer()

    user = fields.Nested(UserSchema(), dump_only=True)

    # Excluding self referencing field
    orderdetails = fields.List(fields.Nested(
        'OrderDetailsSchema', exclude=('order',)))
    payment = fields.Nested(
        'PaymentSchema', exclude=('order',))
    shipping_info = fields.Nested(
        'ShippingInfoSchema', exclude=('order',))

    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)
