from database import db


class UserRole(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)  # New primary key
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'roles.role_id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
