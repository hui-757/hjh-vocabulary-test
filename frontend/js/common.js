/**
 * 公共工具函数模块
 * 包含项目中共享的JavaScript辅助函数
 */

/**
 * DOM 工具函数
 */
const DOM = {
    /**
     * 获取单个元素
     */
    get(id) {
        return document.getElementById(id);
    },

    /**
     * 显示元素
     */
    show(element) {
        if (typeof element === 'string') element = this.get(element);
        if (element) element.style.display = 'block';
    },

    /**
     * 隐藏元素
     */
    hide(element) {
        if (typeof element === 'string') element = this.get(element);
        if (element) element.style.display = 'none';
    },

    /**
     * 设置文本内容
     */
    text(element, content) {
        if (typeof element === 'string') element = this.get(element);
        if (element) element.textContent = content;
    },

    /**
     * 设置HTML内容
     */
    html(element, content) {
        if (typeof element === 'string') element = this.get(element);
        if (element) element.innerHTML = content;
    }
};

/**
 * 文件读取工具
 */
const FileReaderUtil = {
    /**
     * 读取文本文件
     */
    readText(file, encoding = 'utf-8') {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = () => reject(new Error('读取文件失败'));
            reader.readAsText(file, encoding);
        });
    },

    /**
     * 读取二进制文件
     */
    readBinary(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = () => reject(new Error('读取文件失败'));
            reader.readAsArrayBuffer(file);
        });
    }
};

/**
 * 词库数据处理工具
 */
const WordBankUtil = {
    /**
     * 清理控制字符
     */
    cleanControlChars(text) {
        return text.replace(/[\x00-\x1F\x7F]/g, '');
    },

    /**
     * 验证单词数据
     */
    validateWord(wordData) {
        return wordData && 
               wordData.word && 
               wordData.mean && 
               wordData.word.toString().trim() && 
               wordData.mean.toString().trim();
    },

    /**
     * 从文件名提取级别
     */
    getLevelFromFilename(filename, config = {}) {
        const lowerName = filename.toLowerCase();
        const mapping = {
            '小学': '小学',
            '初中': '初中',
            '高中': '高中',
            '四级': '四级',
            ...config
        };
        
        for (const [key, level] of Object.entries(mapping)) {
            if (lowerName.includes(key.toLowerCase())) {
                return level;
            }
        }
        return '其他';
    },

    /**
     * 创建标准词库数据
     */
    createWordBankData(words) {
        return {
            words: words,
            generated_at: new Date().toISOString(),
            total_words: words.length
        };
    },

    /**
     * 修复JSON数据
     */
    fixJsonData(content) {
        content = this.cleanControlChars(content);
        content = content.trim();
        
        // 修复多余逗号
        content = content.replace(/,\s*}/g, '}');
        content = content.replace(/,\s*\]/g, ']');
        
        return content;
    }
};

/**
 * 通知/消息工具
 */
const Notify = {
    /**
     * 显示状态消息
     */
    show(containerId, message, type = 'info') {
        const container = DOM.get(containerId);
        if (!container) return;
        
        const typeMap = {
            'success': 'status-success',
            'error': 'status-error',
            'info': 'status-info',
            'warning': 'status-warning'
        };
        
        container.innerHTML = `<p class="${typeMap[type] || 'status-info'}">${message}</p>`;
    },

    /**
     * 清空状态消息
     */
    clear(containerId) {
        const container = DOM.get(containerId);
        if (container) container.innerHTML = '';
    }
};

/**
 * 随机工具（修复：使用Fisher-Yates洗牌）
 */
const Random = {
    /**
     * 从数组中随机选择指定数量的不重复元素
     */
    sample(array, count) {
        if (count >= array.length) return [...array];
        
        // Fisher-Yates 洗牌后取前count个
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled.slice(0, count);
    },

    /**
     * 生成随机整数 [min, max)
     */
    int(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DOM, FileReaderUtil, WordBankUtil, Notify, Random };
}
