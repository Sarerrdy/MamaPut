from database import db


class MenuOrder(db.Model):
    """
    MenuOrder Flask-SQLAlchemy Model

    Represents manay to many relationship between menu and order objects
    """

    __tablename__ = "menu_orders"

    menuorder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.menu_id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"))
