# 文件: app/config/default.py

import os

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

# 上传文件保存路径
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Python_Basic', 'uploads')

# Flask 配置类
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-for-flask-app'

    # 修改为 MySQL 数据库连接 URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:root@localhost:3306/second_hand_trading'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    DEBUG = True
