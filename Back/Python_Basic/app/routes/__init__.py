# 文件: app/routes/__init__.py

from .auth import auth_bp
from .product import product_bp
from .order import order_bp
from .sendfile_routes import sendfile_bp  # 添加这一行

def register_routes(app):
    """
    注册所有蓝图路由
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(sendfile_bp)
