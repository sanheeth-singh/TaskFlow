from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize these variables but do not attach them to the 'app' yet
db = SQLAlchemy()
login_manager = LoginManager()

migrate = Migrate()