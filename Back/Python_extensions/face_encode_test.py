import json
from Back.Python_extensions.utils.encode.encode_face import FaceRecognizer
from Back.Python_extensions.utils.database.faiss_database import FaissDatabase
from PIL import Image

with open('config/config.json') as f:
    config = json.load(f)

bin_path = config["face_data"]["bin"]
npy_path = config["face_data"]["npy"]

recognizer = FaceRecognizer()
dim = 128
database = FaissDatabase(
    dim=dim,
    index_path=bin_path,
    id_map_path=npy_path,
    index_type="L2",
    normalize=False
)

global test_encode
global konwn_face
def test_encode(img_path,id):
    img = Image.open(img_path)
    # 生成特征向量
    embedding = recognizer.encode(img)
    global test_encode
    test_encode = embedding
    print("向量维度:", embedding.shape)  # 应该显示(128,)
    # 存储到数据库
    database.add_item(embedding, id)

def test_loging(img_path):
    img = Image.open(img_path)
    embedding = recognizer.encode(img)
    global konwn_face
    konwn_face = embedding
    result = database.search(embedding, top_k=1, threshold=0.5)
    print(result)

if __name__ == "__main__":
    test_encode("img.png", 3)
    test_loging("img_1.png")