from .user_routes import bp_user
from .role_routes import bp_role
from .auth_routes import bp_auth 
from .audit_routes import bp_audit
from .vuln_routes import bp_vuln
from .action_routes import bp_action
blueprints = [bp_user, bp_role, bp_auth, bp_audit ,bp_vuln,bp_action]
