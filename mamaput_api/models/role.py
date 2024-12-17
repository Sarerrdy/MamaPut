from database import db


class Role(db.Model):
    """
    Role Flask-SQLAlchemy Model
    Represents roles in the roles table
    """
    __tablename__ = "roles"

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(), unique=True, nullable=False)

    # Define relationship to User model
    users = db.relationship(
        'User', secondary='user_roles', back_populates='roles')

    def save(self):
        db.session.add(self)
        db.session.commit()
