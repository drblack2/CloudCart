from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager

from app.models.product import Product
from app.models.cart import CartItem
from app.models.order import Order, OrderItem

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="customer"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Password verification
    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
