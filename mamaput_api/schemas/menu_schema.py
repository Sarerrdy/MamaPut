from marshmallow import Schema, fields, post_load
from models.menu import Menu
from schemas.category_schema import CategorySchema
# from schemas.order_schema import OrderSchema
# from schemas.menu_order_schema import MenuOrderSchema
from schemas.menu_order_schema import OrderBaseSchema


class MenuSchema(Schema):
    """
    Menu Marshmallow Schema

    Marshmallow schema used for loading/dumping menus
    """

    menu_id = fields.Integer()
    name = fields.String(allow_none=False)
    price = fields.Integer(allow_none=False)
    status = fields.String(allow_none=False)
    menu_url = fields.String(allow_none=False)
    category_id = fields.Integer()
    order_id = fields.Integer()

    category = fields.Nested(CategorySchema(), dump_only=True)
    # orders = fields.Nested(OrderSchema(), dump_only=True)
    orders = fields.Nested(OrderBaseSchema(), many=True, dump_only=True)

    @post_load
    def make_menu(self, data, **kwargs):
        return Menu(**data)
