from app.extensions import db
from app.models.product import Product


class ProductDao:
    def insert(self, product_data):
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()
        return product.product_id

    def update(self, product_id, product_data):
        product = Product.query.get(product_id)
        if not product:
            return None
        for key, value in product_data.items():
            setattr(product, key, value)
        db.session.commit()
        return product

    def delete(self,product_id, user_id):
        """
        删除产品及其关联图片
        :param product_id: 产品ID
        :param user_id: 用户ID(用于验证所有权)
        :return: 成功返回True，失败返回False
        """
        try:
            # 查询产品并验证所有权
            product = Product.query.filter_by(
                product_id=product_id,
                user_id=user_id
            ).first()

            if not product:
                return False

            # 删除产品(级联删除会自动处理关联图片)
            db.session.delete(product)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            # 在实际应用中，你可能需要记录这个错误
            print(f"Error deleting product: {e}")
            return False

    def find_by_id(self, product_id):
        return Product.query.get(product_id)

    def find_all_available(self):
        return Product.query.filter_by(status='available').order_by(Product.created_at.desc()).all()

    def find_by_user_id(self, user_id):
        return Product.query.filter(Product.user_id == user_id, Product.status != 'removed')\
                            .order_by(Product.created_at.desc()).all()

    def search_by_keyword(self, keyword):
        return Product.query.filter(Product.title.ilike(f"%{keyword}%"),
                                    Product.status == 'available').all()
