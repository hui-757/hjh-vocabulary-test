#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试记录与错题本路由
"""

from flask import Blueprint, request, jsonify
import json
from api.routes.auth import get_current_user
from api.record_models import RecordManager, init_db

records_bp = Blueprint('records', __name__, url_prefix='/api')

# 注意：init_db() 不再在模块导入时调用，改由 create_app() 显式调用
# init_db()


@records_bp.route('/records', methods=['POST'])
def save_record():
    """保存测试记录（需要登录）"""
    import traceback
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({"success": False, "message": "未登录，请先登录"}), 401
        
        data = request.get_json(force=True) or {}
        result = data.get('result', {})
        wrong_answers = data.get('wrongAnswers', [])
        
        print(f"[DEBUG] user_id={user.get('id')}")
        print(f"[DEBUG] result={json.dumps(result, ensure_ascii=False)}")
        print(f"[DEBUG] wrongAnswers type={type(wrong_answers)}")
        print(f"[DEBUG] wrongAnswers={json.dumps(wrong_answers, ensure_ascii=False)}")
        
        if not result:
            return jsonify({"success": False, "message": "缺少测试结果数据"}), 400
        
        # 确保是列表
        if not isinstance(wrong_answers, list):
            print(f"[WARN] wrongAnswers is not list, got {type(wrong_answers)}")
            wrong_answers = []
        
        record_id, error = RecordManager.save_exam_record(
            user["id"],
            user.get("nickname") or user.get("username", ""),
            result,
            wrong_answers
        )
        
        if error:
            print(f"[ERROR] save_exam_record error: {error}")
            return jsonify({"success": False, "message": f"保存失败: {error}"}), 500
        
        print(f"[DEBUG] saved record_id={record_id}")
        return jsonify({"success": True, "recordId": record_id}), 201
    except Exception as e:
        print(f"[FATAL] save_record exception: {str(e)}")
        traceback.print_exc()
        return jsonify({"success": False, "message": f"服务器内部错误: {str(e)}"}), 500


@records_bp.route('/records', methods=['GET'])
def get_records():
    """获取当前用户的测试记录列表"""
    user = get_current_user(request)
    if not user:
        return jsonify({"success": False, "message": "未登录，请先登录"}), 401
    
    limit = request.args.get('limit', 50, type=int)
    records = RecordManager.get_user_records(user["id"], limit)
    return jsonify({"success": True, "records": records})


@records_bp.route('/records/<record_id>', methods=['GET'])
def get_record_detail(record_id):
    """获取单次测试记录详情（含错题列表）"""
    user = get_current_user(request)
    if not user:
        return jsonify({"success": False, "message": "未登录，请先登录"}), 401
    
    detail = RecordManager.get_record_detail(record_id, user["id"])
    if not detail:
        return jsonify({"success": False, "message": "记录不存在"}), 404
    
    return jsonify({"success": True, "record": detail})


@records_bp.route('/mistakes/personal', methods=['GET'])
def get_personal_mistakes():
    """获取个人错题本"""
    user = get_current_user(request)
    if not user:
        return jsonify({"success": False, "message": "未登录，请先登录"}), 401
    
    mistakes = RecordManager.get_personal_mistakes(user["id"])
    count = RecordManager.get_personal_mistake_count(user["id"])
    return jsonify({"success": True, "mistakes": mistakes, "count": count})


@records_bp.route('/mistakes/global', methods=['GET'])
def get_global_mistakes():
    """获取全服错误统计（仅管理员）"""
    user = get_current_user(request)
    if not user:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    if user.get("role") != "admin":
        return jsonify({"success": False, "message": "无权访问，仅管理员可查看"}), 403
    
    limit = request.args.get('limit', 100, type=int)
    mistakes = RecordManager.get_global_mistakes(limit)
    stats = RecordManager.get_global_mistake_stats()
    return jsonify({"success": True, "mistakes": mistakes, "stats": stats})
