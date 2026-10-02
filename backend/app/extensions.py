from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Database
db = SQLAlchemy()

# Database migrations
migrate = Migrate()

# User authentication
login_manager = LoginManager()

# Login route
login_manager.login_view = "auth.login"

# Message shown when authentication is required
login_manager.login_message = "Please log in to access this page."
