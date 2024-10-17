from marshmallow import Schema, fields, post_load
from models.menu import Menu
from schemas.category_schema import CategorySchema


class MenuSchema(Schema):
    """
    Menu Marshmallow Schema

    Marshmallow schema used for loading/dumping menus
    """

    menu_id = fields.Integer()
    name = fields.String(allow_none=False)
    description = fields.String(allow_none=False)
    price = fields.Float(allow_none=False)
    stock_quantity = fields.Integer(allow_none=True)
    status = fields.String(allow_none=False)
    menu_url = fields.String(allow_none=False)

    category_id = fields.Integer()
    category = fields.Nested(CategorySchema(), dump_only=True)

    # # Excluding self referencing field
    orderdetails = fields.Nested(
        'OrderDetailsSchema', exclude=('menu',))

    @post_load
    def make_menu(self, data, **kwargs):
        return Menu(**data)
