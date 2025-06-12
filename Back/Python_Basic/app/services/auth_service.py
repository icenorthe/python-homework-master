from app.dao.user_dao import UserDao as UserDAO
from app.models.user import User
from app.common.exception import BusinessException
from app.common.encryption import check_password, encrypt_password
from app.dto.register_dto import RegisterDto as RegisterDTO
from app.dto.login_dto import LoginDto as  LoginDTO
from app.extensions import db
import requests
import json


class AuthService:

    def __init__(self):
        self.user_dao = UserDAO()

    def register(self, dto: RegisterDTO):
        # 检查用户名是否存在
        if self.user_dao.find_by_username(dto.username):
            raise BusinessException("用户名已存在")

        # 保存用户（明文加密）
        user = User(
            username=dto.username,
            password=encrypt_password(dto.password)
        )
        db.session.add(user)
        db.session.commit()

        # 获取用户ID
        user_id = user.user_id

        # 调用Python人脸注册接口
        payload = {
            "id": user_id,
            "image": f"data:image/jpeg;base64,{dto.image}"
        }

        try:
            res = requests.post(
                url="http://127.0.0.1:5000/api/python/register",
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            if res.status_code != 200:
                raise BusinessException(f"人脸注册失败: {res.text}")
        except Exception as e:
            raise BusinessException(f"调用Python注册服务失败: {str(e)}")

    def login(self, dto: LoginDTO) -> User:
        user = self.user_dao.find_by_username(dto.username)
        if not user or not check_password(dto.password, user.password):
            raise BusinessException("用户名或密码错误")
        return user

    def login_by_face(self, base64_image: str) -> User:
        payload = {
            "image": base64_image
        }
        try:
            res = requests.post(
                url="http://127.0.0.1:5000/api/python/login",
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            if res.status_code == 200:
                response_json = res.json()
                if response_json.get("code") == 200:
                    user_id = response_json.get("data", {}).get("id")
                    user = self.user_dao.find_by_id(user_id)
                    if not user:
                        raise BusinessException("用户不存在")
                    return user
                else:
                    raise BusinessException(f"人脸识别失败: {response_json.get('message')}")
            else:
                raise BusinessException(f"识别服务异常: {res.status_code}")
        except Exception as e:
            raise BusinessException(f"人脸登录异常: {str(e)}")
