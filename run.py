from app import create_app
app = create_app()

if __name__ == "__main__":
    # Only create tables once (or use Alembic migrations in real projects)
    with app.app_context():
        from app.extensions import db
        db.create_all()
    app.run(debug=True)
