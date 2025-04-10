from app.extensions import db
from app.models.BaseModel import BaseModel

class Review(BaseModel):
    """Model for property reviews."""

    # Review content
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', backref='reviews')

    def validate(self):
        """Validate review data."""
        # Text validation
        if not self.text or not self.text.strip():
            raise ValueError("Review text is required")

        # Rating validation
        if not isinstance(self.rating, int) or self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        if not self.place_id:
            raise ValueError("Place ID is required")

        if not self.user_id:
            raise ValueError("User ID is required")

    def to_dict(self):
        """Convert the review to a dictionary."""
        review_dict = super().to_dict()

        # Add user information
        if self.user:
            review_dict['user'] = {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            }

        # Remove sensitive information
        if 'place_id' in review_dict:
            del review_dict['place_id']
        if 'user_id' in review_dict:
            del review_dict['user_id']

        return review_dict

    @staticmethod
    def create_review(data, user_id, place_id):
        """Create a new review."""
        review = Review(
            text=data['text'],
            rating=int(data['rating']),
            user_id=user_id,
            place_id=place_id
        )
        review.validate()
        review.save()
        return review

    def update_from_dict(self, data):
        """Update the review from a dictionary."""
        allowed_fields = ['text', 'rating']
        for field in allowed_fields:
            if field in data:
                setattr(self, field, data[field])
        self.validate()
        self.save()

    def __repr__(self):
        """String representation of the review."""
        return f"<Review {self.id} - Rating: {self.rating}/5>"
