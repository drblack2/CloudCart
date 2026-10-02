from datetime import datetime, timezone
from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", backref="orders")
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="placed")
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    items = db.relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_amount": float(self.total_amount),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "items": [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    # Snapshot values preserve the purchase details
    product_name = db.Column(db.String(150), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "unit_price": float(self.unit_price),
            "quantity": self.quantity,
            "subtotal": round(float(self.unit_price) * self.quantity, 2)
        }
