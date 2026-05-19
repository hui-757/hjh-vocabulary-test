#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接层 - 兼容 SQLite（本地开发）和 PostgreSQL（Supabase/Render 生产环境）
"""

import os
import json
import uuid
from datetime import datetime

# 判断使用哪种数据库
DATABASE_URL = os.environ.get('DATABASE_URL', '')
USE_POSTGRES = DATABASE_URL and DATABASE_URL.startswith('postgresql')

if USE_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor
else:
    import sqlite3


def get_db_connection():
    """获取数据库连接"""
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    else:
        from config.settings import DB_FILE, DB_DIR, ensure_directory
        ensure_directory(DB_DIR)
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    """初始化数据库表结构（兼容 SQLite 和 PostgreSQL）"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # 测试记录表
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
                wrong_words TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # 个人错题本
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal_mistakes (
                id SERIAL PRIMARY KEY,
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
        
        # 全服错误统计
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_mistakes (
                id SERIAL PRIMARY KEY,
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    WHERE user_id = %s AND word = %s
                ''', (user_id, word))
                
                row = cursor.fetchone()
                if row:
                    cursor.execute('''
                        UPDATE personal_mistakes 
                        SET mistake_count = mistake_count + 1, last_time = %s
                        WHERE id = %s
                    ''', (now, row[0]))
                else:
                    cursor.execute('''
                        INSERT INTO personal_mistakes 
                        (user_id, word, mean, level, mistake_count, first_time, last_time)
                        VALUES (%s, %s, %s, %s, 1, %s, %s)
                    ''', (user_id, word, mean, level, now, now))
            
            # 更新全服错误统计
            for wa in wrong_answers:
                word = wa.get('word', '')
                mean = wa.get('correct', '')
                level = wa.get('level', '')
                
                cursor.execute('''
                    SELECT id, mistake_count FROM global_mistakes WHERE word = %s
                ''', (word,))
                
                row = cursor.fetchone()
                if row:
                    cursor.execute('''
                        UPDATE global_mistakes 
                        SET mistake_count = mistake_count + 1, last_time = %s
                        WHERE id = %s
                    ''', (now, row[0]))
                else:
                    cursor.execute('''
                        INSERT INTO global_mistakes 
                        (word, mean, level, mistake_count, first_time, last_time)
                        VALUES (%s, %s, %s, 1, %s, %s)
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
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, correct_rate, vocabulary_size, correct_count, 
                       total_answered, level, created_at
                FROM exam_records
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            records = []
            for row in rows:
                records.append({
                    'id': row[0],
                    'correctRate': row[1],
                    'vocabularySize': row[2],
                    'correctCount': row[3],
                    'totalAnswered': row[4],
                    'level': row[5],
                    'createdAt': row[6]
                })
            return records
        finally:
            conn.close()
    
    @staticmethod
    def get_record_detail(record_id, user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM exam_records 
                WHERE id = %s AND user_id = %s
            ''', (record_id, user_id))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            wrong_words = json.loads(row[8]) if row[8] else []
            return {
                'id': row[0],
                'correctRate': row[3],
                'vocabularySize': row[4],
                'correctCount': row[5],
                'totalAnswered': row[6],
                'level': row[7],
                'wrongWords': wrong_words,
                'createdAt': row[9]
            }
        finally:
            conn.close()
    
    @staticmethod
    def get_personal_mistakes(user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT word, mean, level, mistake_count, first_time, last_time
                FROM personal_mistakes
                WHERE user_id = %s
                ORDER BY mistake_count DESC, last_time DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            return [{
                'word': row[0],
                'mean': row[1],
                'level': row[2],
                'mistakeCount': row[3],
                'firstTime': row[4],
                'lastTime': row[5]
            } for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def get_personal_mistake_count(user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM personal_mistakes WHERE user_id = %s
            ''', (user_id,))
            row = cursor.fetchone()
            return row[0] if row else 0
        finally:
            conn.close()
    
    @staticmethod
    def get_global_mistakes(limit=100):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT word, mean, level, mistake_count, first_time, last_time
                FROM global_mistakes
                ORDER BY mistake_count DESC, last_time DESC
                LIMIT %s
            ''', (limit,))
            
            rows = cursor.fetchall()
            return [{
                'word': row[0],
                'mean': row[1],
                'level': row[2],
                'mistakeCount': row[3],
                'firstTime': row[4],
                'lastTime': row[5]
            } for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def get_global_mistake_stats():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM global_mistakes')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(mistake_count) FROM global_mistakes')
            total_errors = cursor.fetchone()[0] or 0
            
            return {'totalWords': total, 'totalErrors': total_errors}
        finally:
            conn.close()
