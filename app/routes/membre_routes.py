from flask import Blueprint, request, abort,jsonify
from app.extensions import db
from app.models.Membre import Membre
from app.schemas.membre import MemberSchema
from app.models.AuditMembre import AuditMembre
from app.schemas.auditmembre import AuditMembreSchema

bp_membre = Blueprint("membres", __name__, url_prefix="/api/membres")
membre_schema = MemberSchema()
membres_schema = MemberSchema(many=True)
auditmembres_schema = AuditMembreSchema(many=True)


@bp_membre.route("",methods=["GET"])
def list_membres():
    return membres_schema.dump(Membre.query.all())

@bp_membre.post("")
def ajouter_membre():
    data = request.json or {}
    if not data:
        abort(400,"donnée json manquantes")
    email=data.get('email').strip().lower()
    email_existe=Membre.query.filter_by(email=email).first()
    if email_existe:
        return jsonify({
            'error':'corrige email'
        }),409
    try:
        membre=Membre(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            email=email,
            telephone=data.get("telephone"),
            typeMembre=data.get("typeMembre"),
            titre=data.get("titre"),
            societe_id=data.get("societe_id") if data.get("typeMembre") == "externe" else None
        )
        db.session.add(membre)
        db.session.commit()
        return jsonify({'message': 'membre ajoutée avec succès'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp_membre.route("societe/<int:societe_id>",methods=["GET"])
def membres_par_societe(societe_id):
    membres = Membre.query.filter_by(societe_id=societe_id).all()
    return jsonify(membres_schema.dump(membres))

@bp_membre.route("interne",methods=["GET"])
def membres_internes():
    membres = Membre.query.filter_by(societe_id=None, typeMembre='interne').all()
    return jsonify(membres_schema.dump(membres))

@bp_membre.get("/ids")
def get_membres_by_ids():
    ids_str=request.args.get("ids")
    if not ids_str:
        return jsonify([])
    ids=[]
    for id in ids_str.split(","):
        if id.isdigit():
            ids.append(id)
    membres = Membre.query.filter(Membre.membre_id.in_(ids)).all()
    return jsonify(membres_schema.dump(membres))

@bp_membre.route("audit/<int:audit_id>",methods=["GET"])
def membres_par_audit(audit_id):
    auditmembres = AuditMembre.query.filter_by(audit_id=audit_id).all()
    return jsonify(auditmembres_schema.dump(auditmembres))

@bp_membre.delete("/<int:membre_id>")
def delete_audit(membre_id):
    membre = Membre.query.get_or_404(membre_id)
    db.session.delete(membre)
    db.session.commit()
    return "", 204