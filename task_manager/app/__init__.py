from flask import Flask
from .extensions import db, login_manager,migrate
from .models import User


def create_app():
    app = Flask(__name__)

    # Configuration
    app.secret_key = "AccessingSession"
    app.config['SECRET_KEY'] = "form_access_CSRF"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///system.db"

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)

    migrate.init_app(app,db)

    # Setup Login Manager
    # Tells Flask where to redirect if user isn't logged in
    login_manager.login_view = "auth.login"  # Note: 'auth.login', not just 'login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Register Blueprints
    from .auth.routes import auth
    from .main.routes import main

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')

    # # Create Database Tables
    with app.app_context():
        db.create_all()

    return app