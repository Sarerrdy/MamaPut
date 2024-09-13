from database import db


class Cart(db.Model):
    """
    Cart Flask-SQLAlchemy Model

    Represents objects contained in the Cart table
    """

    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    user = db.relationship("User", back_populates="cart", uselist=False)

    def __repr__(self):
        return (
            f"**Cart** "
            f"cart_id: {self.cart_id} "
            f"date_created: {self.date_created} "
            f"user_id: {self.user_id}"
            f"**Cart** "
        )
