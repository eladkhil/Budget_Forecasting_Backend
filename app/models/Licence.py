from app.extensions import db
from .User import User 
from .Famille import Famille
from .Type import Type
from .Equipement import Equipement
from .BonLivraison import BonLivraison
from datetime import date



class Licence(db.Model):
    __tablename__ = 'Licence'

    id_licence = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(100), nullable=False)
    cle_licence = db.Column(db.String(100), unique=True)
    periode = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    nombre_siestes = db.Column(db.Integer)
    date_expiration = db.Column(db.Date)

    # Relations
    id_famille = db.Column(db.Integer, db.ForeignKey('Famille.id_famille'))
    id_type = db.Column(db.Integer, db.ForeignKey('Type.id_type'))
    id_equipements = db.Column(db.Integer, db.ForeignKey('Equipement.id_equipement'))

    bons_livraison = db.relationship('BonLivraison', backref='licence', lazy=True)
    famille = db.relationship('Famille', backref='licences', lazy=True)
    type_objet = db.relationship('Type', back_populates='licences')
