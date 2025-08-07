from flask import Blueprint, Response
from app.extensions import db
from app.models import Budget, Direction, Rubrique, Groupement, HorsBudget, ProjetDetail
from sqlalchemy import func
import plotly.graph_objs as go
import plotly.io as pio

bp_dashboard = Blueprint("dashboard_plotly", __name__, url_prefix="/api/dashboard-img")

@bp_dashboard.route("/evolution")
def evolution_budgets_img():
    rows = (
        db.session.query(Budget.year, func.sum(Budget.total_budget), func.sum(Budget.total_consommation))
        .group_by(Budget.year)
        .order_by(Budget.year)
        .all()
    )
    years = [str(r[0]) for r in rows]
    y_alloue = [r[1] or 0 for r in rows]
    y_consomme = [r[2] or 0 for r in rows]

    fig = go.Figure(data=[
        go.Bar(name="Alloué", x=years, y=y_alloue, marker=dict(color="#002856")),
        go.Bar(name="Consommé", x=years, y=y_consomme, marker=dict(color="#ea5455"))
    ])
    fig.update_layout(barmode="group", title="Évolution des Budgets")
    return Response(pio.to_image(fig, format='png'), mimetype='image/png')

@bp_dashboard.route("/ecart-evolution")
def evolution_ecart_img():
    rows = (
        db.session.query(Budget.year, func.sum(Budget.total_budget - Budget.total_consommation))
        .group_by(Budget.year)
        .order_by(Budget.year)
        .all()
    )
    years = [str(r[0]) for r in rows]
    ecarts = [r[1] for r in rows]

    fig = go.Figure(data=[
        go.Scatter(x=years, y=ecarts, mode='lines+markers', name='Écart', line=dict(color='#ff9900'))
    ])
    fig.update_layout(title="Évolution des Écarts (Alloué - Consommé)")
    return Response(pio.to_image(fig, format='png'), mimetype='image/png')

@bp_dashboard.route("/top-groupements")
def top_groupements_img():
    rows = (
        db.session.query(Groupement.name, func.sum(Groupement.budget_consomme))
        .group_by(Groupement.name)
        .order_by(func.sum(Groupement.budget_consomme).desc())
        .limit(5)
        .all()
    )
    fig = go.Figure(data=[
        go.Bar(x=[r[0] for r in rows], y=[r[1] for r in rows], marker=dict(color="#b93c3c"))
    ])
    fig.update_layout(title="Top 5 Groupements les Plus Consommateurs")
    return Response(pio.to_image(fig, format='png'), mimetype='image/png')

@bp_dashboard.route("/kpis/<int:year>")
def dashboard_kpis_by_year(year):
    rows = (
        db.session.query(
            func.sum(Budget.total_budget),
            func.sum(Budget.total_consommation)
        )
        .filter(Budget.year == year)
        .first()
    )

    total_budget = rows[0] or 0
    total_consommation = rows[1] or 0
    ecart_total = total_budget - total_consommation

    return {
        "year": year,
        "total_budget": round(total_budget, 2),
        "total_consommation": round(total_consommation, 2),
        "ecart": round(ecart_total, 2)
    }

@bp_dashboard.route("/years")
def get_all_years():
    years = db.session.query(Budget.year).distinct().order_by(Budget.year).all()
    return [y[0] for y in years]


@bp_dashboard.route("/repartition-direction")
def budget_par_direction_img():
    rows = (
        db.session.query(Direction.name, func.sum(Groupement.budget_alloue))
        .join(Rubrique, Rubrique.direction_id == Direction.id)
        .join(Groupement, Groupement.rubrique_id == Rubrique.id)
        .group_by(Direction.name)
        .all()
    )
    fig = go.Figure(data=[go.Pie(labels=[r[0] for r in rows], values=[r[1] for r in rows])])
    fig.update_layout(title="Répartition du Budget Alloué par Direction")
    return Response(pio.to_image(fig, format='png'), mimetype='image/png')

