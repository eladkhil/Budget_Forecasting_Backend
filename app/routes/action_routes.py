from flask import Blueprint, jsonify,request,abort
from app.extensions import db
from app.models.User import User
from app.models.Action import Action
from app.utils.email_utils import notify_users_about_action
from app.schemas.action import ActionSchema
from datetime import datetime

bp_action = Blueprint('actions', __name__, url_prefix='/api/actions')

action_schema=ActionSchema()
actions_schema=ActionSchema(many=True)

@bp_action.route("",methods=["GET"])
def list_actions():
    statut_actions()
    actions=db.session.query(Action).all()
    return jsonify(actions_schema.dump(actions))
@bp_action.post("")
def ajouter_action():
    data = request.json or {}
    if not data:
        abort(400,"donnée json manquantes")
    try:
        action=Action(
            description = data.get('description'),
            statut = data.get('statut'),
            date_limite = data.get('date_limite'),
            vul_id= data.get('vul_id')
        )
        db.session.add(action)
        db.session.flush()
        user_ids=data.get('userIds',[])
        users=[]
        for user_id in user_ids:
            user = User.query.get(user_id)
            if user:
                action.users.append(user)
                users.append(user)

        notify_users_about_action(action,users)
        db.session.commit()
        return jsonify({
            "status": "success",
            "action_id": action.action_id,
            "message": "action créée avec succès"
        }), 201
    except Exception as e:
        db.session.rollback()
        print("Erreur:", e)
        abort(500,"erreur d'ajout action")

@bp_action.get("/vuln/<int:vul_id>")
def get_actions_by_vuln(vul_id):
    actions=Action.query.filter_by(vul_id=vul_id).all()
    return jsonify(actions_schema.dump(actions))

@bp_action.delete("/<int:action_id>")
def delete_action(action_id):
    action = Action.query.get_or_404(action_id)
    db.session.delete(action)
    db.session.commit()
    return "", 204
@bp_action.put("/<int:action_id>")
def update_action(action_id):
    action = Action.query.get_or_404(action_id)
    data = request.json or {}
    try:
        action.description = data.get('description',action.description)
        action.statut = data.get('statut',action.statut)
        action.date_limite = data.get('date_limite',action.date_limite)
        action.vul_id= data.get('vul_id',action.vul_id)
        db.session.flush()
        user_ids=data.get('userIds',[])
        action.users.clear()
        users=[]
        for user_id in user_ids:
            user = User.query.get(user_id)
            if user:
                action.users.append(user)
                users.append(user)
        notify_users_about_action(action,users)
        db.session.commit()

        return jsonify({
            "status": "success",
            "action_id": action.action_id,
            "message": "action modifié avec succès"
        }), 200
    except Exception as e:
        db.session.rollback()
        print("Erreur:", e)
        abort(500,"erreur lors de modification d'action")

@bp_action.get("/<int:action_id>")
def get_action(action_id):
    action = Action.query.get_or_404(action_id)
    return action_schema.dump(action)
def statut_actions():
    now=datetime.utcnow()
    actions=Action.query.all()
    change= False
    for action in actions:
        old_statut = action.statut
        action.auto_change()
        if action.statut != old_statut:
            change=True
    if change:
        db.session.commit()