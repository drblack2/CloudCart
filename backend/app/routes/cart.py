from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.cart import CartItem
from app.models.product import Product


cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/api/cart"
)


# ADD PRODUCT TO CART
@cart_bp.route("/", methods=["POST"])
@login_required
def add_to_cart():

    data = request.get_json(silent=True) or {}

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    try:
        product_id = int(product_id)
        quantity = int(quantity)

        if product_id <= 0 or quantity <= 0:
            raise ValueError

    except (TypeError, ValueError):
        return jsonify({
            "error": "Valid product_id and positive quantity are required"
        }), 400

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    cart_item = db.session.scalar(
        db.select(CartItem).where(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product_id
        )
    )

    current_quantity = cart_item.quantity if cart_item else 0
    new_quantity = current_quantity + quantity

    if new_quantity > product.stock:
        return jsonify({
            "error": "Requested quantity exceeds available stock",
            "available_stock": product.stock
        }), 400

    if cart_item:
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        "message": "Product added to cart successfully",
        "cart_item": cart_item.to_dict()
    }), 201


# VIEW CURRENT USER CART
@cart_bp.route("/", methods=["GET"])
@login_required
def get_cart():

    cart_items = db.session.scalars(
        db.select(CartItem).where(
            CartItem.user_id == current_user.id
        ).order_by(CartItem.id.desc())
    ).all()

    total = sum(
        float(item.product.price) * item.quantity
        for item in cart_items
    )

    return jsonify({
        "count": len(cart_items),
        "items": [item.to_dict() for item in cart_items],
        "total": round(total, 2)
    }), 200


# UPDATE CART QUANTITY
@cart_bp.route("/<int:cart_item_id>", methods=["PUT"])
@login_required
def update_cart_item(cart_item_id):

    cart_item = db.session.get(CartItem, cart_item_id)

    if not cart_item or cart_item.user_id != current_user.id:
        return jsonify({
            "error": "Cart item not found"
        }), 404

    data = request.get_json(silent=True) or {}

    try:
        quantity = int(data.get("quantity"))

        if quantity <= 0:
            raise ValueError

    except (TypeError, ValueError):
        return jsonify({
            "error": "Quantity must be a positive integer"
        }), 400

    if quantity > cart_item.product.stock:
        return jsonify({
            "error": "Requested quantity exceeds available stock",
            "available_stock": cart_item.product.stock
        }), 400

    cart_item.quantity = quantity
    db.session.commit()

    return jsonify({
        "message": "Cart quantity updated",
        "cart_item": cart_item.to_dict()
    }), 200


# REMOVE ITEM FROM CART
@cart_bp.route("/<int:cart_item_id>", methods=["DELETE"])
@login_required
def remove_cart_item(cart_item_id):

    cart_item = db.session.get(CartItem, cart_item_id)

    if not cart_item or cart_item.user_id != current_user.id:
        return jsonify({
            "error": "Cart item not found"
        }), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({
        "message": "Item removed from cart successfully"
    }), 200
