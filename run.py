from app import create_app
from app.utils.notifier import socketio

app = create_app()

if __name__ == "__main__":
    """# Only create tables once (or use Alembic migrations in real projects)
    with app.app_context():
        from app.extensions import db
        db.create_all()"""
    socketio.run(app, debug=False, port=5000,host='0.0.0.0',allow_unsafe_werkzeug=False
)
