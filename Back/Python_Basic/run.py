from flask import Flask
from app.extensions import db
from app.config.default import Config
from app.routes import register_routes
from flask_cors import CORS
from flask import Flask
from app.common.json_provider import CustomJSONProvider


def create_app():
    app = Flask(__name__)
    # 加载默认配置
    app.config.from_object(Config)
    app.json_provider_class = CustomJSONProvider  # 设置新的 JSON 处理方式,自动调用to_dict
    app.json = app.json_provider_class(app)
    # 初始化数据库等扩展
    db.init_app(app)

    # 注册路由蓝图
    register_routes(app)
    CORS(app, supports_credentials=True)
    # 返回构建完成的应用
    return app


if __name__ == '__main__':
    app = create_app()

    app.run(debug=True, host='0.0.0.0', port=8081)
