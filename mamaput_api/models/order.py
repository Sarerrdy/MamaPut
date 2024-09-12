from database import db
from models.menu_order import MenuOrder


class Order(db.Model):
    """
    Order Flask-SQLAlchemy Model

    Represents objects contained in the order table
    """

    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price = db.Column(db.Integer, nullable=False)
    date_ordered = db.Column(db.DateTime, nullable=False)
    expected_date_of_delivery = db.Column(db.DateTime)
    status = db.Column(db.String(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship("User", back_populates="orders")

    # menu_id = db.Column(db.Integer, db.ForeignKey("menus.menu_id"))
    # menus = db.relationship("Menu", back_populates="orders")

    menus = db.relationship(
        'Menu', secondary=MenuOrder.__table__, back_populates='orders')

    def __repr__(self):
        return (
            f"**Order** "
            f"order_id: {self.id} "
            f"total_price: {self.total_price} "
            f"date_ordered: {self.date_ordered}"
            f"expected_date_of_delivery: {self.expected_date_of_delivery}"
            f"status: {self.status}"
            f"**Order** "
        )
