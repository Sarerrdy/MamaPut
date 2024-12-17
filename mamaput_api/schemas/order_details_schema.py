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

    menu = fields.Nested(MenuSchema)  # Include full Menu schema
    order = fields.Nested(OrderSchema)  # Include full Order schema

    # orders = fields.Nested(OrderSchema, only=(
    #     'order_id', 'total_price', 'date_ordered', 'expected_date_of_delivery', 'status', 'user_id'))
    # # order = fields.List(fields.Nested(OrderSchema(), dump_only=True))
    # menus = fields.Nested(MenuSchema, only=(
    #     'menu_id', 'name', 'price', 'menu_url'))

    @post_load
    def make_order_detail(self, data, **kwargs):
        return Order_Detail(**data)
