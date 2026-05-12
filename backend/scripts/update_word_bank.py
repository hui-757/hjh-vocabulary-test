#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词库更新工具
用于更新词库中单词的级别信息
"""

import sys
import os

# 添加backend目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, BACKEND_DIR)

from config.settings import (
    WORD_BANK_FILE,
    HIGH_SCHOOL_WORDS_COUNT
)
from scripts.utils import (
    read_json_file,
    write_json_file,
    get_timestamp
)


def update_word_levels(words, high_school_count):
    """
    更新单词级别
    将末尾指定数量的单词设为高中级别，其余设为小学级别
    
    Args:
        words: 单词列表
        high_school_count: 高中单词数量
        
    Returns:
        tuple: (更新后的单词列表, 高中单词数, 小学单词数)
    """
    total_words = len(words)
    high_school_count = min(high_school_count, total_words)
    primary_count = total_words - high_school_count
    
    # 重置所有单词级别为小学
    for word in words:
        word['level'] = '小学'
    
    # 将末尾单词设为高中级别
    for i in range(total_words - high_school_count, total_words):
        words[i]['level'] = '高中'
    
    return words, high_school_count, primary_count


def main():
    """主函数"""
    print("=" * 50)
    print("词库级别更新工具")
    print("=" * 50)
    
    # 读取词库文件
    try:
        data = read_json_file(WORD_BANK_FILE)
    except FileNotFoundError:
        print(f"错误: 未找到词库文件 '{WORD_BANK_FILE}'")
        print("请先运行 'python backend/scripts/convert_excel.py' 生成词库文件")
        return 1
    except Exception as e:
        print(f"错误: 读取词库文件时出错: {e}")
        return 1
    
    # 检查数据结构
    if 'words' not in data or not isinstance(data['words'], list):
        print("错误: 词库文件结构不正确，缺少'words'字段")
        return 1
    
    words = data['words']
    total_words = len(words)
    
    print(f"\n当前词库包含 {total_words} 个单词")
    
    # 更新级别
    words, high_count, primary_count = update_word_levels(
        words, HIGH_SCHOOL_WORDS_COUNT
    )
    
    # 更新元数据
    data['words'] = words
    data['total_words'] = total_words
    data['updated_at'] = get_timestamp()
    
    # 保存更新后的词库
    try:
        write_json_file(WORD_BANK_FILE, data)
        
        print(f"\n更新成功!")
        print(f"  - 总单词数: {total_words}")
        print(f"  - 高中级别: {high_count}")
        print(f"  - 小学级别: {primary_count}")
        print(f"\n提示: 现在可以打开 frontend/pages/index.html 开始测评")
        return 0
        
    except Exception as e:
        print(f"\n错误: 保存词库文件时出错: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
