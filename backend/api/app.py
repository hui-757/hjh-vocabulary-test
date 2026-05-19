#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理后端 API 服务
Flask 应用入口
"""

import sys
import os

# 将项目根目录和 backend 目录加入 Python 路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

# 确保 backend 在 sys.path（兼容本地开发和 Render 部署）
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from api.routes.auth import auth_bp
from api.routes.users import users_bp
from api.routes.records import records_bp


def create_app():
    """应用工厂"""
    # 优先从当前工作目录找项目根
    cwd = os.getcwd()
    project_root = cwd
    frontend_dir = os.path.join(project_root, 'frontend')
    
    # 如果 cwd 下没有 frontend，尝试向上找一级（wsgi.py 在项目根目录启动时 cwd=项目根）
    if not os.path.exists(frontend_dir):
        project_root = os.path.dirname(cwd)
        frontend_dir = os.path.join(project_root, 'frontend')
    
    # 如果还是没有，用 __file__ 的回退
    if not os.path.exists(frontend_dir):
        project_root = PROJECT_ROOT
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
        app.logger.info("[OK] Database initialized")
    except Exception as e:
        app.logger.warning(f"[WARN] Database init failed: {e}")
    
    # ==================== 前端静态文件服务 ====================
    
    @app.route('/')
    def serve_root():
        """首页"""
        pages_dir = os.path.join(frontend_dir, 'pages')
        index_path = os.path.join(pages_dir, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(pages_dir, 'index.html')
        return jsonify({
            "error": "index.html not found",
            "project_root": project_root,
            "frontend_dir": frontend_dir,
            "pages_dir": pages_dir,
            "cwd": os.getcwd(),
            "frontend_exists": os.path.exists(frontend_dir),
            "pages_exists": os.path.exists(pages_dir)
        }), 404
    
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
