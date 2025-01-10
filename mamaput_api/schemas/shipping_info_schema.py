from marshmallow import Schema, fields, post_load
from schemas.order_schema import OrderSchema
from schemas.user_Address_schemas import AddressSchema
from models.shipping_info import ShippingInfo


class ShippingInfoSchema(Schema):
    """
    ShippingInfoSchema Marshmallow Schema

    Marshmallow schema used for loading/dumping ShippingInfo
    """

    shipping_info_id = fields.Integer()
    shipping_Method = fields.String(allow_none=False)
    shipping_cost = fields.Float(allow_none=False)
    shipping_status = fields.String(allow_none=False)
    shipped_date = fields.DateTime(allow_none=True)
    expected_delivery_date = fields.DateTime()
    order_id = fields.Integer()
    address_id = fields.Integer()

    order = fields.Nested(OrderSchema)
    address = fields.Nested(AddressSchema)

    @post_load
    def make_ShippingInfo(self, data, **kwargs):
        return ShippingInfo(**data)
