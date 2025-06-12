import os
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

# 设置代理（根据实际需要）
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# 定义模型名称和保存目录
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model_dir = "model_2"
os.makedirs(model_dir, exist_ok=True)

# 加载并保存分词器
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(model_dir)

# 加载模型并包装
model = AutoModel.from_pretrained(model_name)
model.eval()


class WrappedModel(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask):
        return self.model(input_ids, attention_mask).last_hidden_state


wrapped_model = WrappedModel(model)

# 准备dummy输入
dummy_text = "这是一段测试文本"
dummy_inputs = tokenizer(
    dummy_text,
    return_tensors="pt",
    padding="max_length",
    max_length=256,
    truncation=True
)

# 导出ONNX（关键修改点）
onnx_model_path = os.path.join(model_dir, "minilm-l6-v2.onnx")
torch.onnx.export(
    wrapped_model,
    args=(dummy_inputs["input_ids"], dummy_inputs["attention_mask"]),
    f=onnx_model_path,
    input_names=["input_ids", "attention_mask"],
    output_names=["last_hidden_state"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "seq_len"},
        "attention_mask": {0: "batch_size", 1: "seq_len"},
        "last_hidden_state": {0: "batch_size", 1: "seq_len"}
    },
    opset_version=14,  # 必须≥14
    do_constant_folding=True,
    export_params=True
)

print(f"✅ ONNX模型导出成功: {onnx_model_path}")