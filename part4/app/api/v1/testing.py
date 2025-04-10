from flask import jsonify, Blueprint
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity
from app.extensions import db
from datetime import datetime, timedelta
import random

# Create testing blueprint
testing_bp = Blueprint('testing', __name__)

@testing_bp.route('/api-status', methods=['GET'])
def api_status():
    """Test endpoint to check API status."""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'api_version': 'v1'
    }), 200

@testing_bp.route('/test-data/generate', methods=['POST'])
def generate_test_data():
    """Generate test data for the application."""
    try:
        # Create test amenities
        amenities = ['WiFi', 'Kitchen', 'Parking', 'Pool', 'AC']
        db_amenities = []
        for name in amenities:
            amenity = Amenity(name=name)
            db.session.add(amenity)
            db_amenities.append(amenity)

        # Create test users
        users = []
        for i in range(3):
            user = User(
                email=f'test{i}@test.com',
                password='test123',
                first_name=f'Test{i}',
                last_name=f'User{i}'
            )
            db.session.add(user)
            users.append(user)

        # Create test places
        places = []
        locations = ['Paris', 'London', 'New York', 'Tokyo', 'Berlin']
        for i in range(5):
            place = Place(
                name=f'Test Place {i}',
                description=f'A lovely test place in {locations[i]}',
                location=locations[i],
                price=random.randint(50, 500),
                owner_id=random.choice(users).id
            )
            # Add random amenities
            for amenity in random.sample(db_amenities, random.randint(1, len(db_amenities))):
                place.amenities.append(amenity)
            db.session.add(place)
            places.append(place)

        # Create test reviews
        for place in places:
            for _ in range(random.randint(1, 3)):
                review = Review(
                    content=f'Test review for {place.name}',
                    rating=random.randint(1, 5),
                    user_id=random.choice(users).id,
                    place_id=place.id
                )
                db.session.add(review)

        db.session.commit()

        return jsonify({
            'message': 'Test data generated successfully',
            'data': {
                'users': len(users),
                'places': len(places),
                'amenities': len(amenities)
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@testing_bp.route('/test-data/clear', methods=['POST'])
def clear_test_data():
    """Clear all test data from the database."""
    try:
        Review.query.delete()
        Place.query.delete()
        User.query.filter(User.email.like('test%@test.com')).delete()
        Amenity.query.delete()
        db.session.commit()

        return jsonify({'message': 'Test data cleared successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
