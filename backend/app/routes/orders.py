from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from app.extensions import db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@orders_bp.route("/checkout", methods=["POST"])
@login_required
def checkout():

    try:
        cart_items = db.session.scalars(
            db.select(CartItem)
            .where(CartItem.user_id == current_user.id)
        ).all()

        if not cart_items:
            return jsonify({"error": "Your cart is empty"}), 400

        total = 0
        order = Order(
            user_id=current_user.id,
            total_amount=0,
            status="placed"
        )

        db.session.add(order)
        db.session.flush()

        for cart_item in cart_items:

            product = db.session.execute(
                db.select(Product)
                .where(Product.id == cart_item.product_id)
                .with_for_update()
            ).scalar_one_or_none()

            if not product:
                raise ValueError("A product in your cart no longer exists")

            if cart_item.quantity > product.stock:
                raise ValueError(
                    f"Insufficient stock for {product.name}. "
                    f"Available: {product.stock}"
                )

            subtotal = float(product.price) * cart_item.quantity
            total += subtotal

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=cart_item.quantity
            )

            db.session.add(order_item)
            product.stock -= cart_item.quantity
            db.session.delete(cart_item)

        order.total_amount = round(total, 2)

        db.session.commit()

        return jsonify({
            "message": "Order placed successfully",
            "order": order.to_dict()
        }), 201

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Checkout failed. Please try again."}), 500


@orders_bp.route("/", methods=["GET"])
@login_required
def get_orders():

    orders = db.session.scalars(
        db.select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.id.desc())
    ).all()

    return jsonify({
        "count": len(orders),
        "orders": [order.to_dict() for order in orders]
    }), 200
