from database import db


class Shipping(db.Model):
    """
    Shipping Flask-SQLAlchemy Model

    Represents objects contained in the Shipping table
    """

    __tablename__ = "shippings"

    shipping_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    shipping_Method = db.Column(db.String(), nullable=False)
    shipping_cost = db.Column(db.Float(precision=2), nullable=False)
    shipping_status = db.Column(db.String(), nullable=False)
    shipped_date = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)
    expected_delivery_date = db.Column(
        db.DateTime, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    order = db.relationship("Order", back_populates="shipping", uselist=False)

    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    address = db.relationship(
        "Address", back_populates="shipping", uselist=False)

    shipper_id = db.Column(db.Integer, db.ForeignKey('shippers.shipper_id'))
    shipper = db.relationship(
        "Shipper", back_populates="shipping", uselist=False)

    def __repr__(self):
        return (
            f"**Shipping** "
            f"shipping_id: {self.shipping_id} "
            f"order_id: {self.order_id} "
            f"address_id: {self.address_id}"
            f"shipper_id: {self.shipper_id} "
            f"shipping_Method: {self.shipping_Method}"
            f"shipping_cost: {self.shipping_cost}"
            f"shipping_status: {self.shipping_status}"
            f"shipped_date: {self.shipped_date}"
            f"expected_delivery_date: {self.expected_delivery_date}"
            f"**Shipping** "
        )
