from marshmallow import Schema, fields

class ProjetDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    groupement_id = fields.Int(required=True)
    type = fields.Str(required=True)
    montant = fields.Float(required=True)
    montant_consomme = fields.Float(allow_none=True)