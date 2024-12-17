# from marshmallow import Schema, fields, post_load
from marshmallow import Schema, fields
from schemas.category_schema import CategorySchema
from schemas.user_schema import UserSchema
# from models.menu_order import MenuOrder
# from schemas.menu_schema import MenuSchema
# from schemas.order_schema import OrderSchema


class OrderBaseSchema(Schema):
    order_id = fields.Integer()
    total_price = fields.Float(allow_none=False)
    date_ordered = fields.DateTime(allow_none=False)
    expected_date_of_delivery = fields.DateTime()
    status = fields.String(allow_none=False)
    user_id = fields.Integer()
    user = fields.Nested(UserSchema(), dump_only=True)


class MenuBaseSchema(Schema):
    menu_id = fields.Integer()
    name = fields.String(allow_none=False)
    price = fields.Integer(allow_none=False)
    status = fields.String(allow_none=False)
    menu_url = fields.String(allow_none=False)
    category_id = fields.Integer()
    category = fields.Nested(CategorySchema(), dump_only=True)


# class MenuOrderSchema(Schema):
#     """
#     MenuOrder Marshmallow Schema

#     Marshmallow schema used for loading/dumping MenuOrders
#     """
#     menuorder_id = fields.Integer()
#     orders = fields.Nested(OrderBaseSchema(), many=True, dump_only=True)
#     menus = fields.Nested(MenuBaseSchema(), many=True, dump_only=True)

#     @post_load
#     def make_menuorder(self, data, **kwargs):
#         return MenuOrder(**data)
