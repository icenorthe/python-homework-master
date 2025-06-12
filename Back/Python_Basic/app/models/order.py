from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled'), default='pending', nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def  to_dict(self):
        return {
            'id': self.id,
            'productId': self.product_id,
            'buyerId': self.buyer_id,
            'sellerId': self.seller_id,
            'phone': self.phone,
            'status': self.status,
            'createdAt': self.created_at
        }