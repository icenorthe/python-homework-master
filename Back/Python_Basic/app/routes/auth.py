from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.dto.login_dto import LoginDto
from app.dto.register_dto import RegisterDto
from app.common.base_response import BaseResponse
import base64

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        print("执行注册")
        username = request.form.get('username')
        password = request.form.get('password')
        image_file = request.files.get('image')

        if not username or not password or not image_file:
            return BaseResponse.validate_failed('参数不完整')

        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        dto = RegisterDto(username=username, password=password, image=base64_image)

        print(f"用户名: {username}")
        print(f"Base64图片前50字符: {base64_image[:50]}")

        auth_service.register(dto)
        return BaseResponse.success("注册成功")

    except Exception as e:
        return BaseResponse.error(500, f"注册失败: {str(e)}")


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        print("执行登录")
        json_data = request.get_json()
        dto = LoginDto(**json_data)
        user = auth_service.login(dto)
        return BaseResponse.success("登录成功", user.to_dict())
    except Exception as e:
        return BaseResponse.error(401, str(e))


@auth_bp.route('/face_login', methods=['POST'])
def face_login():
    try:
        image_file = request.files.get('face_image')

        if image_file is None:
            return BaseResponse.validate_failed("请上传人脸图像")

        content_type = image_file.content_type
        if not content_type or not content_type.startswith('image/'):
            return BaseResponse.error(400, "图片格式不支持")

        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        user = auth_service.login_by_face(base64_image)
        return BaseResponse.success(f"登录成功 欢迎回来{user.username}", user.to_dict())
    except Exception as e:
        return BaseResponse.error(401, f"登录失败: {str(e)}")
