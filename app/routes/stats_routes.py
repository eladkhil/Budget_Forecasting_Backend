from app.extensions import db
from sqlalchemy import text
from flask import Blueprint,jsonify
from app.routes.action_routes import statut_actions
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

@bp_stats.route("/urgent",methods=["GET"])
def criticite_urgent():
    results=db.session.execute(text("""
    SELECT v.vul_id,v.nom,v.criticite,v.audit_id,v.niveau_impact,v.proba,v.complex_mise_oeuvre
    From (select vul_id,nom,audit_id,criticite,niveau_impact,proba,complex_mise_oeuvre,(
        (case niveau_impact when 'Fort' then 3 when 'Moyen' then 2 else 1 end)+
        (case proba  when 'plus' then 3 when 'Probable' then 2 else 1 end)-
        (case complex_mise_oeuvre when 'Simple' then 1 when 'Moyenne' then 2 else 3 end)
        )As score From Vuln)v 
        JOIN Audit a ON a.audit_id = v.audit_id 
        order by
        case v.criticite when 'Fort' then 3 when 'Moyen' then 2 else 1 end desc,v.score desc;
    """)).mappings().all()
    data=[dict(row) for row in results]
    return jsonify(data)
@bp_stats.route("/evolaudit",methods=["GET"])
def audit_evolution():
    results=db.session.execute(text("""
    SELECT 
        ISNULL( a.TotalAudit ,0) As TotalAudit ,
        m.mois,
        m.annee 
        From (
        SELECT MONTH(DATEADD(MONTH, -1, GETDATE())) AS mois, YEAR(DATEADD(MONTH, -1,GETDATE())) AS annee
        UNION ALL
            SELECT  MONTH(GETDATE()),YEAR(GETDATE()) ) m
        Left JOIN (select month(date) as mois, year(date) as annee , count(audit_id) as TotalAudit from Audit 
            Group by month(date),year(date) ) a
        ON a.annee=m.annee AND m.mois=a.mois
    order by m.mois, m.annee;
    """)).mappings().all()
    data=[dict(row) for row in results]
    for i in range(len(data)):
        if i==0:
            data[i]['evolution']=0
        else:
            pre=data[i-1]['TotalAudit']
            curr=data[i]['TotalAudit']
            if pre==0:
                data[i]['evolution']=100
            else:
                data[i]['evolution']=round((curr-pre)*100/pre,2)

    return jsonify(data)
@bp_stats.route("/nbvuln",methods=["GET"])
def Nbr_vuln():
    results=db.session.execute(text("""
    SELECT count(vul_id) as TotalVuln,Sum(Case when criticite='Fort' then 1 else 0 End)as critique From Vuln;
    """)).mappings().all()
    data=[dict(row) for row in results]
    return jsonify(data)

@bp_stats.route("/cours",methods=["GET"])
def action_En_Cours():
    statut_actions()
    results=db.session.execute(text("""
    SELECT count(*) ActionCours, sum(case when DATEDIFF(Day,GETDATE(),date_limite) 
    BETWEEN 1 and 2 then 1 else 0 end) as Proche from Action where statut='En cours'""")).mappings().all()
    data=[dict(row) for row in results]
    return jsonify(data)

@bp_stats.route("/conforme",methods=["GET"])
def taux_conformité():
    results=db.session.execute(text("""
        With trimestres As(
        select 1 as trimestre
        union all select 2
        union all select 3
        union all select 4),
    Taux As(
    SELECT DATEPART(QUARTER, date_limite) AS trimestre,
    Cast( sum (case when statut ='Validée' then 1 else 0 end)*100.0/count(*)
        as decimal(5,2))as tauxConformite  From Action
    where YEAR(date_limite) = YEAR(GETDATE())
    GROUP BY DATEPART(QUARTER, date_limite))
    SELECT t.trimestre,ISNULL(a.tauxConformite,0) As tauxConformite From trimestres t         
    LEFT JOIN Taux a ON t.trimestre = a.trimestre;
    """)).mappings().all()
    data=[dict(row) for row in results]
    for i in range(len(data)):
        if i==0:
            data[i]['evolution']=0
        else:
            pre=data[i-1]['tauxConformite']
            curr=data[i]['tauxConformite']
            if pre==0:
                data[i]['evolution']=100
            else:
                data[i]['evolution']=round((curr-pre)*100/pre,2)
    return jsonify(data)
