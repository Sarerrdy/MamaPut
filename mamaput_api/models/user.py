from database import db


class User(db.Model):
    """
    User Flask-SQLAlchemy Model

    Represents objects contained in the users table
    """

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    join_date = db.Column(db.DateTime,  default=db.func.now(), nullable=True)
    user_url = db.Column(db.String(), nullable=True)
    roles = db.relationship(
        'Role', secondary='user_roles', back_populates='users')
    # roles = db.Column(db.String(), default='User')  # Default role attribute

    addresses = db.relationship(
        "Address", back_populates="user", lazy=True)
    cart = db.relationship("Cart", back_populates="user", uselist=False)
    orders = db.relationship("Order", back_populates="user")
    menu_reviewer = db.relationship(
        "Review", uselist=False, back_populates="reviewer")

    # def __repr__(self):
    #     return (
    #         f"**User** "
    #         f"user_id: {self.user_id} "
    #         f"first_name: {self.first_name} "
    #         f"last_name: {self.last_name}"
    #         f"gender: {self.gender}"
    #         f"email: {self.email}"
    #         f"phone: {self.phone}"
    #         f"join_date: {self.join_date}"
    #         f"user_url: {self.user_id}"
    #         f"**User** "
    #     )
