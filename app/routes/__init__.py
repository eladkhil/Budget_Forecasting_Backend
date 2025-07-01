from .user_routes import bp_user
from .role_routes import bp_role
from .auth_routes import bp_auth 

blueprints = [bp_user, bp_role, bp_auth]
