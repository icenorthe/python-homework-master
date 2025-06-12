from app.dao.order_dao import OrderDao
from app.dao.product_dao import ProductDao
from app.dao.user_dao import UserDao
from app.dao.product_image_dao import ProductImageDao
from app.common.exception import BusinessException
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename


class OrderService:
    def __init__(self):
        self.order_dao = OrderDao()
        self.product_dao = ProductDao()
        self.user_dao = UserDao()
        self.product_image_dao = ProductImageDao()

    def create_order(self, order_data):
        product = self.product_dao.find_by_id(order_data.get("product_id"))
        if not product:
            raise BusinessException("商品不存在")

        if product.user_id != order_data.get("seller_id"):
            raise BusinessException("卖家信息不匹配")

        order_data["status"] = "pending"
        order_data["created_at"] = datetime.now()

        return self.order_dao.insert(order_data)

    def update_order_status(self, order_id, status):
        order = self.order_dao.select_by_id(order_id)
        if not order:
            raise BusinessException("订单不存在")

        return self.order_dao.update_status(order_id, status)

    def delete_order(self, order_id):
        return self.order_dao.delete_by_id(order_id)

    def get_order_detail(self, order_id):
        order = self.order_dao.select_detail_by_id(order_id)
        return order.to_dict() if order else None

    def get_buyer_orders(self, buyer_id, status=None):
        orders = self.order_dao.select_by_buyer_id(buyer_id, status)
        return [o.to_dict() for o in orders]

    def get_seller_orders(self, seller_id, status=None):
        orders = self.order_dao.select_by_seller_id(seller_id, status)
        return [o.to_dict() for o in orders]