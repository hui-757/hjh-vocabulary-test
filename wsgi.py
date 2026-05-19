import os
import sys
import traceback

# 确保项目根目录在 Python 路径中
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend'))

try:
    from api.app import create_app
    app = create_app()
    print("[OK] Flask app created successfully")
except Exception as e:
    print("[FATAL] Failed to create Flask app:")
    traceback.print_exc()
    raise
