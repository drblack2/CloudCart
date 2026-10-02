from flask import render_template
from flask import Blueprint, request, jsonify
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sqlalchemy import select
from email_validator import validate_email, EmailNotValidError

from app.extensions import db
from app.models import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({
            "error": "Username, email and password are required"
        }), 400

    if len(username) > 80:
        return jsonify({
            "error": "Username must be 80 characters or fewer"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must contain at least 8 characters"
        }), 400

    try:
        email = validate_email(
            email,
            check_deliverability=False
        ).normalized

    except EmailNotValidError:
        return jsonify({
            "error": "Please provide a valid email address"
        }), 400

    existing_user = db.session.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        return jsonify({
            "error": "Email is already registered"
        }), 409

    user = User(
        username=username,
        email=email,
        role="customer"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = db.session.scalar(
        select(User).where(User.email == email)
    )

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    login_user(user)

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200


@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({
        "user": current_user.to_dict()
    }), 200

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    return jsonify({
        "message": "Logged out successfully"
    }), 200
