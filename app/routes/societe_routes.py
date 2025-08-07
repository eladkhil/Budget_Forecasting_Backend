from flask import Blueprint, request, abort,jsonify
from app.extensions import db
from app.models.Societe import Societe
from app.schemas.societe import SocieteSchema

bp_societe = Blueprint("societes", __name__, url_prefix="/api/societes")
societe_schema = SocieteSchema()
societes_schema = SocieteSchema(many=True)


@bp_societe.route("",methods=["GET"])
def list_societes():
    return societes_schema.dump(Societe.query.all())

@bp_societe.post("")
def ajouter_societe():
    data = request.json or {}
    if not data:
        abort(400,"donnée json manquantes")
    nom=data.get('nom').strip().lower()
    societe_existe=Societe.query.filter_by(nom=nom).first()
    if societe_existe:
        return jsonify({
            'error':'la sociéte existe déjà'
        }),409
    try:
        societe=Societe(
            nom=nom,
            adresse=data.get("adresse"),
            telephone_contact=data.get("telephone_contact"),
            email_contact=data.get("email_contact")
        )
        db.session.add(societe)
        db.session.commit()
        return jsonify({'message': 'Société ajoutée avec succès'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@bp_societe.delete("/<int:societe_id>")
def delete_audit(societe_id):
    societe = Societe.query.get_or_404(societe_id)
    db.session.delete(societe)
    db.session.commit()
    return "", 204