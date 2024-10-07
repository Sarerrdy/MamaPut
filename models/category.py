from database import db


class Category(db.Model):
    """
    Category Flask-SQLAlchemy Model

    Represents objects contained in the categories table
    """

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    category_url = db.Column(db.String(), nullable=False)

    menus = db.relationship("Menu", back_populates="category")

    def __repr__(self):
        return (
            f"**Category** "
            f"category_id: {self.category_id} "
            f"name: {self.name} "
            f"category_url: {self.category_url} "
            f"**Category** "
        )
