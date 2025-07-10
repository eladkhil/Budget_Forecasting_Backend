from marshmallow import Schema, fields

class ConsommationSchema(Schema):
    id = fields.Int(dump_only=True)
    groupement_id = fields.Int(required=True)
    montant = fields.Float(required=True)