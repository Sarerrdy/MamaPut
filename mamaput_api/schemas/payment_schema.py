from marshmallow import Schema, fields, post_load
from models.payment import Payment
from schemas.order_schema import OrderSchema


class PaymentSchema(Schema):
    """
    PaymentSchema Marshmallow Schema

    Marshmallow schema used for loading/dumping Payment
    """

    payment_id = fields.Integer()
    payment_Method = fields.String(allow_none=False)
    amount = fields.Float(allow_none=False)
    payment_status = fields.String(allow_none=False)
    payment_date = fields.DateTime(allow_none=True)
    reference = fields.String(required=True)
    order_id = fields.Integer()

    order = fields.Nested(OrderSchema)

    @post_load
    def make_Shipping(self, data, **kwargs):
        return Payment(**data)
