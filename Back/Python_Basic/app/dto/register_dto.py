# app/dto/register_dto.py

from dataclasses import dataclass

@dataclass
class RegisterDto:
    username: str
    password: str
    image: str  # Base64 编码的图像字符串
