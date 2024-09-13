from marshmallow import Schema, fields, post_load
from models.order_details import Order_Detail
from schemas.order_schema import OrderSchema
from schemas.menu_schema import MenuSchema


class OrderDetailsSchema(Schema):
    """
    OrderDetailsSchema Marshmallow Schema

    Marshmallow schema used for loading/dumping OrderDetailsSchema
    """

    order_details_id = fields.Integer()
    quantity = fields.Integer(allow_none=False)
    discount = fields.Float(allow_none=True)
    price = fields.Float(allow_none=False)
    menu_id = fields.Integer()
    order_id = fields.Integer()

    order = fields.Nested(OrderSchema(), dump_only=True)
    menus = fields.Nested(MenuSchema(), dump_only=True)

    @post_load
    def make_order_detail(self, data, **kwargs):
        return Order_Detail(**data)
