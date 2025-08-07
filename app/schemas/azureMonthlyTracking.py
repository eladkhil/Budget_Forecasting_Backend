from marshmallow import Schema, fields

class AzureMonthlyTrackingSchema(Schema):
    id = fields.Int(dump_only=True)
    groupement_id = fields.Int(required=True)
    mois = fields.Str()
    periode = fields.Str()
    fournisseur = fields.Str()
    numero_facture = fields.Str()

    reservation = fields.Decimal(as_string=True)
    consommation = fields.Decimal(as_string=True)
    montant_ht = fields.Decimal(as_string=True, dump_only=True)
    tva_percent = fields.Decimal(as_string=True)
    montant_tva = fields.Decimal(as_string=True, dump_only=True)
