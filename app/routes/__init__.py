from .user_routes import bp_user
from .role_routes import bp_role
from .auth_routes import bp_auth
from .famille_routes import famille_bp
from .equipement_routes import equipement_bp
from .fournisseur_routes import fournisseur_bp
from .type_routes import type_bp

from .licence_routes import licence_bp
from .bon_livraison_routes import bon_bp

blueprints = [bp_user, bp_role, bp_auth, fournisseur_bp, famille_bp, equipement_bp, type_bp, licence_bp, bon_bp]