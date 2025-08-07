from app.extensions import db
from sqlalchemy import text
from flask import Blueprint,jsonify
bp_stats = Blueprint("stats", __name__, url_prefix="/api/stats")

@bp_stats.route("/type",methods=["GET"])
def TypeAudit_par_mois():
    results=db.session.execute(text("""
    SELECT type,month(date) AS mois, 
    COUNT(*) AS total_audits FROM Audit 
    where year(date)=year(getdate())
    GROUP BY type,month(date)""")).mappings().all()
    data=[dict(row) for row in results]
    return jsonify(data)

@bp_stats.route("/criticite",methods=["GET"])
def niveau_criticite():
    results=db.session.execute(text("""
    SELECT criticite, ROUND(CAST(COUNT(*) * 100.0 / SUM(COUNT(*))
     OVER ()AS NUMERIC(5,2)), 2) as 
    pourcentage_criticite FROM Vuln 
    group by criticite""")).mappings().all()
    data=[dict(row) for row in results]
    return jsonify(data)