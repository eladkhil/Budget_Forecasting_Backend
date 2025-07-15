from marshmallow import Schema, fields

class GroupementSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    rubrique_id = fields.Int(required=True)
    budget_alloue = fields.Float(allow_none=True)
    budget_consomme = fields.Float(allow_none=True)
    ecart = fields.Float(dump_only=True) 
    budget_id = fields.Int(allow_none=True)