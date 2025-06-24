from functools import wraps
from flask import session, abort

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            abort(401)          # not logged in
        return fn(*args, **kwargs)
    return wrapper
