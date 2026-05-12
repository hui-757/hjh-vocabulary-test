#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词库统计工具
用于查看词库的统计信息和分布情况
"""

import sys
import os
from collections import Counter

# 添加backend目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, BACKEND_DIR)

from config.settings import WORD_BANK_FILE
from scripts.utils import read_json_file


def analyze_word_bank(filepath):
    """分析词库统计信息"""
    data = read_json_file(filepath)
    words = data.get('words', [])
    
    if not words:
        print("词库为空")
        return
    
    # 基础统计
    total = len(words)
    print(f"\n{'='*50}")
    print(f"词库统计报告")
    print(f"{'='*50}")
    print(f"总单词数: {total}")
    print(f"生成时间: {data.get('generated_at', '未知')}")
    print(f"更新时间: {data.get('updated_at', '未更新')}")
    
    # 级别分布
    level_counter = Counter(w.get('level', '未知') for w in words)
    print(f"\n级别分布:")
    for level, count in level_counter.most_common():
        percentage = (count / total) * 100
        print(f"  {level}: {count} ({percentage:.1f}%)")
    
    # 单词长度统计
    lengths = [len(w['word']) for w in words if w.get('word')]
    if lengths:
        avg_length = sum(lengths) / len(lengths)
        max_length = max(lengths)
        min_length = min(lengths)
        print(f"\n单词长度统计:")
        print(f"  平均长度: {avg_length:.1f}")
        print(f"  最长: {max_length}")
        print(f"  最短: {min_length}")
    
    # 数据完整性检查
    invalid = [w for w in words if not w.get('word') or not w.get('mean')]
    if invalid:
        print(f"\n警告: 发现 {len(invalid)} 条无效数据")
    else:
        print(f"\n数据完整性: 全部有效 [OK]")


def main():
    print("=" * 50)
    print("词库统计工具")
    print("=" * 50)
    
    try:
        analyze_word_bank(WORD_BANK_FILE)
        return 0
    except FileNotFoundError:
        print(f"错误: 未找到词库文件 '{WORD_BANK_FILE}'")
        return 1
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
