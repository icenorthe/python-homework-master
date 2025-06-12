from flask import Blueprint, request
from app.services.order_service import OrderService
from app.common.base_response import BaseResponse

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')
order_service = OrderService()


@order_bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    order = order_service.create_order(data)
    return BaseResponse.success("订单创建成功", order)


@order_bp.route('/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')
    updated_order = order_service.update_order_status(order_id, new_status)
    return BaseResponse.success("订单更新完成", updated_order)


@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order_detail(order_id):
    detail = order_service.get_order_detail(order_id)
    return BaseResponse.success("订单信息获取成功", detail)


@order_bp.route('/buyer/<int:buyer_id>', methods=['GET'])
def get_buyer_orders(buyer_id):
    status = request.args.get('status')
    orders = order_service.get_buyer_orders(buyer_id, status)
    return BaseResponse.success("获取买家订单列表成功", orders)


@order_bp.route('/seller/<int:seller_id>', methods=['GET'])
def get_seller_orders(seller_id):
    status = request.args.get('status')
    orders = order_service.get_seller_orders(seller_id, status)
    return BaseResponse.success("获取卖家订单列表成功", orders)


@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order_service.delete_order(order_id)
    return BaseResponse.success("订单删除成功")