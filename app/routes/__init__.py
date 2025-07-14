from .user_routes import bp_user
from .role_routes import bp_role
from .auth_routes import bp_auth 
from .direction_routes import bp_direction
from .rubrique_routes import bp_rubrique
from .groupement_routes import bp_groupement
from .budget_routes import bp_budget
from .projetDetail_routes import bp_projet_detail
from .budget_routes import bp_report
from .prediction_routes import bp_prediction 
from .horsBudget_routes import bp_hors_budget
blueprints = [bp_user, bp_role, bp_auth, bp_direction, bp_rubrique, bp_groupement, bp_budget,  bp_projet_detail, bp_report, bp_prediction,bp_hors_budget]
