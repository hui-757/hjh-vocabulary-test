import os
import sys

# 计算项目根目录（wsgi.py 在项目根目录）
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 确保 backend 目录在 Python 路径中
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend'))

# 直接导入全局 app 实例（不是工厂函数）
from api.app import app
