from database import db


class Order(db.Model):
    """
    Order Flask-SQLAlchemy Model

    Represents objects contained in the order table
    """

    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price = db.Column(db.Float(precision=2), nullable=False)
    date_ordered = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)
    expected_date_of_delivery = db.Column(db.DateTime)
    status = db.Column(db.String(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship("User", back_populates="orders")

    orderdetails = db.relationship(
        'Order_Detail', back_populates='order')

    payment = db.relationship("Payment", back_populates="order")

    shipping = db.relationship(
        "Shipping", back_populates="order", uselist=False)

    def __repr__(self):
        return (
            f"**Order** "
            f"order_id: {self.order_id} "
            f"total_price: {self.total_price} "
            f"date_ordered: {self.date_ordered}"
            f"expected_date_of_delivery: {self.expected_date_of_delivery}"
            f"status: {self.status}"
            f"**Order** "
        )
