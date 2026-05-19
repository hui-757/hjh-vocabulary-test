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

from flask import Flask, jsonify
from flask_cors import CORS

from api.routes.auth import auth_bp
from api.routes.users import users_bp
from api.routes.records import records_bp


def create_app():
    """应用工厂"""
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
    
    @app.route('/')
    def index():
        return jsonify({"message": "词汇测评系统 API 服务", "version": "1.1.0"})
    
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
