from marshmallow import Schema, fields, validate


class ReviewSchema(Schema):
    review_id = fields.Int(dump_only=True)
    menu_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    review = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    user_names = fields.Str(required=True)
