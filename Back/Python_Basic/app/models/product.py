from app.extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('available', 'sold', 'removed'), default='available', nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 添加级联删除配置
    images = db.relationship(
        'ProductImage',
        backref='product',
        lazy=True,
        cascade="all, delete-orphan",  # 级联删除关联的图片
        passive_deletes=True  # 让数据库处理外键约束
    )

    def to_dict(self):
        return {
            'productId': self.product_id,
            'userId': self.user_id,
            'title': self.title,
            'price': str(self.price),
            'description': self.description,
            'status': self.status,
            'createdAt': self.created_at.isoformat(),
            'images': [image.image_url for image in self.images]
        }