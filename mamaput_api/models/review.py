from database import db


class Review(db.Model):
    """
    Review Flask-SQLAlchemy Model

    Represents objects contained in the reviews table
    """

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    has_reviewed = db.Column(db.Boolean, nullable=False)
    date_reviewed = db.Column(db.DateTime, nullable=False)

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.menu_id'))
    menu = db.relationship("Menu", back_populates="reviews")

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    reviewer = db.relationship("User", back_populates="menu_reviewer")

    def __repr__(self):
        return (
            f"**Review** "
            f"review_id: {self.review_id} "
            f"details: {self.details} "
            f"rating: {self.rating}"
            f"revied_status: {self.revied_status}"
            f"date_reviewed: {self.date_reviewed}"
            f"**Review** "
        )
