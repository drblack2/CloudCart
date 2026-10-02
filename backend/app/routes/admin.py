from functools import wraps

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import func

from app.extensions import db
from app.models import User
from app.models.product import Product
from app.models.order import Order


admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def admin_required(func_view):
    @wraps(func_view)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return func_view(*args, **kwargs)

    return wrapper


@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    total_products = db.session.scalar(
        db.select(func.count(Product.id))
    ) or 0

    total_customers = db.session.scalar(
        db.select(func.count(User.id)).where(User.role == "customer")
    ) or 0

    total_orders = db.session.scalar(
        db.select(func.count(Order.id))
    ) or 0

    revenue = db.session.scalar(
        db.select(func.coalesce(func.sum(Order.total_amount), 0))
        .where(Order.status != "cancelled")
    ) or 0

    low_stock = db.session.scalar(
        db.select(func.count(Product.id)).where(Product.stock <= 5)
    ) or 0

    return jsonify({
        "total_products": total_products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": float(revenue),
        "low_stock": low_stock
    }), 200


@admin_bp.route("/customers", methods=["GET"])
@admin_required
def customers():
    users = db.session.scalars(
        db.select(User)
        .where(User.role == "customer")
        .order_by(User.id.desc())
    ).all()

    return jsonify({
        "count": len(users),
        "customers": [user.to_dict() for user in users]
    }), 200


@admin_bp.route("/orders", methods=["GET"])
@admin_required
def all_orders():
    orders = db.session.scalars(
        db.select(Order).order_by(Order.id.desc())
    ).all()

    result = []

    for order in orders:
        order_data = order.to_dict()
        order_data["customer"] = (
            order.user.to_dict() if order.user else None
        )
        result.append(order_data)

    return jsonify({
        "count": len(result),
        "orders": result
    }), 200


@admin_bp.route("/orders/<int:order_id>/status", methods=["PATCH"])
@admin_required
def update_order_status(order_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status", "").strip().lower()

    allowed_statuses = {
        "placed",
        "processing",
        "shipped",
        "delivered",
        "cancelled"
    }

    if status not in allowed_statuses:
        return jsonify({
            "error": "Invalid order status"
        }), 400

    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.status = status
    db.session.commit()

    return jsonify({
        "message": "Order status updated",
        "order": order.to_dict()
    }), 200
