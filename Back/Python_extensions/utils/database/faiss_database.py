import faiss
import numpy as np
import os
from typing import Union

import faiss
import numpy as np
import os
from typing import Union


class FaissDatabase:
    def __init__(self,
                 dim: int,
                 index_path: str,
                 id_map_path: str,
                 normalize: bool = False,
                 index_type: str = "L2"):
        self.dim = dim
        self.index_path = index_path
        self.id_map_path = id_map_path
        self.normalize = normalize
        self.index_type = index_type
        self.index = self._load_or_create_index()
        self.id_map = self._load_id_map()

    def _load_or_create_index(self) -> faiss.Index:
        """加载或创建索引"""
        if os.path.exists(self.index_path):
            index = faiss.read_index(self.index_path)
            print(f"Loaded existing index of type: {type(index)}")
            return index
        else:
            if self.index_type == "L2":
                print("Creating new L2 index")
                return faiss.IndexFlatL2(self.dim)
            elif self.index_type == "IP":
                print("Creating new IP index")
                return faiss.IndexFlatIP(self.dim)
            else:
                raise ValueError(f"Unsupported index type: {self.index_type}")

    def _load_id_map(self) -> dict:
        """加载ID映射表"""
        if os.path.exists(self.id_map_path):
            return np.load(self.id_map_path, allow_pickle=True).item()
        return {}

    def _preprocess_vector(self, vector: np.ndarray) -> np.ndarray:
        """向量预处理（归一化）"""
        if self.normalize:
            norm = np.linalg.norm(vector)
            if norm == 0:
                raise ValueError("Zero vector cannot be normalized")
            return vector / norm
        return vector

    def add_item(self, vector: np.ndarray, item_id: Union[str, int]):
        """添加向量到数据库"""
        vector = self._preprocess_vector(vector.astype(np.float32))
        self.index.add(vector.reshape(1, -1))
        pos = self.index.ntotal - 1
        self.id_map[pos] = item_id
        self._save()

    def update_item(self, vector: np.ndarray, item_id: Union[str, int]):
        """
        修改向量
        :param vector: 新的向量
        :param item_id: 需要修改的ID
        """
        # 查找ID对应的位置
        pos = None
        for idx, id_val in self.id_map.items():
            if id_val == item_id:
                pos = idx
                break
        if pos is None:
            raise ValueError(f"Item ID {item_id} not found in the database")

        # 预处理向量
        vector = self._preprocess_vector(vector.astype(np.float32)).reshape(1, -1)

        # 替换向量
        self.index.remove_ids(np.array([pos], dtype=np.int64))
        self.index.add(vector)
        self._save()

    def has_id(self, item_id: Union[str, int]) -> bool:
        """检查是否存在指定ID"""
        return item_id in self.id_map.values()
    def delete_item(self, item_id: Union[str, int]):
        """
        删除向量
        :param item_id: 需要删除的ID
        """
        # 查找ID对应的位置
        pos = None
        for idx, id_val in self.id_map.items():
            if id_val == item_id:
                pos = idx
                break
        if pos is None:
            raise ValueError(f"Item ID {item_id} not found in the database")

        # 删除向量
        self.index.remove_ids(np.array([pos], dtype=np.int64))

        # 更新ID映射表
        del self.id_map[pos]
        self._save()

    def search(self,
               query: np.ndarray,
               top_k: int = -1,
               threshold: float = None) -> list:
        """相似性搜索"""
        query = self._preprocess_vector(query.astype(np.float32)).reshape(1, -1)
        if top_k == -1:
            top_k = self.index.ntotal
        distances, indices = self.index.search(query, top_k)

        # 根据索引类型处理阈值
        if threshold is not None:
            if self.index_type == "L2":
                mask = distances[0] < threshold
            else:  # IP
                mask = distances[0] > threshold
            filtered = indices[0][mask]
        else:
            filtered = indices[0]

        return [self.id_map[i] for i in filtered if i in self.id_map]

    def _save(self):
        """持久化存储"""
        faiss.write_index(self.index, self.index_path)
        np.save(self.id_map_path, self.id_map)

# ----------------- 使用示例 -------------------
class TextSearchSystem:
    """文本搜索子系统（基于MiniLM模型）"""
    def __init__(self, model_path: str, db_config: dict):
        self.model = self._load_onnx_model(model_path)
        self.db = FaissDatabase(
            dim=384,  # MiniLM-L6-v2的维度
            index_path=db_config['index_path'],
            id_map_path=db_config['id_map_path'],
            normalize=True,  # 文本向量需要归一化
            index_type="IP"   # 使用内积（余弦相似度）
        )

    @staticmethod
    def _load_onnx_model(path: str):
        """加载ONNX模型（示例需根据实际实现）"""
        # 这里添加具体的模型加载和推理逻辑
        return None

    def encode_text(self, text: str) -> np.ndarray:
        """文本编码（示例需实现实际编码逻辑）"""
        # return self.model.encode(text)
        return np.random.randn(384).astype(np.float32)  # 模拟向量

    def add_product(self, product_id: str, description: str):
        """添加商品"""
        vector = self.encode_text(description)
        self.db.add_item(vector, product_id)

    def search_products(self, keyword: str, top_k=5, threshold=0.7) -> list:
        """商品搜索"""
        query_vec = self.encode_text(keyword)
        return self.db.search(query_vec, top_k, threshold)


# 人脸系统保持原有用法
class FaceRecognitionSystem:
    """人脸识别子系统"""
    def __init__(self, db_config: dict):
        self.db = FaissDatabase(
            dim=128,  # face_recognition的编码维度
            index_path=db_config['index_path'],
            id_map_path=db_config['id_map_path'],
            normalize=False,  # 保持原始L2距离
            index_type="L2"
        )

    def add_face(self, image_path: str, user_id: str):
        """添加人脸（示例需实现实际编码）"""
        # encoding = face_recognition.face_encodings(...)
        encoding = np.random.randn(128).astype(np.float32)
        self.db.add_item(encoding, user_id)

    def identify_face(self, image_path: str, threshold=0.6) -> list:
        """人脸识别"""
        # query_encoding = face_recognition.face_encodings(...)
        query_encoding = np.random.randn(128).astype(np.float32)
        return self.db.search(query_encoding, threshold=threshold)