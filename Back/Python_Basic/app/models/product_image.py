from app.extensions import db

class ProductImage(db.Model):
    __tablename__ = 'product_images'

    image_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # 和数据库一致

    def to_dict(self):
        return {
            'imageId': self.image_id,
            'productId': self.product_id,
            'imageUrl': self.image_url
        }