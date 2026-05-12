#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel转JSON工具
将Excel表格转换为标准词库JSON文件
"""

import sys
import os

# 添加backend目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, BACKEND_DIR)

import pandas as pd
import numpy as np
from config.settings import (
    WORD_BANK_DIR,
    WORD_BANK_FILE,
    SUPPORTED_EXTENSIONS,
    COLUMN_MAPPING,
    LEVEL_MAPPING
)
from scripts.utils import (
    ensure_directory,
    get_level_from_filename,
    clean_word_data,
    create_word_bank_data,
    find_files,
    write_json_file
)


def is_valid_value(value):
    """检查值是否有效（排除NaN、None、空字符串）"""
    if value is None:
        return False
    if isinstance(value, float) and np.isnan(value):
        return False
    return bool(str(value).strip())


def process_excel_file(filepath):
    """
    处理单个Excel文件
    
    Args:
        filepath: Excel文件路径
        
    Returns:
        list: 提取的单词列表
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(filepath)
        
        # 重命名列
        df = df.rename(columns=COLUMN_MAPPING)
        
        # 检查必要列
        if 'word' not in df.columns or 'mean' not in df.columns:
            print(f"警告: 文件 {os.path.basename(filepath)} 缺少必要的列（需要'word'和'mean'列）")
            return []
        
        # 提取级别
        level = get_level_from_filename(os.path.basename(filepath), LEVEL_MAPPING)
        
        # 处理数据
        words = []
        for _, row in df.iterrows():
            # 跳过空值/NaN行
            if not is_valid_value(row['word']) or not is_valid_value(row['mean']):
                continue
            
            word_data = {
                'word': row['word'],
                'mean': row['mean'],
                'level': level
            }
            
            cleaned = clean_word_data(word_data)
            if cleaned:
                words.append(cleaned)
        
        print(f"处理完成: {os.path.basename(filepath)} - {len(words)} 个单词")
        return words
        
    except Exception as e:
        print(f"错误: 处理文件 {os.path.basename(filepath)} 时出错: {e}")
        return []


def main():
    """主函数"""
    print("=" * 50)
    print("Excel转JSON工具")
    print("=" * 50)
    
    # 确保目录存在
    ensure_directory(WORD_BANK_DIR)
    
    # 查找Excel文件
    excel_files = find_files(WORD_BANK_DIR, SUPPORTED_EXTENSIONS)
    
    if not excel_files:
        print(f"错误: 未在 '{WORD_BANK_DIR}' 目录中找到Excel文件")
        print("请将Excel文件放在该目录中，支持格式: .xlsx, .xls")
        return 1
    
    print(f"\n找到 {len(excel_files)} 个Excel文件:")
    for file in excel_files:
        print(f"  - {os.path.basename(file)}")
    
    # 处理所有文件
    print("\n开始处理...")
    all_words = []
    for file in excel_files:
        words = process_excel_file(file)
        all_words.extend(words)
    
    if not all_words:
        print("\n错误: 未从任何文件中提取到有效单词")
        return 1
    
    # 生成词库数据
    word_bank_data = create_word_bank_data(all_words)
    
    # 保存JSON文件
    try:
        write_json_file(WORD_BANK_FILE, word_bank_data)
        
        print(f"\n成功生成词库文件: {WORD_BANK_FILE}")
        print(f"  - 处理文件数: {len(excel_files)}")
        print(f"  - 有效单词数: {len(all_words)}")
        print(f"\n提示: 运行 'python backend/scripts/update_word_bank.py' 可更新单词级别")
        return 0
        
    except Exception as e:
        print(f"\n错误: 保存词库文件时出错: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
