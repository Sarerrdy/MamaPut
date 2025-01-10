from marshmallow import EXCLUDE, Schema, fields, post_load, validates_schema, ValidationError, validate
from models.user import User
from models.address import Address


class UserSchema(Schema):
    """
    User Marshmallow Schema

    Marshmallow schema used for loading/dumping Users
    """

    class Meta:
        unknown = EXCLUDE  # Ignore unknown fields

    user_id = fields.Integer(allow_none=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    gender = fields.String(
        required=True, validate=validate.OneOf(["male", "female"]))
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=6))
    phone = fields.String(required=True, validate=[validate.Length(
        min=1), validate.Regexp(r'^\d+$', error="Phone number must contain only digits")])

    @validates_schema
    def validate_non_empty_strings(self, data, **kwargs):
        for field, value in data.items():
            if isinstance(value, str) and not value.strip() and not self.fields[field].allow_none:
                raise ValidationError(
                    f"{field} cannot be empty or contain only whitespace", field_names=[field])

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class AddressSchema(Schema):
    """
    Address Marshmallow Schema

    Marshmallow schema used for loading/dumping Addresses
    """

    class Meta:
        unknown = EXCLUDE  # Ignore unknown fields

    address_id = fields.Integer(allow_none=True)
    address = fields.String(required=True, validate=validate.Length(min=1))
    town = fields.String(required=True, validate=validate.Length(min=1))
    state = fields.String(required=True, validate=validate.Length(min=1))
    lga = fields.String(required=True, validate=validate.Length(min=1))
    landmark = fields.String(allow_none=True)  # Make landmark optional
    user_id = fields.Integer()

    @validates_schema
    def validate_non_empty_strings(self, data, **kwargs):
        for field, value in data.items():
            if isinstance(value, str) and not value.strip() and not self.fields[field].allow_none:
                raise ValidationError(
                    f"{field} cannot be empty or contain only whitespace", field_names=[field])

    @post_load
    def make_address(self, data, **kwargs):
        return Address(**data)
