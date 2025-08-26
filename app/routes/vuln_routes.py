from app.extensions import db
from app.models.Vuln import Vuln
from app.schemas.vuln import VulnSchema
from flask import Blueprint, jsonify,request,abort

bp_vuln = Blueprint("vulns", __name__, url_prefix="/api/vulns")
vulns_schema=VulnSchema(many=True)
vuln_schema  = VulnSchema()

@bp_vuln.route("",methods=["GET"])
def list_vulnerabilites():
    vulns=db.session.query(Vuln).all()
    return jsonify(vulns_schema.dump(vulns))


@bp_vuln.get("/audit/<int:audit_id>")
def get_vulns_by_audit(audit_id):
    page =int(request.args.get("page",1))
    limite =int(request.args.get("limit",3))
    offset = (page - 1) * limite
    query=db.session.query(Vuln).filter_by(audit_id=audit_id).order_by(Vuln.vul_id)
    totalVuln=query.count()
    vulns= query.offset(offset).limit(limite).all()
    return jsonify({
        "totalVuln":totalVuln,
        "vulns":[vuln.to_dict() for vuln in vulns]
    })

@bp_vuln.post("")
def create_vuln():
    data = request.json or {}
    print("JSON reçu :", data)  
    if not data:
        abort(400,"donnée json manquantes")
    try:
        vuln=Vuln(
            nom=data.get("nom"),
            description=data.get("description"),
            preuve=data.get("preuve"),
            type=data.get("type"),
            scenario=data.get("scenario"),
            processus=data.get("processus"),
            impacts=data.get("impacts"),
            niveau_impact=data.get("niveau_impact"),
            complex_exploi=data.get("complex_exploi"),
            proba=data.get("proba"),
            criticite=data.get("criticite"),
            priorite_mise_oeuvre=data.get("priorite_mise_oeuvre"),
            complex_mise_oeuvre=data.get("complex_mise_oeuvre"),
            audit_id=data.get("audit_id")
        )
        db.session.add(vuln)
        db.session.commit()
        return jsonify({
            "status": "success",
            "vul_id": vuln.vul_id,
            "message": "vulnerabilité créée avec succès"
        }), 201
    except Exception as e:
        db.session.rollback()
        print("Erreur:", e)
        abort(500, "Erreur lors de la création de la vulnerabilité")

@bp_vuln.get("/<int:vul_id>")
def get_vuln(vul_id):
    vuln = Vuln.query.get_or_404(vul_id)
    return vuln_schema.dump(vuln)

@bp_vuln.delete("/<int:vul_id>")
def delete_vuln(vul_id):
    vuln = Vuln.query.get_or_404(vul_id)
    db.session.delete(vuln)
    db.session.commit()
    return "", 204

@bp_vuln.put("/<int:vul_id>")
def update_vuln(vul_id):
    vuln = Vuln.query.get_or_404(vul_id)
    data = request.json or {}
    try:
            vuln.nom=data.get("nom",vuln.nom)
            vuln.description=data.get("description",vuln.description)
            vuln.preuve=data.get("preuve",vuln.preuve)
            vuln.type=data.get("type",vuln.type)
            vuln.scenario=data.get("scenario",vuln.scenario)
            vuln.processus=data.get("processus",vuln.processus)
            vuln.impacts=data.get("impacts",vuln.impacts)
            vuln.niveau_impact=data.get("niveau_impact",vuln.niveau_impact)
            vuln.complex_exploi=data.get("complex_exploi",vuln.complex_exploi)
            vuln.proba=data.get("proba",vuln.proba)
            vuln.criticite=data.get("criticite",vuln.criticite)
            vuln.priorite_mise_oeuvre=data.get("priorite_mise_oeuvre",vuln.priorite_mise_oeuvre)
            vuln.complex_mise_oeuvre=data.get("complex_mise_oeuvre",vuln.complex_mise_oeuvre)
            vuln.audit_id=data.get("audit_id",vuln.audit_id)
            db.session.commit()
            return jsonify({
            "status": "success",
            "vul_id":vuln.vul_id,
            "message": "vuln modifié avec succès"
        }), 201
    except Exception as e:
        db.session.rollback()
        print("Erreur:", e)
        abort(500, "Erreur lors de la modification de l'vuln")
