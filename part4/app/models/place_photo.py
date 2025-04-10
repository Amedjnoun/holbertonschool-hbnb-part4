"""Place photo model for property images."""
from app.extensions import db
from app.models.BaseModel import BaseModel

class PlacePhoto(BaseModel):
    """Model for property photos/images."""

    # Photo information
    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)

    # Relationship
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def validate(self):
        """Validate photo data."""
        if not self.filename:
            raise ValueError("Filename is required")

        if not self.url:
            raise ValueError("URL is required")

        if self.caption and len(self.caption) > 255:
            raise ValueError("Caption must be less than 255 characters")

    def to_dict(self):
        """Convert the photo to a dictionary."""
        return {
            'id': self.id,
            'filename': self.filename,
            'url': self.url,
            'caption': self.caption,
            'is_primary': self.is_primary,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def create_photo(data):
        """Create a new photo."""
        photo = PlacePhoto(
            filename=data['filename'],
            url=data['url'],
            caption=data.get('caption'),
            is_primary=data.get('is_primary', False),
            place_id=data['place_id']
        )

        # If this is the primary photo, ensure no other photos for this place are marked as primary
        if photo.is_primary:
            existing_primary = PlacePhoto.query.filter_by(
                place_id=photo.place_id,
                is_primary=True
            ).all()

            for existing in existing_primary:
                existing.is_primary = False
                existing.save()

        # Validate and save
        photo.validate()
        photo.save()
        return photo

    def update_from_dict(self, data):
        """Update the photo from a dictionary."""
        if 'filename' in data:
            self.filename = data['filename']
        if 'url' in data:
            self.url = data['url']
        if 'caption' in data:
            self.caption = data['caption']
        if 'is_primary' in data:
            old_is_primary = self.is_primary
            self.is_primary = data['is_primary']

            # If this is now the primary photo, ensure no other photos for this place are marked as primary
            if not old_is_primary and self.is_primary:
                existing_primary = PlacePhoto.query.filter(
                    PlacePhoto.place_id == self.place_id,
                    PlacePhoto.id != self.id,
                    PlacePhoto.is_primary == True
                ).all()

                for existing in existing_primary:
                    existing.is_primary = False
                    existing.save()

        # Validate and save
        self.validate()
        self.save()

    def __repr__(self):
        """String representation of the photo."""
        return f'<PlacePhoto {self.filename}>'
