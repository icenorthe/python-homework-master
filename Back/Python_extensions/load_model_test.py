import onnxruntime as ort

def test_model_load():
    try:
        sess = ort.InferenceSession("models/minilm-l6-v2/minilm-l6-v2.onnx")
        print("✅ 模型加载成功！输入维度:", sess.get_inputs()[0].shape)
    except Exception as e:
        print("❌ 加载失败:", str(e))

if __name__ == "__main__":
    test_model_load()