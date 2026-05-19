import os
import sys

# 计算项目根目录（wsgi.py 在项目根目录）
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 确保 backend 目录在 Python 路径中
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend'))

# 从 backend 导入应用工厂
from api.app import create_app

# 创建 Flask 应用实例
try:
    app = create_app()
except Exception as e:
    import traceback
    print("[FATAL] Failed to create Flask app:")
    traceback.print_exc()
    raise
