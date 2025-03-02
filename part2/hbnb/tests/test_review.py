import unittest
from app import create_app

# Global vaiarble to keep UUID
GLOBAL_USER_ID = None
GLOBAL_PLACE_ID = None


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Only create user and place if they not exist
        if GLOBAL_USER_ID is None or GLOBAL_PLACE_ID is None:
            self.create_user_and_place()

    def create_user_and_place(self):
        """
        Creating a new user and a new place

        We need to create a user and a place
        to be able to create a review
        """
        global GLOBAL_USER_ID, GLOBAL_PLACE_ID

        # Create a user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Luke",
            "last_name": "Skywalker",
            "email": "luke@starwars.com"
        })
        print("\nUser creation response:", response.json)
        self.assertEqual(response.status_code, 201)

        # Get user ID from response
        GLOBAL_USER_ID = response.json['id']

        # Create a place
        response = self.client.post('/api/v1/places/', json={
            "title": "Cloud City",
            "description": "Best cloudy place to stay in Bespin",
            "price": 1000000.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner": GLOBAL_USER_ID
        })
        print("\nPlace creation response:", response.json)
        self.assertEqual(response.status_code, 201)

        # Get place ID from response
        GLOBAL_PLACE_ID = response.json['id']

    def test_create_review_valid_data(self):
        """
        Test creating a new review with valid data
        """
        response = self.client.post('/api/v1/reviews/', json={
            "text": "I lost a hand. Traumatic experience.",
            "rating": 1,
            "place_id": GLOBAL_PLACE_ID,
            "user_id": GLOBAL_USER_ID
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_empty_data(self):
        """
        Test creating a new user with empty data
        """
        response = self.client.post('/api/v1/reviews/', json={})
        self.assertEqual(response.status_code, 400)

    def test_create_review_wrong_UUID(self):
        """
        Test creating a new user with wrong UUID
        """

        response = self.client.post('/api/v1/reviews/', json={
            "text": "I lost a hand. Traumatic experience.",
            "rating": 1,
            "place_id": "12",
            "user_id": "14"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_review_by_ID(self):
        """
        Test getting a review by ID

        Due to the creation of a random UUID for each review, we need to
        create a review first, then retrieve it
        """
        # Create another review
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Dangerous evacuation shaft: "
            "I almost fell into Bespin's atmosphere.",
            "rating": 2,
            "place_id": GLOBAL_PLACE_ID,
            "user_id": GLOBAL_USER_ID
        })
        self.assertEqual(response.status_code, 201)

        # Get ID
        review_id = response.json['id']

        # Get review by ID
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_non_existing_ID(self):
        """
        Test getting a review by non existing ID
        """
        response = self.client.get('/api/v1/reviews/1234567890')
        self.assertEqual(response.status_code, 404)

    def test_retrieve_review_list(self):
        """
        Test retrieving the list of reviews
        """
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        # Print the userlist fort debug
        print(f"\nReviews in memory: {response.json}")

    def test_update_review(self):
        """
        Test updating a existing review

        Get the list of all review,
        Catch the first UUID and update the associated review
        """
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

        first_review = response.json[0]
        review_id = first_review['id']

        before_modification = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        print(f"\nOriginal Review: {before_modification.json}")

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "It wasn't so bad after all !",
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)

        after_modification = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        print(f"\nUpdated Review: {after_modification.json}")

    def test_update_non_existing_review(self):
        """
        Test updating a non-existing review
        """
        response = self.client.put('/api/v1/reviews/1234567890', json={
            "text": "It wasn't so bad after all !",
            "rating": 5
        })
        self.assertEqual(response.status_code, 404)

    def test_update_review_with_invalid_data(self):
        """
        Test updating a review with invalid data

        Catch the first review and this UUID to perform the test
        """
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

        first_review = response.json[0]
        review_id = first_review['id']

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={})
        self.assertEqual(response.status_code, 400)

    def test_delete_review(self):
        """
        Test delete a review

        Catch the first review and this UUID to perform the test
        """
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

        first_review = response.json[0]
        review_id = first_review['id']

        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existing_review(self):
        """
        Test delete a non existing review
        """
        response = self.client.delete('/api/v1/reviews/1234567890')
        self.assertEqual(response.status_code, 404)

    def test_create_review_empty_text(self):
        """
        Test creating a new review with text field empty
        """
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 4,
            "place_id": GLOBAL_PLACE_ID,
            "user_id": GLOBAL_USER_ID
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_non_existing_user(self):
        """
        Test creating a new review with a non existing user
        """
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 4,
            "place_id": GLOBAL_PLACE_ID,
            "user_id": "1234567890"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_non_existing_place(self):
        """
        Test creating a new review with a non existing place
        """
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 4,
            "place_id": "01234567890",
            "user_id": GLOBAL_USER_ID
        })
        self.assertEqual(response.status_code, 400)
