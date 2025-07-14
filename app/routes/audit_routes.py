from app.extensions import db
from app.models.Audit import Audit
from app.schemas.audit import AuditSchema
from flask import Blueprint, jsonify,request,abort

bp_audit = Blueprint("audits", __name__, url_prefix="/api/audits")
audits_schema=AuditSchema(many=True)
audit_schema  = AuditSchema()

@bp_audit.route("",methods=["GET"])
def list_audits():
    audits=db.session.query(Audit).all()
    return jsonify(audits_schema.dump(audits))

@bp_audit.get("/<int:audit_id>")
def get_audit(audit_id):
    audit = Audit.query.get_or_404(audit_id)
    return audit_schema.dump(audit)

@bp_audit.post("")
def create_audit():
    data = request.json or {}
    if not data:
        abort(400,"donnée json manquantes")
    try:
        audit=Audit(
            titre=data.get("titre"),
            type=data.get("type"),
            date=data.get("date"),
            description=data.get("description"),
            user_id=data.get("user_id")

        )
        db.session.add(audit)
        db.session.commit()
        return jsonify({
            "status": "success",
            "id_audit": audit.audit_id,
            "message": "audit créée avec succès"
        }), 201
    except Exception as e:
        db.session.rollback()
        print("Erreur:", e)
        abort(500, "Erreur lors de la création de l'audit")

@bp_audit.delete("/<int:audit_id>")
def delete_audit(audit_id):
    audit = Audit.query.get_or_404(audit_id)
    db.session.delete(audit)
    db.session.commit()
    return "", 204
@bp_audit.put("/<int:audit_id>")
def update_audit(audit_id):
    audit = Audit.query.get_or_404(audit_id)
    data = request.json or {}
    try:
        audit.titre = data.get('titre', audit.titre)
        audit.type = data.get('type', audit.type)
        audit.date = data.get('date', audit.date)
        audit.description = data.get('description', audit.description)
        audit.user_id = data.get('user_id', audit.user_id)
        db.session.commit()
        return jsonify({
            "status": "success",
            "id_audit": audit.audit_id,
            "message": "audit modifié avec succès"
        }), 201
    except Exception as e:
        db.session.rollback()
        print("Erreur:", e)
        abort(500, "Erreur lors de la modification de l'audit")


