from app.extensions import db

licence_equipement = db.Table(
    'licence_equipement',
    db.Column('licence_id', db.Integer, db.ForeignKey('Licence.id_licence'), primary_key=True),
    db.Column('equipement_id', db.Integer, db.ForeignKey('Equipement.id_equipement'), primary_key=True),
    extend_existing=True
)