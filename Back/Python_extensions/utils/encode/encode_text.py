from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np


class TextEncoder:
    def __init__(self, model_dir: str = "models/minilm-l6-v2/"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.session = ort.InferenceSession(f"{model_dir}/minilm-l6-v2.onnx")
        self.input_details = {inp.name: inp for inp in self.session.get_inputs()}

    def encode(self, text: str, normalize: bool = True) -> np.ndarray:
        # 文本预处理
        inputs = self.tokenizer(
            text,
            padding='max_length',
            max_length=256,
            truncation=True,
            return_tensors='np'
        )

        # 构建输入字典
        feed_dict = {
            'input_ids': inputs['input_ids'].astype(np.int64),
            'attention_mask': inputs['attention_mask'].astype(np.int64)
        }

        # 执行推理
        outputs = self.session.run(None, feed_dict)
        # 提取嵌入并池化 (形状从 [1, 256, 384] -> [1, 384])
        embeddings = outputs[0]
        embeddings = np.mean(embeddings, axis=1)  # 平均池化

        # 归一化处理
        if normalize:
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

        return embeddings[0]