from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select

from app.extensions import db
from app.models.product import Product


products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/api/products"
)


# GET ALL PRODUCTS
@products_bp.route("/", methods=["GET"])
def get_products():

    products = db.session.scalars(
        select(Product).order_by(Product.id.desc())
    ).all()

    return jsonify({
        "count": len(products),
        "products": [product.to_dict() for product in products]
    }), 200


# GET SINGLE PRODUCT
@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify({
        "product": product.to_dict()
    }), 200


# CREATE PRODUCT - ADMIN ONLY
@products_bp.route("/", methods=["POST"])
@login_required
def create_product():

    if current_user.role != "admin":
        return jsonify({
            "error": "Admin access required"
        }), 403

    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock", 0)
    image_url = data.get("image_url")

    if not name or price is None:
        return jsonify({
            "error": "Product name and price are required"
        }), 400

    try:
        price = float(price)
        stock = int(stock)

        if price <= 0 or stock < 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "error": "Price must be positive and stock cannot be negative"
        }), 400

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully",
        "product": product.to_dict()
    }), 201


# UPDATE PRODUCT - ADMIN ONLY
@products_bp.route("/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):

    if current_user.role != "admin":
        return jsonify({
            "error": "Admin access required"
        }), 403

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    data = request.get_json(silent=True) or {}

    if "name" in data:
        name = data["name"].strip()

        if not name:
            return jsonify({
                "error": "Product name cannot be empty"
            }), 400

        product.name = name

    if "description" in data:
        product.description = data["description"]

    if "price" in data:
        try:
            price = float(data["price"])

            if price <= 0:
                raise ValueError

            product.price = price

        except (ValueError, TypeError):
            return jsonify({
                "error": "Price must be positive"
            }), 400

    if "stock" in data:
        try:
            stock = int(data["stock"])

            if stock < 0:
                raise ValueError

            product.stock = stock

        except (ValueError, TypeError):
            return jsonify({
                "error": "Stock cannot be negative"
            }), 400

    if "image_url" in data:
        product.image_url = data["image_url"]

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully",
        "product": product.to_dict()
    }), 200


# DELETE PRODUCT - ADMIN ONLY
@products_bp.route("/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):

    if current_user.role != "admin":
        return jsonify({
            "error": "Admin access required"
        }), 403

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200
