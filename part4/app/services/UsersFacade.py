from app.models.user import User
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository
import re
from flask_bcrypt import Bcrypt
from app.extensions import db
from flask_bcrypt import check_password_hash

bcrypt = Bcrypt()

def is_valid_email(email):
    """Vérifie si l'email est valide avec une regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$'
    return re.match(email_regex, email) is not None

class UsersFacade():
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)

    def hash_password(self, password):
        """Hache le mot de passe avec Bcrypt"""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def create_user(self, user_data):
        """Crée un utilisateur avec un mot de passe haché déjà reçu"""
        email = user_data.get("email")

        if not is_valid_email(email):
            return None  # Rejette l'email invalide

        if self.get_user_by_email(email):
            return None  # L'email existe déjà

        password_hashed = user_data.pop('password', None)  # 🔹 Déjà haché en amont
        if not password_hashed:
            return None  # Mot de passe obligatoire

        print(f"✅ Mot de passe déjà haché reçu : {password_hashed}")  # ✅ Debug

        user = User(**user_data)
        user.password = password_hashed  # 🔹 On stocke le hash tel quel

        self.user_repo.add(user)  # 🔹 Ajout en base
        db.session.commit()  # 🔹 Commit SQLAlchemy

        stored_user = self.get_user_by_email(email)
        print(f"📌 Mot de passe APRÈS insertion en DB : {stored_user.password}")  # ✅ Debug

        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve user by email."""
        return User.query.filter_by(email=email).first()

    def get_all_users(self):
        """Récupérer tous les utilisateurs."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None  # 🔹 Ensure this results in a `404`

        for key, value in user_data.items():
            setattr(user, key, value)

        self.user_repo.update(user.id, user_data)
        return user


    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    def verify_password(self, user, password):
        """Verify if the provided password matches the stored hashed password."""
        if not user:
            return False
        return check_password_hash(user.password, password)

    def authenticate_user(self, email, password):
        """Authenticate user and return user object if credentials are valid."""
        user = self.get_user_by_email(email)
        if user and self.verify_password(user, password):
            return user
        return None