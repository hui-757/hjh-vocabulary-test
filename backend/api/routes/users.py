#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理路由（管理员权限）
"""

from flask import Blueprint, request, jsonify
from api.routes.auth import get_current_user
from api.models import user_manager

users_bp = Blueprint('users', __name__, url_prefix='/api')


def _get_current_admin_level():
    """获取当前用户的管理员级别"""
    user = get_current_user(request)
    if not user:
        return None
    # 兼容旧数据：没有admin_level的admin视为一级
    level = user.get("admin_level")
    if level is None and user.get("role") == "admin":
        level = 1
    return level


@users_bp.route('/users', methods=['GET'])
def get_users():
    """获取所有用户列表（管理员权限）"""
    current = get_current_user(request)
    if not current:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    # 兼容旧数据：没有admin_level的admin视为一级
    level = current.get("admin_level")
    if level is None and current.get("role") == "admin":
        level = 1
    
    if current.get("role") != "admin":
        return jsonify({"success": False, "message": "无权访问"}), 403
    
    users = user_manager.get_all_users()
    return jsonify({"success": True, "users": users})


@users_bp.route('/users/<user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    """修改用户角色（仅一级管理员）"""
    current = get_current_user(request)
    if not current:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    # 兼容旧数据
    my_level = current.get("admin_level")
    if my_level is None and current.get("role") == "admin":
        my_level = 1
    
    if my_level != 1:
        return jsonify({"success": False, "message": "仅一级管理员可操作"}), 403
    
    data = request.get_json() or {}
    new_role = data.get("role", "user")
    new_level = data.get("admin_level")
    
    # 只允许设为普通用户或二级管理员
    if new_role == "admin" and new_level not in [1, 2]:
        return jsonify({"success": False, "message": "无效的管理员级别"}), 400
    if new_role == "user":
        new_level = None
    
    user, error = user_manager.update_user_role(
        user_id, new_role, new_level, updater_level=my_level
    )
    
    if error:
        return jsonify({"success": False, "message": error}), 400
    
    return jsonify({"success": True, "user": user})
