from app.models.user import User
from app.extensions import db


class UserDao:
    def insert(self, user_data):
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user.user_id

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def find_by_id(self, user_id):
        return User.query.get(user_id)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return 0
        db.session.delete(user)
        db.session.commit()
        return 1

    def update(self, user_id, user_data):
        user = User.query.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        db.session.commit()
        return user
