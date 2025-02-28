import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        """
        Test creating a new user with valid data
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        """
        Test creating a new user with invalid data
        """
        response = self.client.post('/api/v1/users/', json={})
        self.assertEqual(response.status_code, 400)

    def test_create_user_preexisting_email(self):
        """
        Test creating a new user with an email that already exists
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_user_by_ID(self):
        """
        Test getting a user by ID

        Due to the creation of a random UUID for each user, we need to
        create a user first, then retrieve it
        """
        # Create user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

        # Get user ID from response
        user_id = response.json['id']

        # Get user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)

    def get_user_by_invalid_ID(self):
        """
        Test getting a user by an invalid ID
        """
        response = self.client.get('/api/v1/users/1234567890')
        self.assertEqual(response.status_code, 404)

    def test_retrieve_user_list(self):
        """
        Test retrieving the list of users
        """
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

        # Print the userlist fort debug
        print(f"Users in memory: {response.json}")

    def test_update_a_user(self):
        """
        Test updating a existing user

        Due to the creation of a random UUID for each user, we need to
        create a user first, then retrieve it
        """
        # Create user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Anakin",
            "last_name": "Skywalker",
            "email": "anakin.skywalker@starwars.com"
        })
        self.assertEqual(response.status_code, 201)

        # UUID extraction
        user_id = response.json["id"]

        # Get user by ID
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Darth",
            "last_name": "Vader",
            "email": "darth.vader@starwars.com"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_a_non_existing_user(self):
        """
        Test updating a non existing user
        """

        response = self.client.put('/api/v1/users/1234567890', json={
            "first_name": "Gial",
            "last_name": "Ackbar",
            "email": "its_a_trap@starwars.com"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_a_user_with_invalid_data(self):
        """
        Test updating a existing user with invalid data

        Due to the creation of a random UUID for each user, we need to
        create a user first, then retrieve it
        """
        # Create user
        create_user = self.client.post('/api/v1/users/', json={
            "first_name": "Anakin",
            "last_name": "Skywalker",
            "email": "anakin.skywalker@starwars.com"
        })
        self.assertEqual(create_user.status_code, 201)

        # UUID extraction
        user_id = create_user.json["id"]

        # Get user by ID
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "color": "Blue",
        })
        self.assertEqual(response.status_code, 400)

    def test_user_first_name_validation_len(self):
        """
        Test creating a new user with a very long first_name (> 50 char)
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Orn Free Taa the Twi'lek Senator of "
                          "Ryloth and Coruscant",
            "last_name": "Doe",
            "email": "email@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_user_last_name_validation_len(self):
        """
        Test creating a new user with a very long last_name (> 50 char)
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Orn Free Taa the Twi'lek Senator of "
                         "Ryloth and Coruscant",
            "email": "email@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_user_email_validation(self):
        """
        Test creating an invalid email
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "1234567890"
        })
        self.assertEqual(response.status_code, 400)

    def test_user_first_name_validation_string(self):
        """
        Test creating a new user with a non-string first_name
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": 1234567890,
            "last_name": "Doe",
            "email": "email@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_user_last_name_validation_string(self):
        """
        Test creating a new user with a non-string last_name
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": 1234567890,
            "email": "email@example.com"
        })
        self.assertEqual(response.status_code, 400)
