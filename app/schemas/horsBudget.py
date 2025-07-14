from marshmallow import Schema, fields

class HorsBudgetSchema(Schema):
    id = fields.Int(dump_only=True)
    article = fields.Str(required=True)
    prix_ht = fields.Float(required=True)
    qte = fields.Int(required=True)
    fournisseur = fields.Str(allow_none=True)

    # Foreign keys
    budget_id = fields.Int(required=True)
    direction_id = fields.Int(required=True)
