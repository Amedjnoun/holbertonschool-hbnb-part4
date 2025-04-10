from app.models.user import User
from app.extensions import db

class UserRepository:
    def __init__(self):
        self.model = User

    def add(self, user):
        db.session.add(user)
        db.session.commit()

    def get(self, user_id):
        return self.model.query.get(user_id)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_all(self):
        return self.model.query.all()
