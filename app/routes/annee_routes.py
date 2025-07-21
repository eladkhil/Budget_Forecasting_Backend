from app.models.Audit import Audit
from app.extensions import db
from flask import Blueprint, jsonify
from sqlalchemy import extract

bp_annee = Blueprint("annees", __name__, url_prefix="/api/audits/annees")

@bp_annee.route("",methods=["GET"])
def list_annees():
    list_annees=[]
    anneeSelect=extract('year',Audit.date).label("annee")
    annees=(
        db.session.query(anneeSelect).distinct().order_by(anneeSelect.desc()).all())
    for annee in annees:
        if(annee[0] is not None):
            list_annees.append(int(annee[0]))
    return jsonify(list_annees)