"""
通用工具函数模块
提供项目中共享的辅助函数
"""

import os
import json
from datetime import datetime


def ensure_directory(path):
    """确保目录存在，不存在则创建"""
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    elif not os.path.isdir(path):
        raise NotADirectoryError(f"路径存在但不是目录: {path}")
    return False


def read_json_file(filepath):
    """
    安全读取JSON文件
    
    Args:
        filepath: JSON文件路径
        
    Returns:
        dict: 解析后的JSON数据
        
    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON格式错误
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # 清理控制字符（保留换行、制表符等空白字符）
        content = ''.join(char for char in content if ord(char) >= 32 or char in '\n\r\t')
        content = content.strip()
        
    return json.loads(content)


def write_json_file(filepath, data, indent=2):
    """
    安全写入JSON文件
    
    Args:
        filepath: 输出文件路径
        data: 要写入的数据
        indent: 缩进空格数
    """
    # 确保目录存在
    directory = os.path.dirname(filepath)
    if directory:
        ensure_directory(directory)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def get_timestamp():
    """获取当前ISO格式时间戳"""
    return datetime.now().isoformat()


def get_level_from_filename(filename, level_mapping):
    """
    从文件名提取级别
    
    Args:
        filename: 文件名
        level_mapping: 级别映射字典
        
    Returns:
        str: 识别到的级别，未识别返回'其他'
    """
    filename_lower = filename.lower()
    for key, level in level_mapping.items():
        if key in filename_lower:
            return level
    return '其他'


def validate_word_data(word_data):
    """
    验证单词数据是否有效
    
    Args:
        word_data: 单词数据字典
        
    Returns:
        bool: 是否有效
    """
    return (
        isinstance(word_data, dict)
        and word_data.get('word')
        and word_data.get('mean')
        and str(word_data['word']).strip()
        and str(word_data['mean']).strip()
    )


def clean_word_data(raw_data):
    """
    清理和标准化单词数据
    
    Args:
        raw_data: 原始单词数据
        
    Returns:
        dict: 清理后的数据，无效返回None
    """
    if not validate_word_data(raw_data):
        return None
    
    return {
        'word': str(raw_data['word']).strip(),
        'mean': str(raw_data['mean']).strip(),
        'level': raw_data.get('level', '其他')
    }


def create_word_bank_data(words, timestamp=None):
    """
    创建标准格式的词库数据
    
    Args:
        words: 单词列表
        timestamp: 生成时间戳
        
    Returns:
        dict: 标准格式的词库数据
    """
    return {
        'words': words,
        'generated_at': timestamp or get_timestamp(),
        'total_words': len(words)
    }


def get_file_extension(filename):
    """获取文件扩展名（小写）"""
    return os.path.splitext(filename)[1].lower()


def find_files(directory, extensions):
    """
    查找目录中指定扩展名的文件
    
    Args:
        directory: 搜索目录
        extensions: 扩展名列表
        
    Returns:
        list: 匹配的文件路径列表
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for filename in os.listdir(directory):
        if get_file_extension(filename) in extensions:
            files.append(os.path.join(directory, filename))
    
    return sorted(files)
