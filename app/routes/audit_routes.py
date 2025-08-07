from app.extensions import db
from app.models.Audit import Audit
from app.models.AuditMembre import AuditMembre
from app.schemas.audit import AuditSchema
from flask import Blueprint,request,jsonify,abort
from sqlalchemy import func,collate
bp_audit = Blueprint("audits", __name__, url_prefix="/api/audits")
audits_schema=AuditSchema(many=True)
audit_schema  = AuditSchema()

@bp_audit.route("",methods=["GET"])
def list_audits():
    par_type=request.args.get("type")
    par_annee=request.args.get("annee")
    recherche=request.args.get("recherche")
    page =int(request.args.get("page",1))
    limite =int(request.args.get("limit",3))
    offset = (page - 1) * limite
    query=db.session.query(Audit)
    query = query.order_by(Audit.date.desc())
    if par_type:
        query=query.filter(Audit.type==par_type)
    if par_annee:
        query=query.filter(func.extract('year',Audit.date)==int(par_annee))
    if recherche and recherche.strip():
        query=query.filter(collate(Audit.titre,'Latin1_General_CI_AI').like(f"%{recherche}%"))
    totalAudit=query.count()
    audits= query.offset(offset).limit(limite).all()
    
    return jsonify({
        "totalAudit":totalAudit,
        "audits":[audit.to_dict() for audit in audits]})

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
        db.session.flush()
        responsables=data.get("responsables",[])
        for membre_id in responsables:
            audit_membre=AuditMembre(audit_id=audit.audit_id,membre_id=membre_id)
            db.session.add(audit_membre)
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
        AuditMembre.query.filter_by(audit_id=audit_id).delete()
        responsables=data.get("responsables",[])
        for membre_id in responsables:
            audit_membre=AuditMembre(audit_id=audit.audit_id,membre_id=membre_id)
            db.session.add(audit_membre)
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


