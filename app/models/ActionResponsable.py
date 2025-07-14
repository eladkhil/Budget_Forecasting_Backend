from app.extensions import db

action_responsable = db.Table(
    'Action_Responsable',
    db.Column('user_id', db.Integer, db.ForeignKey('User.user_id'), primary_key=True),
    db.Column('action_id', db.Integer, db.ForeignKey('Action.action_id'), primary_key=True)
)
