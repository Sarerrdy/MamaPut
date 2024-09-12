from marshmallow import Schema, fields, post_load
from models.category import Category


class CategorySchema(Schema):
    """
    Category Marshmallow Schema

    Marshmallow schema used for loading/dumping Categories
    """

    category_id = fields.Integer()
    name = fields.String(allow_none=False)
    category_url = fields.String(allow_none=False)

    @post_load
    def make_category(self, data, **kwargs):
        return Category(**data)
