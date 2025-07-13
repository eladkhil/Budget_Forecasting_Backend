from app import create_app
from flask_cors import CORS
app = create_app()

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)



if __name__ == "__main__":
    # Only create tables once (or use Alembic migrations in real projects)
    with app.app_context():
        from app.extensions import db
        db.create_all()
    app.run(debug=True)
