from database import db


class Order_Detail(db.Model):
    """
    Order_Detail Flask-SQLAlchemy Model

    Represents objects contained in the Order_Details table
    """

    __tablename__ = "order_details"

    order_details_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Float(precision=2), nullable=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    menu_id = db.Column(db.Integer, db.ForeignKey("menus.menu_id"))
    menu = db.relationship('Menu', back_populates='orderdetails')
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"))
    order = db.relationship('Order', back_populates='orderdetails')

    def __repr__(self):
        return (
            f"**Order_Details** "
            f"order_details_id: {self.order_details_id} "
            f"quantity: {self.quantity} "
            f"discount: {self.discount}"
            f"menu_id: {self.menu_id}"
            f"order_id: {self.order_id}"
            f"**Order_Details** "
        )
