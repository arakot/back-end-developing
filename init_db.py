from app import db, app  # Import both db and app

with app.app_context():  # Create an application context
    db.create_all()
    print("Database initialized successfully!")