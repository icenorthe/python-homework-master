import json

from flask import Blueprint, request
from app.services.product_service import ProductService
from app.common.base_response import BaseResponse

product_bp = Blueprint('products', __name__, url_prefix='/api/products')
product_service = ProductService()



def parse_product_dto():
    """从 multipart/form-data 的 files 中解析 productDto 字段"""
    product_dto_file = request.files.get('productDto')
    if not product_dto_file:
        raise ValueError("缺少 productDto 字段")
    try:
        return json.load(product_dto_file)
    except Exception as e:
        raise ValueError(f"productDto 解析失败: {str(e)}")


@product_bp.route('', methods=['POST'])
def add_product():
    try:
        product_data = parse_product_dto()
        images = request.files.getlist('images')
        product = product_service.add_product(product_data, images)
        return BaseResponse.success("商品上传成功", product)
    except ValueError as e:
        return BaseResponse.error(str(e))


@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        product_data = parse_product_dto()
        images = request.files.getlist('images')
        product = product_service.update_product(id, product_data, images)
        return BaseResponse.success("商品修改成功", product)
    except ValueError as e:
        return BaseResponse.error(str(e))

@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    user_id = request.args.get('userId', type=int)
    product_service.delete_product(id, user_id)
    return BaseResponse.success("商品删除成功")


@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = product_service.get_product_by_id(id)
    return BaseResponse.success("商品获取成功", product)


@product_bp.route('', methods=['GET'])
def get_all_products():
    products = product_service.get_all_products()
    return BaseResponse.success("商品列表获取成功", products)


@product_bp.route('/user', methods=['GET'])
def get_user_products():
    user_id = request.args.get('userId', type=int)
    products = product_service.get_user_products(user_id)
    return BaseResponse.success("用户商品列表获取成功", products)


@product_bp.route('/search', methods=['GET'])
def search_products():
    keyword = request.args.get('keyword', '')
    products = product_service.search_products(keyword)
    return BaseResponse.success("搜索成功", products)

