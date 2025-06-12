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


class ProductService:
    def __init__(self):
        self.product_dao = ProductDao()
        self.product_image_dao = ProductImageDao()

    def add_product(self, product_data, image_files):
        product_data["status"] = "available"
        product_id = self.product_dao.insert(product_data)

        if image_files:
            images = self.save_product_images(image_files, product_id)
            product_data["images"] = images

        product_data["product_id"] = product_id
        return product_data

    def update_product(self, product_id, product_data, image_files):
        product = self.product_dao.find_by_id(product_id)
        if not product or product.user_id != product_data.get("user_id"):
            raise BusinessException("商品不存在或无权修改")

        self.product_dao.update(product_id, product_data)

        if image_files:
            self.product_image_dao.delete_by_product_id(product_id)
            images = self.save_product_images(image_files, product_id)
            product_data["images"] = images

        product_data["product_id"] = product_id
        return product_data

    def delete_product(self, product_id, user_id):
        product = self.product_dao.find_by_id(product_id)
        if not product or product.user_id != user_id:
            raise BusinessException("商品不存在或无权删除")

        self.product_dao.delete(product_id,  user_id)
        self.product_image_dao.delete_by_product_id(product_id)

    def get_product_by_id(self, product_id):
        product = self.product_dao.find_by_id(product_id)
        if not product:
            raise BusinessException("商品不存在")

        product_dict = product.to_dict()
        product_dict["images"] = self.product_image_dao.find_by_product_id(product_id)
        return product_dict

    def get_all_products(self):
        products = self.product_dao.find_all_available()
        result = []
        for p in products:
            p_dict = p.to_dict()
            p_dict["images"] = self.product_image_dao.find_by_product_id(p.product_id)
            result.append(p_dict)
        return result

    def get_user_products(self, user_id):
        products = self.product_dao.find_by_user_id(user_id)
        result = []
        for p in products:
            p_dict = p.to_dict()
            p_dict["images"] = self.product_image_dao.find_by_product_id(p.product_id)
            result.append(p_dict)
        return result

    def search_products(self, keyword):
        products = self.product_dao.search_by_keyword(keyword)
        result = []
        for p in products:
            p_dict = p.to_dict()
            p_dict["images"] = self.product_image_dao.find_by_product_id(p.product_id)
            result.append(p_dict)
        return result

    def save_product_images(self, image_files, product_id):
        saved_images = []
        upload_path = os.path.join(os.getcwd(), "uploads")
        os.makedirs(upload_path, exist_ok=True)

        for image_file in image_files:
            if image_file:
                ext = os.path.splitext(image_file.filename)[1]
                filename = f"{uuid.uuid4().hex}{ext}"
                filepath = os.path.join(upload_path, secure_filename(filename))
                image_file.save(filepath)

                image_url = f"uploads/{filename}"
                self.product_image_dao.insert(product_id, image_url)
                saved_images.append({"product_id": product_id, "image_url": image_url})

        return saved_images
