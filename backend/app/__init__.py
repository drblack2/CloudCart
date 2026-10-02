from flask import Flask, jsonify, render_template
from flask_login import login_required, current_user

from app.config import Config
from app.extensions import db, migrate, login_manager
from app.models import User, Product
from app.routes import (
    auth_bp,
    products_bp,
    cart_bp,
    orders_bp,
    admin_bp
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/admin")
    @login_required
    def admin_dashboard():
        if current_user.role != "admin":
            return "Admin access required", 403

        return render_template("admin.html")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "application": "CloudCart",
            "version": "1.0.0"
        }), 200

    return app
