import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

class TextEncoder:
    def __init__(self, onnx_path: str):
        self.session = ort.InferenceSession(onnx_path)
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def encode(self, text: str) -> np.ndarray:
        """生成文本向量"""
        # 文本分词
        inputs = self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="np"
        )
        # ONNX推理
        input_ids = inputs["input_ids"].astype(np.int64)
        attention_mask = inputs["attention_mask"].astype(np.int64)
        outputs = self.session.run(
            None,
            {
                "input_ids": input_ids,
                "attention_mask": attention_mask
            }
        )
        # 取[CLS]向量作为句子表示
        return outputs[:, 0, :].squeeze()