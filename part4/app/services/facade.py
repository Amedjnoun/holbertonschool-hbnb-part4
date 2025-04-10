from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Facade class to interact between the application
    and different repositories.
    """
    def __init__(self):
        """
        __init__

        Initialize repositories for user, place, review, and amenity
        """
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

# USER ENDPOINTS
    def create_user(self, user_data):
        """
        create_user

        Create a new user and add it to the user repository
        Hash the password before adding to repo

        Args:
            user_data (dict): A dictionary containing user data

        Returns:
            User: User model representing the newly created user
        """

        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        """
        get_all_users

        Retrivies all users from the repo

        Returns:
            list: A list of all User objects
        """
        return self.user_repo.get_all()

    def get_user(self, user_id):
        """
        get_user

        Get a user by their UUID

        Args:
            user_id (UUID): UUID of the user to retrieve

        Returns:
            User: The user object corresponding to the UUID
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        get_user_by_email

        Get a user by their email

        Args:
            email (string): email of the user to retrieve

        Returns:
            User: The user object corresponding to the mail
        """
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        """
        Update an existing user with new data if it exists

        Args:
            user_id (UUID): UUID
            user_data (dict): Dictionary of data

        Returns:
            user (User): instance of the user
            None: if the user does not exist
        """
        user = self.user_repo.get(user_id)

        if not user:
            return None

        user.update(user_data)
        self.user_repo.update(user, user_data)
        return user

# AMENITY ENDPOINTS
    def create_amenity(self, amenity_data):
        """
        create_amenity

        Create an amenity instance and add it to the repository

        Args:
            amenity_data (dict): A dictionary containing amenity data

        Returns:
            Amenity: The newly created Amenity object
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        get_amenity

        Retrieve an amenity by its ID

        Args:
            amenity_id (UUID): The ID of the amenity to retrieve

        Returns:
            Amenity: The amenity object corresponding to the ID
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        get_all_amenities

        Retrieves all amenities from the repository

        Returns:
            list: A list of all Amenity objects
        """
        amenities = self.amenity_repo.get_all()
        return amenities

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity with new data if it exists

        Args:
            amenity_id (UUID): UUID of the amenity to update
            amenity_data (dict): Dictionary of data to update

        Returns:
            amenity (Amenity): Instance of the updated amenity
            None: If the amenity does not exist
        """
        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            return None

        # Check for duplicate name
        if 'name' in amenity_data:
            existing_amenity = self.amenity_repo.get_by_attribute('name', amenity_data['name'])
            if existing_amenity and existing_amenity[0].id != amenity_id:
                raise ValueError("An amenity with this name already exists.")

        self.amenity_repo.update(amenity_id, amenity_data)  # Pass amenity_id
        return self.amenity_repo.get(amenity_id)  # Return updated amenity

# PLACE ENDPOINTS
    def create_place(self, place_data):
        """
        create_place

        Create a new place and add it to the place repository

        Args:
            place_data (dict): A dictionary containing place data

        Returns:
            Place: Place model representing the newly created place
        """
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        get_place

        Retrieve a place by its ID

        Args:
            place_id (UUID): The ID of the place to retrieve

        Returns:
            Place: The place object corresponding to the ID
        """
        if not place_id:
            return None
        else:
            return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        get_all_places

        Retrieves all places from the repository

        Returns:
            list: A list of all Place objects
        """
        places = self.place_repo.get_all()
        return places

    def update_place(self, place_id, place_data):
        """
        Update an existing place with new data if it exists

        Args:
            place_id (UUID): UUID of the place to update
            place_data (dict): Dictionary of data to update

        Returns:
            place (Place): Instance of the updated place
            None: If the place does not exist
        """
        place = self.place_repo.get(place_id)

        if not place:
            return None

        self.place_repo.update(place_id, place_data)  # Pass place_id
        return self.place_repo.get(place_id)  # Return updated place

# REVIEW ENDPOINTS
    def create_review(self, review_data):
        """
        create_review

        Create a new review and add it to the review repository

        Args:
            review_data (dict): A dictionary containing review data

        Returns:
            Review: Review model representing the newly created review
        """
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        get_review

        Retrieve a review by its ID

        Args:
            review_id (UUID): The ID of the review to retrieve

        Returns:
            Review: The review object corresponding to the ID
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        get_all_reviews

        Retrieves all reviews from the repository

        Returns:
            list: A list of all Review objects
        """
        reviews = self.review_repo.get_all()
        return reviews

    def get_reviews_by_place(self, place_id):
        """
        get_reviews_by_place

        Retrieve all reviews for a specific place

        Args:
            place_id (UUID): The ID of the place to retrieve reviews for

        Returns:
            list: A list of all Review objects for the specified place
        """
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """
        Update an existing review with new data if it exists

        Args:
            review_id (UUID): UUID of the review to update
            review_data (dict): Dictionary of data to update

        Returns:
            review (Review): Instance of the updated review
            None: If the review does not exist
        """
        review = self.review_repo.get(review_id)

        if not review:
            return None

        self.review_repo.update(review_id, review_data)  # Pass review_id
        return self.review_repo.get(review_id)  # Return updated review

    def delete_review(self, review_id):
        """
        delete_review

        Delete a review by its ID

        Args:
            review_id (UUID): The ID of the review to delete

        Returns:
            bool: True if the review was deleted, False otherwise
        """
        return self.review_repo.delete(review_id)
