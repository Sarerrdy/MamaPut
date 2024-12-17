from marshmallow import Schema, fields, post_load
from models.role import Role


class RoleSchema(Schema):
    """
    Role Marshmallow Schema

    Marshmallow schema used for loading/dumping Roles
    """

    role_id = fields.Integer(allow_none=True)
    role_name = fields.String(required=True)

    @post_load
    def make_role(self, data, **kwargs):
        return Role(**data)
