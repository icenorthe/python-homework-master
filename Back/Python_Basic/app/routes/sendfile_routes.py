from flask import Blueprint, current_app, send_from_directory
from app.config.default import UPLOAD_FOLDER  # ✅ 引入统一配置路径

sendfile_bp = Blueprint('sendfile', __name__)

@sendfile_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_uploaded_file(filename):
    # 直接使用配置中的 UPLOAD_FOLDER
    print(UPLOAD_FOLDER)
    return send_from_directory(UPLOAD_FOLDER, filename)
