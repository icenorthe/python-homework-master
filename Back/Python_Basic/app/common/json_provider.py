from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        return super().default(obj)

    def dumps(self, obj, **kwargs):
        kwargs.setdefault("ensure_ascii", False)  # ✅ 保留中文字符
        return super().dumps(obj, **kwargs)
