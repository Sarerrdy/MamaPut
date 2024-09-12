from marshmallow import Schema, fields, post_load
from models.review import Review
from schemas.user_schema import UserSchema
from schemas.menu_schema import MenuSchema


class ReviewSchema(Schema):
    """
    Review Marshmallow Schema

    Marshmallow schema used for loading/dumping Reviews
    """

    review_id = fields.Integer()
    content = fields.String()
    rating = fields.Integer(allow_none=False)
    has_reviewed = fields.Boolean(allow_none=False)
    date_reviewed = fields.DateTime(allow_none=False)

    menu = fields.Nested(UserSchema(), dump_only=True)
    reviewer = fields.Nested(MenuSchema(), dump_only=True)

    @post_load
    def make_Review(self, data, **kwargs):
        return Review(**data)
