#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite错题与测试记录数据模型
负责错题本和测试记录的持久化存储
"""

import sqlite3
import json
import uuid
from datetime import datetime
from config.settings import DB_FILE, DB_DIR, ensure_directory


def get_db_connection():
    """获取数据库连接（自动创建目录和表）"""
    ensure_directory(DB_DIR)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表结构"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # 测试记录表：每次测评的结果
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_records (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                user_name TEXT,
                correct_rate REAL NOT NULL,
                vocabulary_size INTEGER NOT NULL,
                correct_count INTEGER NOT NULL,
                total_answered INTEGER NOT NULL,
                level TEXT,
                wrong_words TEXT,  -- JSON数组 [{word, mean, level}]
                created_at TEXT NOT NULL
            )
        ''')
        
        # 个人错题本：每个用户的错误单词去重记录
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal_mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                word TEXT NOT NULL,
                mean TEXT NOT NULL,
                level TEXT,
                mistake_count INTEGER DEFAULT 1,
                first_time TEXT NOT NULL,
                last_time TEXT NOT NULL,
                UNIQUE(user_id, word)
            )
        ''')
        
        # 全服错误统计：管理记录
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE,
                mean TEXT NOT NULL,
                level TEXT,
                mistake_count INTEGER DEFAULT 1,
                first_time TEXT NOT NULL,
                last_time TEXT NOT NULL
            )
        ''')
        
        conn.commit()
    finally:
        conn.close()


class RecordManager:
    """测试记录与错题管理器"""
    
    @staticmethod
    def save_exam_record(user_id, user_name, result, wrong_answers):
        """
        保存一次测试记录
        result: {correctRate, vocabularySize, correctCount, totalAnswered, level}
        wrong_answers: [{word, correct, level, difficulty}, ...]
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            record_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            # 整理错误单词数据
            wrong_words_data = []
            for wa in wrong_answers:
                wrong_words_data.append({
                    'word': wa.get('word', ''),
                    'mean': wa.get('correct', ''),
                    'level': wa.get('level', '')
                })
            
            # 插入测试记录
            cursor.execute('''
                INSERT INTO exam_records 
                (id, user_id, user_name, correct_rate, vocabulary_size, 
                 correct_count, total_answered, level, wrong_words, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record_id, user_id, user_name,
                float(result.get('correctRate', 0)),
                int(result.get('vocabularySize', 0)),
                int(result.get('correctCount', 0)),
                int(result.get('totalAnswered', 0)),
                result.get('level', ''),
                json.dumps(wrong_words_data, ensure_ascii=False),
                now
            ))
            
            # 更新个人错题本
            for wa in wrong_answers:
                word = wa.get('word', '')
                mean = wa.get('correct', '')
                level = wa.get('level', '')
                
                cursor.execute('''
                    SELECT id, mistake_count FROM personal_mistakes 
                    WHERE user_id = ? AND word = ?
                ''', (user_id, word))
                
                row = cursor.fetchone()
                if row:
                    cursor.execute('''
                        UPDATE personal_mistakes 
                        SET mistake_count = mistake_count + 1, last_time = ?
                        WHERE id = ?
                    ''', (now, row['id']))
                else:
                    cursor.execute('''
                        INSERT INTO personal_mistakes 
                        (user_id, word, mean, level, mistake_count, first_time, last_time)
                        VALUES (?, ?, ?, ?, 1, ?, ?)
                    ''', (user_id, word, mean, level, now, now))
            
            # 更新全服错误统计
            for wa in wrong_answers:
                word = wa.get('word', '')
                mean = wa.get('correct', '')
                level = wa.get('level', '')
                
                cursor.execute('''
                    SELECT id, mistake_count FROM global_mistakes WHERE word = ?
                ''', (word,))
                
                row = cursor.fetchone()
                if row:
                    cursor.execute('''
                        UPDATE global_mistakes 
                        SET mistake_count = mistake_count + 1, last_time = ?
                        WHERE id = ?
                    ''', (now, row['id']))
                else:
                    cursor.execute('''
                        INSERT INTO global_mistakes 
                        (word, mean, level, mistake_count, first_time, last_time)
                        VALUES (?, ?, ?, 1, ?, ?)
                    ''', (word, mean, level, now, now))
            
            conn.commit()
            return record_id, None
        except Exception as e:
            conn.rollback()
            return None, str(e)
        finally:
            conn.close()
    
    @staticmethod
    def get_user_records(user_id, limit=50):
        """获取用户的测试记录列表"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, correct_rate, vocabulary_size, correct_count, 
                       total_answered, level, created_at
                FROM exam_records
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            records = []
            for row in rows:
                records.append({
                    'id': row['id'],
                    'correctRate': row['correct_rate'],
                    'vocabularySize': row['vocabulary_size'],
                    'correctCount': row['correct_count'],
                    'totalAnswered': row['total_answered'],
                    'level': row['level'],
                    'createdAt': row['created_at']
                })
            return records
        finally:
            conn.close()
    
    @staticmethod
    def get_record_detail(record_id, user_id):
        """获取单次测试记录的详情（含错题列表）"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM exam_records 
                WHERE id = ? AND user_id = ?
            ''', (record_id, user_id))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            wrong_words = json.loads(row['wrong_words']) if row['wrong_words'] else []
            return {
                'id': row['id'],
                'correctRate': row['correct_rate'],
                'vocabularySize': row['vocabulary_size'],
                'correctCount': row['correct_count'],
                'totalAnswered': row['total_answered'],
                'level': row['level'],
                'wrongWords': wrong_words,
                'createdAt': row['created_at']
            }
        finally:
            conn.close()
    
    @staticmethod
    def get_personal_mistakes(user_id):
        """获取个人错题本"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT word, mean, level, mistake_count, first_time, last_time
                FROM personal_mistakes
                WHERE user_id = ?
                ORDER BY mistake_count DESC, last_time DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            return [{
                'word': row['word'],
                'mean': row['mean'],
                'level': row['level'],
                'mistakeCount': row['mistake_count'],
                'firstTime': row['first_time'],
                'lastTime': row['last_time']
            } for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def get_personal_mistake_count(user_id):
        """获取个人错题数量"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) as count FROM personal_mistakes WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            return row['count'] if row else 0
        finally:
            conn.close()
    
    @staticmethod
    def get_global_mistakes(limit=100):
        """获取全服错误统计（管理记录）"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT word, mean, level, mistake_count, first_time, last_time
                FROM global_mistakes
                ORDER BY mistake_count DESC, last_time DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            return [{
                'word': row['word'],
                'mean': row['mean'],
                'level': row['level'],
                'mistakeCount': row['mistake_count'],
                'firstTime': row['first_time'],
                'lastTime': row['last_time']
            } for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def get_global_mistake_stats():
        """获取全服错题统计信息"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as total FROM global_mistakes')
            total = cursor.fetchone()['total']
            
            cursor.execute('SELECT SUM(mistake_count) as total FROM global_mistakes')
            total_errors = cursor.fetchone()['total'] or 0
            
            return {'totalWords': total, 'totalErrors': total_errors}
        finally:
            conn.close()
