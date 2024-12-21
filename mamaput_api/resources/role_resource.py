# role_resource.py
from flask import request
from flask_restful import Resource
from models.role import Role
from schemas.role_schema import RoleSchema

ROLES_ENDPOINT = "/api/roles"


class RolesResource(Resource):
    def get(self, id=None):
        try:
            roles = Role.query.all()
            role_schema = RoleSchema(many=True)
            roles_data = role_schema.dump(roles)
            return roles_data, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        role_schema = RoleSchema()
        role = role_schema.load(data)
        role.save()
        return role_schema.dump(role), 201
