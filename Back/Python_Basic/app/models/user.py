from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)


    def to_dict(self):
        return {
            'userId': self.user_id,
            'username': self.username,
            'password': self.password,
            'createdAt': self.created_at
        }