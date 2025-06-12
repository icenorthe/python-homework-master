
import bcrypt

def encrypt_password(password: str) -> str:
    # 生成盐并加密密码
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    # 验证密码是否匹配
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
