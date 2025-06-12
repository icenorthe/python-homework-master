import faiss
import numpy as np
import os
from PIL import Image
import face_recognition

class FaceRecognizer:
    def __init__(self):
        # 无需模型路径，使用face_recognition内置模型
        pass



    @staticmethod
    def encode(image: Image.Image) -> np.ndarray:
        """生成人脸特征向量"""
        # 转换为numpy数组
        img_array = np.array(image)

        # 检测人脸并编码
        encodings = face_recognition.face_encodings(img_array)

        if len(encodings) == 0:
            raise ValueError("未检测到人脸")

        return encodings[0]  # 返回第一个检测到的人脸
