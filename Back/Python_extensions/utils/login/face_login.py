import base64

from PIL import Image
from io import BytesIO

from Back.Python_extensions.utils.database.faiss_database import FaissDatabase
from Back.Python_extensions.utils.encode.encode_face import FaceRecognizer


face_recognizer = FaceRecognizer()
face_db = FaissDatabase(
    dim=128,
    index_path="Back/Python_extensions/data/face_data/face.bin",
    id_map_path="Back/Python_extensions/data/face_data/face_id.npy",
    index_type="L2",
    normalize=False
)
def base64_to_image(image_base64):
    """将Base64字符串转换为PIL图像"""
    try:
        image_data = base64.b64decode(image_base64.split(",")[-1])
        return Image.open(BytesIO(image_data))
    except Exception as e:
        raise ValueError(f"无效的图片格式: {str(e)}")
def register_user(data):
    user_id = int(data['id'])
    image = base64_to_image(data['image'])

    if image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background
    elif image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')

    embedding = face_recognizer.encode(image)

    if face_db.has_id(user_id):
        return {"code": 400, "message": "用户ID已存在", "data": {}}

    face_db.add_item(embedding, user_id)
    print(f"注册成功{user_id}")
    return {"code": 200, "message": "注册成功", "data": {}}


def login_user(data):
    image = base64_to_image(data['image'])

    if image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background
    elif image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')

    embedding = face_recognizer.encode(image)

    results = face_db.search(embedding, top_k=1, threshold=0.5)

    if not results:
        return {"code": 400, "message": "登录失败", "data": {}}
    print( {"id": int(results[0])})
    return {"code": 200, "message": "登录成功", "data": {"id": int(results[0])}}

