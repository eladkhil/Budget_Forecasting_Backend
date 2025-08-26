from .user_routes import bp_user
from .role_routes import bp_role
from .auth_routes import bp_auth 
from .audit_routes import bp_audit
from .vuln_routes import bp_vuln
from .action_routes import bp_action
from .email_config_routes import bp_email_config
from .annee_routes import bp_annee
from .stats_routes import bp_stats
from .societe_routes import bp_societe
from .membre_routes import bp_membre
from .notif_routes import bp_notif
blueprints = [bp_user, bp_role, bp_auth, bp_audit ,bp_vuln,bp_action ,bp_email_config,bp_annee,bp_stats,bp_societe,bp_membre,bp_notif]
