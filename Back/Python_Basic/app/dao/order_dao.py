from app.models.order import Order
from app.extensions import db
from sqlalchemy.orm import joinedload
from datetime import datetime


class OrderDao:
    def insert(self, order_data):
        order = Order(**order_data)
        db.session.add(order)
        db.session.commit()
        return order.order_id

    def update_status(self, order_id, status):
        order = Order.query.get(order_id)
        if order:
            order.status = status
            db.session.commit()
            return True
        return False

    def delete_by_id(self, order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False

    def select_detail_by_id(self, order_id):
        order = Order.query.options(
            joinedload(Order.product),
            joinedload(Order.buyer),
            joinedload(Order.seller)
        ).filter_by(order_id=order_id).first()
        return order

    def select_by_buyer_id(self, buyer_id, status=None):
        query = Order.query.filter_by(buyer_id=buyer_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Order.created_at.desc()).all()

    def select_by_seller_id(self, seller_id, status=None):
        query = Order.query.filter_by(seller_id=seller_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Order.created_at.desc()).all()
