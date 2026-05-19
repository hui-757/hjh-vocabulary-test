#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户数据模型层
负责 users.json 的读写与数据操作
"""

import json
import hashlib
import uuid
import os
from datetime import datetime

from config.settings import USERS_FILE, ensure_directory


class UserDataManager:
    """用户数据管理器"""

    def __init__(self):
        self._data = None
        self._ensure_file()

    def _ensure_file(self):
        """确保用户数据文件存在"""
        ensure_directory(os.path.dirname(USERS_FILE))
        if not os.path.exists(USERS_FILE):
            self._save({"users": []})

    def _load(self):
        """加载用户数据"""
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"users": []}

    def _save(self, data):
        """保存用户数据"""
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _get_users(self):
        """获取用户列表（缓存）"""
        if self._data is None:
            self._data = self._load()
        return self._data.get("users", [])

    def _persist(self):
        """持久化当前数据"""
        if self._data is not None:
            self._save(self._data)

    @staticmethod
    def hash_password(password):
        """SHA256 密码哈希"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def get_all_users(self):
        """获取所有用户（脱敏密码）"""
        users = self._get_users()
        return [
            {
                "id": u["id"],
                "username": u["username"],
                "nickname": u.get("nickname", u["username"]),
                "role": u.get("role", "user"),
                "admin_level": u.get("admin_level"),
                "avatar": u.get("avatar", ""),
                "created_at": u.get("created_at", "")
            }
            for u in users
        ]

    def get_user_by_id(self, user_id):
        """按 ID 查找用户"""
        for u in self._get_users():
            if u["id"] == user_id:
                return self._sanitize(u)
        return None

    def get_user_by_username(self, username):
        """按用户名查找用户（含密码，用于验证）"""
        for u in self._get_users():
            if u["username"] == username:
                return u
        return None

    def add_user(self, username, password, nickname=None, role="user", admin_level=None):
        """添加新用户"""
        if self.get_user_by_username(username):
            return None, "用户名已存在"

        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "password": self.hash_password(password),
            "nickname": nickname or username,
            "role": role,
            "admin_level": admin_level,
            "avatar": "",
            "created_at": datetime.now().isoformat()
        }

        if self._data is None:
            self._data = self._load()
        self._data["users"].append(user)
        self._persist()

        return self._sanitize(user), None

    def update_user_role(self, target_id, new_role, new_admin_level=None, updater_level=1):
        """
        修改用户角色
        updater_level: 执行者的一级管理员级别(1或2)
        返回: (user, error_msg)
        """
        if updater_level != 1:
            return None, "仅一级管理员可操作"

        if self._data is None:
            self._data = self._load()

        for user in self._data["users"]:
            if user["id"] == target_id:
                user["role"] = new_role
                user["admin_level"] = new_admin_level
                self._persist()
                return self._sanitize(user), None

        return None, "用户不存在"

    def verify_password(self, username, password):
        """验证用户名密码"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        hashed = self.hash_password(password)
        if user["password"] == hashed:
            return self._sanitize(user)
        return None

    def _sanitize(self, user):
        """脱敏用户数据（移除密码）"""
        return {k: v for k, v in user.items() if k != "password"}
    
    def has_admin(self):
        """检查是否已有一级管理员（兼容旧数据：无admin_level的admin视为一级）"""
        for u in self._get_users():
            if u.get("role") == "admin":
                level = u.get("admin_level")
                # 兼容旧数据：没有admin_level的admin视为一级管理员
                if level is None or level == 1:
                    return True
        return False


# 全局实例
user_manager = UserDataManager()
