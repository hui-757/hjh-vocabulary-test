#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理后端 API 服务
Flask 应用入口
"""

import sys
import os

# 将 backend 目录加入路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, BACKEND_DIR)

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from api.routes.auth import auth_bp
from api.routes.users import users_bp
from api.routes.records import records_bp


def create_app():
    """应用工厂"""
    # 计算项目根目录（backend/api/app.py → 上三级到项目根）
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    frontend_dir = os.path.join(project_root, 'frontend')
    
    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "supports_credentials": True
        }
    })
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(records_bp)
    
    # 初始化数据库（SQLite 表结构）
    from api.record_models import init_db
    try:
        init_db()
        print("[OK] Database initialized")
    except Exception as e:
        print(f"[WARN] Database init failed: {e}")
    
    # ==================== 前端静态文件服务 ====================
    
    @app.route('/')
    def serve_root():
        """首页"""
        return send_from_directory(os.path.join(frontend_dir, 'pages'), 'index.html')
    
    @app.route('/pages/<path:filename>')
    def serve_pages(filename):
        """前端页面（records.html, mistakes.html, admin-records.html 等）"""
        return send_from_directory(os.path.join(frontend_dir, 'pages'), filename)
    
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        """CSS 样式"""
        return send_from_directory(os.path.join(frontend_dir, 'css'), filename)
    
    @app.route('/js/<path:filename>')
    def serve_js(filename):
        """JavaScript"""
        return send_from_directory(os.path.join(frontend_dir, 'js'), filename)
    
    @app.route('/data/<path:filename>')
    def serve_data(filename):
        """数据文件（词库 JSON 等）"""
        return send_from_directory(os.path.join(project_root, 'data'), filename)
    
    # ==================== API 健康检查 ====================
    
    @app.route('/api/health')
    def health():
        return jsonify({"status": "ok"})
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("用户管理 API 服务已启动")
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    # 禁用自动重载，避免 Windows 下加载旧代码缓存
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
