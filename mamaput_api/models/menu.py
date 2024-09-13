from database import db
# from models.menu_order import MenuOrder


class Menu(db.Model):
    """
    Menu Flask-SQLAlchemy Model

    Represents objects contained in the menus table
    """

    __tablename__ = "menus"

    menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(), nullable=False)
    menu_url = db.Column(db.String(), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.category_id'), nullable=False)
    category = db.relationship("Category", back_populates="menus")
    reviews = db.relationship("Review", back_populates="menu")

    # orders = db.relationship(
    #     'Order', secondary=MenuOrder.__table__, back_populates='menus')
    orderdetails = db.relationship(
        'Order_Detail', back_populates='menu')

    def __repr__(self):
        return (
            f"**Menu** "
            f"menu_id: {self.menu_id} "
            f"name: {self.name} "
            f"price: {self.price}"
            f"status: {self.status}"
            f"menu_url: {self.menu_url}"
            f"**Menu** "
        )
