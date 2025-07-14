from flask import Blueprint, jsonify,request,abort
from app.extensions import db,mail
from app.models.User import User
from app.models.Action import Action
from flask_mail import Message
import os
from app.schemas.action import ActionSchema
bp_action = Blueprint('actions', __name__, url_prefix='/api/actions')

action_schema=ActionSchema()
actions_schema=ActionSchema(many=True)

def notify_users_about_action(action,users):
    for user in users:
        try:
            msg = Message(
            subject="Nouvelle Action Assignée",
            recipients=[user.email],
            sender=os.getenv("SMTP_USER"),
            body=f"Bonjour {user.name},\n\nUne nouvelle action vous a été assignée :\n\n"
            f"- Description : {action.description}\n"
            f"- Statut : {action.statut}\n"
            f"- Date limite : {action.date_limite}\n\nMerci de prendre connaissance de cette tâche.",
            )
            mail.send(msg)
        except Exception as mail_err:
            print(f"Erreur envoi mail à {user.email} :", mail_err)
            print(f"Action users: {[user.user_id for user in action.users]}")
@bp_action.route("",methods=["GET"])
def list_actions():
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