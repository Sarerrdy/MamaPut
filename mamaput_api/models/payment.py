from database import db


class Payment(db.Model):
    """
    Payment Flask-SQLAlchemy Model

    Represents objects contained in the Payment table
    """

    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_Method = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
    payment_status = db.Column(db.String(), nullable=False)
    payment_date = db.Column(
        db.DateTime, default=db.func.now(), nullable=True)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    order = db.relationship("Order", back_populates="payment", uselist=False)

    def __repr__(self):
        return (
            f"**Payment** "
            f"payment_id: {self.payment_id} "
            f"order_id: {self.order_id} "
            f"amount: {self.amount}"
            f"payment_Method: {self.payment_Method} "
            f"payment_status: {self.payment_status}"
            f"payment_date: {self.payment_date}"
            f"**Payment** "
        )
