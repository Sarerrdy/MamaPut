from datetime import datetime, timezone
from database import db


class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey(
        'menus.menu_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone.utc))  # Use timezone-aware datetime
    user_names = db.Column(db.String(255), nullable=False, default='Unknown')

    menu = db.relationship('Menu', back_populates='reviews')
    reviewer = db.relationship('User', back_populates='menu_reviewer')

    def to_dict(self):
        return {
            'review_id': self.review_id,
            'menu_id': self.menu_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'review': self.review,
            'created_at': self.created_at.isoformat(),
            'user_names': self.user_names
        }
