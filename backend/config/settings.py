"""
项目全局配置文件
集中管理所有硬编码配置，便于维护和修改
"""

import os

# 基础路径配置
# settings.py 位于 backend/config/，项目根目录是 backend/ 的父目录
_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_CONFIG_DIR)
BASE_DIR = os.path.dirname(_BACKEND_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')
WORD_BANK_DIR = os.path.join(DATA_DIR, 'word_bank')

# 词库文件配置
WORD_BANK_FILE = os.path.join(WORD_BANK_DIR, 'word_bank.json')
HIGH_SCHOOL_WORDS_COUNT = 1866

# Excel文件配置
SUPPORTED_EXTENSIONS = ['.xlsx', '.xls']

# 列名映射（支持多种可能的列名）
COLUMN_MAPPING = {
    '词汇': 'word',
    'word': 'word',
    'Word': 'word',
    '译文': 'mean',
    'mean': 'mean',
    'Mean': 'mean',
    '翻译': 'mean',
    '中文': 'mean'
}

# 级别映射配置
LEVEL_MAPPING = {
    '小学': '小学',
    '初中': '初中',
    '高中': '高中',
    '四级': '四级',
    '大学': '四级'
}

# 难度级别词汇基数
LEVEL_BASE_VOCABULARY = {
    '小学': {1: 300, 2: 600, 3: 1000},
    '初中': {1: 1500, 2: 2200, 3: 3000},
    '高中': {1: 4000, 2: 5000, 3: 6000}
}

# 学段权重
LEVEL_WEIGHTS = {
    '小学': 1.25,
    '初中': 1.1,
    '高中': 1.1
}

# 测评配置
EXAM_CONFIG = {
    'total_questions': 50,
    'options_per_question': 6,
    'consecutive_wrong_limit': 4,
    'total_wrong_limit': 7,
    'auto_next_delay': 1000,  # 答对后自动下一题延迟（毫秒）
    'word_bank_timeout': 60000  # 词库加载超时（毫秒）
}

# 单词分布规则（分层抽样）
WORD_DISTRIBUTION = [
    {'level': '小学', 'difficulty': 1, 'count': 4},
    {'level': '小学', 'difficulty': 2, 'count': 6},
    {'level': '小学', 'difficulty': 3, 'count': 6},
    {'level': '初中', 'difficulty': 1, 'count': 6},
    {'level': '初中', 'difficulty': 2, 'count': 6},
    {'level': '初中', 'difficulty': 3, 'count': 6},
    {'level': '高中', 'difficulty': 1, 'count': 6},
    {'level': '高中', 'difficulty': 2, 'count': 6},
    {'level': '高中', 'difficulty': 3, 'count': 4}
]

# 能力等级评定标准
LEVEL_THRESHOLDS = [
    (10, '入门级'),
    (20, '小学水平'),
    (30, '初中水平'),
    (40, '高中水平'),
    (50, '优秀水平')
]

# 学习建议配置
SUGGESTIONS = {
    '入门级': [
        '建议从基础单词开始学习，重点掌握日常生活常用词汇',
        '可以通过背单词APP或词汇书进行系统学习',
        '多听多说，提高单词的实际应用能力',
        '建议每天学习20-30个新单词，并进行复习'
    ],
    '小学水平': [
        '继续巩固基础词汇，尝试学习更多日常用语',
        '可以通过阅读简单的英文故事来扩大词汇量',
        '注意单词的发音和拼写，打好基础',
        '建议每天学习20-30个新单词，并进行复习'
    ],
    '初中水平': [
        '可以开始学习一些专业领域的词汇',
        '通过阅读英文文章和书籍来扩大词汇量',
        '注意单词的搭配和用法，提高语言表达能力',
        '建议每天学习30-40个新单词，并进行复习'
    ],
    '高中水平': [
        '可以学习一些生僻词和专业术语',
        '通过阅读英文原著和学术文章来扩大词汇量',
        '注意单词的辨析和同义词的使用',
        '建议每天学习40-50个新单词，并进行复习'
    ],
    '优秀水平': [
        '可以学习一些古英语和外来词',
        '通过阅读各种类型的英文材料来保持词汇量',
        '注意单词的文化内涵和历史背景',
        '建议每天学习一些新单词，并进行复习'
    ]
}

# 前端CDN资源配置
CDN_RESOURCES = {
    'xlsx': 'https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js'
}
