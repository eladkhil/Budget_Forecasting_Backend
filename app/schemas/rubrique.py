from marshmallow import Schema, fields

class RubriqueSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    direction_id = fields.Int(required=True)
