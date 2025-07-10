from marshmallow import Schema, fields

class BudgetSchema(Schema):
    id = fields.Int(dump_only=True)
    year = fields.Int(required=True)
    cloture = fields.Bool()
    total_budget = fields.Float()
    total_consommation = fields.Float()
    ecart = fields.Float(allow_none=True)