from app.models.product_image import ProductImage
from app.extensions import db


class ProductImageDao:
    def insert(self, product_id, image_url):
        image = ProductImage(product_id=product_id, image_url=image_url)
        db.session.add(image)
        db.session.commit()
        return image.image_id

    def delete_by_product_id(self, product_id):
        deleted = ProductImage.query.filter_by(product_id=product_id).delete()
        db.session.commit()
        return deleted

    def find_by_product_id(self, product_id):
        return ProductImage.query.filter_by(product_id=product_id).all()
