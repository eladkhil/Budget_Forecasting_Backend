from .user_routes import bp_user
from .role_routes import bp_role
from .auth_routes import bp_auth
from .license_routes import bp_license
from .software_routes import bp_software


blueprints = [bp_user, bp_role, bp_auth, bp_license, bp_software]
