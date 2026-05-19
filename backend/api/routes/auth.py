#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证路由：注册 / 登录 / 登出
"""

from flask import Blueprint, request, jsonify
from api.models import user_manager

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# 内存 Token 存储: {token: user_id}
token_store = {}


def get_current_user(request_obj):
    """从请求头中提取当前用户"""
    auth_header = request_obj.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
        user_id = token_store.get(token)
        if user_id:
            return user_manager.get_user_by_id(user_id)
    return None


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    nickname = data.get('nickname', '').strip()
    role = data.get('role', 'user')
    admin_level = None
    
    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400
    
    if len(password) < 6:
        return jsonify({"success": False, "message": "密码长度至少6位"}), 400
    
    # 第一个注册用户自动设为一级管理员（如果没有一级管理员的话）
    if not user_manager.has_admin():
        role = "admin"
        admin_level = 1
    
    user, error = user_manager.add_user(username, password, nickname, role, admin_level)
    if error:
        return jsonify({"success": False, "message": error}), 409
    
    return jsonify({"success": True, "user": user}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400
    
    user = user_manager.verify_password(username, password)
    if not user:
        return jsonify({"success": False, "message": "用户名或密码错误"}), 401
    
    import uuid
    token = str(uuid.uuid4())
    token_store[token] = user["id"]
    
    return jsonify({"success": True, "user": user, "token": token})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
        token_store.pop(token, None)
    
    return jsonify({"success": True, "message": "已登出"})


@auth_bp.route('/profile', methods=['GET'])
def profile():
    """获取当前登录用户信息"""
    user = get_current_user(request)
    if not user:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    return jsonify({"success": True, "user": user})
