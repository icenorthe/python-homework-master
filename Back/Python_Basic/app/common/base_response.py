# app/common/base_response.py

import time
from flask import request


class BaseResponse:
    @staticmethod
    def success( message,data=None):
        return {
            "success": True,
            "code": 200,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
            "requestId": BaseResponse._get_request_id(),
            "path": request.path if request else None
        }

    @staticmethod
    def error(code, message):
        return {
            "success": False,
            "code": code,
            "message": message,
            "data": None,
            "timestamp": int(time.time() * 1000),
            "requestId": BaseResponse._get_request_id(),
            "path": request.path if request else None
        }

    @staticmethod
    def validate_failed(message="参数验证失败"):
        return BaseResponse.error(400, message)

    @staticmethod
    def unauthorized(message="未授权"):
        return BaseResponse.error(401, message)

    @staticmethod
    def forbidden(message="禁止访问"):
        return BaseResponse.error(403, message)

    @staticmethod
    def _get_request_id():
        # 你可以从请求头或日志追踪系统中获取真实 requestId
        return request.headers.get("X-Request-ID") if request else None
