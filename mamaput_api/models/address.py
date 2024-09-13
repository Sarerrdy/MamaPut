from database import db


class Address(db.Model):
    """
    Address Flask-SQLAlchemy Model

    Represents objects contained in the address table
    """

    __tablename__ = "addresses"

    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(), nullable=False)
    town = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    lga = db.Column(db.String(), nullable=False)
    landmark = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship("User", back_populates="addresses")

    shipping = db.relationship(
        "Shipping", back_populates="address", uselist=False)

    def __repr__(self):
        return (
            f"**Address** "
            f"address_id: {self.address_id} "
            f"address: {self.address} "
            f"town: {self.town}"
            f"state: {self.state}"
            f"lga: {self.lga}"
            f"landmark: {self.landmark}"
            f"**Address** "
        )
