from concurrent.futures import ThreadPoolExecutor
import json
from flask import Flask, request, jsonify

from Back.Python_extensions.utils.login.face_login import register_user, login_user

# 初始化Flask应用
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=8)
# 加载配置文件
with open('config/config.json') as f:
    config = json.load(f)


# 人脸识别路由
@app.route('/api/python/register', methods=['POST'])
def register():
    try:
        data = request.json
        future = executor.submit(register_user, data)
        result = future.result()  # 阻塞等待线程返回
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e),
            "data": {}
        })


@app.route('/api/python/login', methods=['POST'])
def login():
    try:
        data = request.json
        future = executor.submit(login_user, data)
        result = future.result()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e),
            "data": {}
        })

#
# # 商品管理路由
# @app.route('/api/python/products', methods=['POST'])
# def add_product():
#     try:
#         data = request.json
#         product_id = int(data['product_id'])
#         description = str(data['description']).strip()
#
#         if product_db.has_id(product_id):
#             return jsonify({
#                 "code": 400,
#                 "message": "商品ID已存在",
#                 "data": {}
#             })
#
#         # 生成文本向量
#         vector = text_encoder.encode(description)
#
#         # 存储数据
#         product_db.add_item(vector, product_id)
#
#         return jsonify({
#             "code": 200,
#             "message": "商品上传成功",
#             "data": {}
#         })
#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "message": str(e),
#             "data": {}
#         })
#
#
# @app.route('/api/python/products', methods=['PUT'])
# def update_product():
#     try:
#         data = request.json
#         product_id = int(data['product_id'])
#         new_description = str(data['description']).strip()
#
#         if not product_db.has_id(product_id):
#             return jsonify({
#                 "code": 404,
#                 "message": "商品不存在",
#                 "data": {}
#             })
#
#         # 更新向量和描述
#         new_vector = text_encoder.encode(new_description)
#         product_db.update_item(new_vector, product_id)
#
#
#         return jsonify({
#             "code": 200,
#             "message": "修改成功",
#             "data": {}
#         })
#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "message": str(e),
#             "data": {}
#         })
#
#
# @app.route('/api/python/products', methods=['DELETE'])
# def delete_product():
#     try:
#         product_id = int(request.json['product_id'])
#
#         if not product_db.has_id(product_id):
#             return jsonify({
#                 "code": 404,
#                 "message": "商品不存在",
#                 "data": {}
#             })
#
#         # 删除数据
#         product_db.delete_item(product_id)
#
#         return jsonify({
#             "code": 200,
#             "message": "删除成功",
#             "data": {}
#         })
#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "message": str(e),
#             "data": {}
#         })
#
#
# @app.route('/api/python/search', methods=['GET'])
# def search_products():
#     try:
#         keyword = request.args.get('keyword', '')
#         threshold = config["search_threshold"]
#
#         # 生成查询向量
#         query_vector = text_encoder.encode(keyword)
#
#         # 执行搜索
#         results = product_db.search(query_vector, top_k=10, threshold=threshold)
#
#         return jsonify({
#             "code": 200,
#             "message": "",
#             "data": {
#                 "product_ids": [int(id) for id in results]
#             }
#         })
#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "message": str(e),
#             "data": {}
#         })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config["port"], debug=True)