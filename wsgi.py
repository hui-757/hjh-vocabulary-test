import os
import sys

# 确保项目根目录在 Python 路径中
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# 将 backend 目录加入路径
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend'))

from api.app import create_app

# 创建 Flask 应用实例（gunicorn 会使用这个变量）
app = create_app()
