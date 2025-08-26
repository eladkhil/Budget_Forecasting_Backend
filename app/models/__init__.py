from app.extensions import db
from .Role import Role
from .User import User
from .Societe import Societe
from .Membre import Membre
from .Audit import Audit
from .AuditMembre import AuditMembre
from .Vuln import Vuln
from .Action import Action
from .ActionResponsable import action_responsable
from .Notifications import Notifications
from .NotifUser import NotifUser
def configure_relationships():
    db.configure_mappers()