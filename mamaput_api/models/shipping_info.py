from database import db


class ShippingInfo(db.Model):
    """
    shipping_info Flask-SQLAlchemy Model

    Represents objects contained in the shipping_info table
    """

    __tablename__ = "shipping_info"

    shipping_info_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)

    shipping_Method = db.Column(db.String(), nullable=False)
    shipping_cost = db.Column(db.Float(precision=2), nullable=False)
    shipping_status = db.Column(db.String(), nullable=False)
    shipped_date = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)
    expected_delivery_date = db.Column(
        db.DateTime, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    order = db.relationship(
        "Order", back_populates="shipping_info", uselist=False)

    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    address = db.relationship(
        "Address", back_populates="shipping_info", uselist=False)

    # def __repr__(self):
    #     return (
    #         f"**ShippingInfo** "
    #         f"shipping_info_id: {self.shipping_info_id} "
    #         f"order_id: {self.order_id} "
    #         f"address_id: {self.address_id}"
    #         f"shipper_id: {self.shipper_id} "
    #         f"shipping_Method: {self.shipping_Method}"
    #         f"shipping_cost: {self.shipping_cost}"
    #         f"shipping_status: {self.shipping_status}"
    #         f"shipped_date: {self.shipped_date}"
    #         f"expected_delivery_date: {self.expected_delivery_date}"
    #         f"**ShippingInfo** "
    #     )
