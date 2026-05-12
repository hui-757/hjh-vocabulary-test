#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试
测试核心工具函数
"""

import sys
import os
import json
import tempfile
import shutil
import unittest

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils import (
    ensure_directory,
    read_json_file,
    write_json_file,
    get_level_from_filename,
    validate_word_data,
    clean_word_data,
    create_word_bank_data,
    find_files
)


class TestUtils(unittest.TestCase):
    """测试工具函数"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.json')

    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ensure_directory(self):
        """测试目录创建"""
        new_dir = os.path.join(self.temp_dir, 'new_folder')
        self.assertTrue(ensure_directory(new_dir))
        self.assertTrue(os.path.exists(new_dir))
        
        # 再次创建应返回False（已存在）
        self.assertFalse(ensure_directory(new_dir))

    def test_read_write_json(self):
        """测试JSON读写"""
        test_data = {'words': [{'word': 'hello', 'mean': '你好'}]}
        
        write_json_file(self.test_file, test_data)
        self.assertTrue(os.path.exists(self.test_file))
        
        read_data = read_json_file(self.test_file)
        self.assertEqual(read_data, test_data)

    def test_read_json_file_not_found(self):
        """测试读取不存在的文件"""
        with self.assertRaises(FileNotFoundError):
            read_json_file(os.path.join(self.temp_dir, 'not_exist.json'))

    def test_get_level_from_filename(self):
        """测试从文件名提取级别"""
        mapping = {'小学': '小学', '初中': '初中'}
        
        self.assertEqual(
            get_level_from_filename('小学词汇.xlsx', mapping), '小学'
        )
        self.assertEqual(
            get_level_from_filename('初中考纲.xlsx', mapping), '初中'
        )
        self.assertEqual(
            get_level_from_filename('其他文件.xlsx', mapping), '其他'
        )

    def test_validate_word_data(self):
        """测试单词数据验证"""
        self.assertTrue(validate_word_data({'word': 'hello', 'mean': '你好'}))
        self.assertFalse(validate_word_data({'word': '', 'mean': '你好'}))
        self.assertFalse(validate_word_data({'word': 'hello'}))
        self.assertFalse(validate_word_data(None))

    def test_clean_word_data(self):
        """测试数据清理"""
        raw = {'word': ' hello ', 'mean': ' 你好 ', 'level': '小学'}
        cleaned = clean_word_data(raw)
        
        self.assertEqual(cleaned['word'], 'hello')
        self.assertEqual(cleaned['mean'], '你好')
        self.assertEqual(cleaned['level'], '小学')
        
        # 无效数据
        self.assertIsNone(clean_word_data({'word': '', 'mean': 'test'}))

    def test_create_word_bank_data(self):
        """测试创建词库数据"""
        words = [{'word': 'a', 'mean': '一'}]
        data = create_word_bank_data(words, '2024-01-01')
        
        self.assertEqual(data['words'], words)
        self.assertEqual(data['total_words'], 1)
        self.assertEqual(data['generated_at'], '2024-01-01')

    def test_find_files(self):
        """测试文件查找"""
        # 创建测试文件
        open(os.path.join(self.temp_dir, 'test1.xlsx'), 'w').close()
        open(os.path.join(self.temp_dir, 'test2.txt'), 'w').close()
        
        files = find_files(self.temp_dir, ['.xlsx'])
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith('test1.xlsx'))


class TestConfig(unittest.TestCase):
    """测试配置"""

    def test_import_settings(self):
        """测试配置可正常导入"""
        from config.settings import (
            WORD_BANK_FILE,
            HIGH_SCHOOL_WORDS_COUNT,
            SUPPORTED_EXTENSIONS,
            COLUMN_MAPPING,
            LEVEL_MAPPING
        )
        
        self.assertIsNotNone(WORD_BANK_FILE)
        self.assertEqual(HIGH_SCHOOL_WORDS_COUNT, 1866)
        self.assertIn('.xlsx', SUPPORTED_EXTENSIONS)
        self.assertIn('词汇', COLUMN_MAPPING)
        self.assertIn('小学', LEVEL_MAPPING)


if __name__ == '__main__':
    unittest.main(verbosity=2)
