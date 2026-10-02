from datetime import datetime, timezone

from app.extensions import db


class CartItem(db.Model):

    __tablename__ = "cart_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship("User", backref="cart_items")

    product = db.relationship("Product")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "product_id",
            name="unique_user_product_cart"
        ),
        db.CheckConstraint(
            "quantity > 0",
            name="positive_cart_quantity"
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "product": self.product.to_dict(),
            "subtotal": round(
                float(self.product.price) * self.quantity,
                2
            ),
            "created_at": self.created_at.isoformat()
        }
