from marshmallow import Schema, fields


# Schema For API
class CarSchema(Schema):
    id = fields.String()
    year = fields.Integer()
    make = fields.String()
    created_at = fields.String()
    updated_at = fields.String()
