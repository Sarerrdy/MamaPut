from flask import request
from flask_restful import Resource
from models.role import Role
from schemas.role_schema import RoleSchema


class RoleResource(Resource):
    def get(self):
        roles = Role.query.all()
        role_schema = RoleSchema(many=True)
        return role_schema.dump(roles), 200

    def post(self):
        data = request.get_json()
        role_schema = RoleSchema()
        role = role_schema.load(data)
        role.save()
        return role_schema.dump(role), 201
