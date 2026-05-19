# 词汇量测评系统

> 基于网页的分层抽样词汇测试工具，采用工程化架构设计。

## 项目结构

```
vocabulary-test-system/
├── src/                          # 源代码
│   ├── css/                      # 样式文件
│   │   ├── common.css            # 公共样式（CSS变量、工具类、响应式）
│   │   └── index.css             # 测评页面样式
│   ├── js/                       # JavaScript模块
│   │   ├── common.js             # 公共工具函数
│   │   ├── wordBank.js           # 词库加载器类
│   │   └── exam.js               # 测评核心逻辑类
│   └── pages/                    # HTML页面
│       ├── index.html            # 主测评页面
│       └── tools.html            # 词库管理工具
├── scripts/                      # Python工具脚本
│   ├── utils.py                  # 公共工具函数
│   ├── convert_excel.py          # Excel转JSON
│   ├── update_word_bank.py       # 更新词库级别
│   └── stats.py                  # 词库统计
├── config/                       # 配置文件
│   └── settings.py               # 全局配置（路径、常量、规则）
├── data/                         # 数据文件
│   └── word_bank/                # 词库目录
│       ├── word_bank.json        # 主词库文件
│       └── *.xlsx                # Excel源文件
├── tests/                        # 单元测试
│   └── test_core.py              # 核心功能测试
├── index.html                    # 项目入口
├── start_server.bat              # 启动脚本
├── requirements.txt              # Python依赖
├── package.json                  # 项目配置
├── .gitignore                    # Git忽略规则
└── README.md                     # 说明文档
```

## 快速开始

### 方式一：直接打开（仅测评功能）

双击 `index.html` 或在浏览器中打开，即可使用测评功能（无需登录）。

### 方式二：启动完整服务（推荐）

同时启动前端静态服务器 + 后端 API 服务：

```bash
# 双击运行 start_server.bat
# 或手动执行
python backend/api/app.py        # 后端 API (端口 5000)
python -m http.server 8080       # 前端服务 (端口 8080)
```

访问 `http://localhost:8080`

### 方式三：使用npm脚本

```bash
# 启动服务器
npm run start

# 仅启动后端 API
npm run start:api

# 一键启动全部（Windows）
npm run start:all

# 运行测试
npm run test

# 转换Excel词库
npm run convert

# 更新词库级别
npm run update-bank
```

## 词库管理

### 从Excel导入词库

1. 将Excel文件放入 `data/word_bank/` 目录
2. 运行 `python scripts/convert_excel.py`
3. 运行 `python scripts/update_word_bank.py` 更新级别
4. 打开页面开始测评

### 使用网页工具

打开 `src/pages/tools.html`：
- **Excel转JSON**：上传Excel文件，配置级别关键词
- **JSON修复**：修复格式错误，清理无效数据
- **级别修复**：按规则重新分配单词级别

### 查看词库统计

```bash
python scripts/stats.py
```

## 工程化特性

- **目录结构规范**：按功能分离 `src/`, `scripts/`, `config/`, `data/`, `tests/`
- **代码模块化**：提取公共模块，封装类（WordBankLoader, VocabularyExam）
- **配置集中管理**：`config/settings.py` 统一管理常量
- **依赖管理**：`requirements.txt` + `package.json`
- **单元测试**：`tests/test_core.py`
- **响应式设计**：支持移动端访问

## 配置说明

编辑 `config/settings.py` 可自定义：

| 配置项 | 说明 |
|--------|------|
| `WORD_BANK_FILE` | 词库文件路径 |
| `HIGH_SCHOOL_WORDS_COUNT` | 高中级别单词数量 |
| `EXAM_CONFIG` | 测评参数 |
| `WORD_DISTRIBUTION` | 分层抽样规则 |
| `LEVEL_THRESHOLDS` | 能力等级标准 |

## 依赖

- Python 3.6+, pandas, openpyxl, flask, flask-cors
- 现代浏览器（Chrome, Firefox, Edge）

## 用户管理

系统支持两种用户角色：

- **普通用户**：使用测评功能、查看个人资料
- **管理员**：额外拥有用户管理权限

### 使用流程

1. **首页点击「登录/注册」** → 弹窗中可切换登录/注册
2. **注册时**：第一个注册用户自动成为管理员
3. **登录后**：右上角显示头像+昵称，点击进入个人中心
4. **管理员**：个人中心内出现「管理用户」按钮，可查看所有用户信息

### 不登录也能用

测评功能完全支持游客模式，不强制登录。

## 许可证

MIT