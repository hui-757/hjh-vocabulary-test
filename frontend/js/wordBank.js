/**
 * 词库加载模块
 * 负责从服务器加载和管理词库数据
 */

class WordBankLoader {
    constructor(options = {}) {
        this.filePath = options.filePath || '../../data/word_bank/word_bank.json';
        this.timeout = options.timeout || 60000;
        this.words = [];
        this.isLoading = false;
        this.onLoad = options.onLoad || (() => {});
        this.onError = options.onError || (() => {});
    }

    /**
     * 加载词库
     */
    async load() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        console.log('开始加载词库:', this.filePath);
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);
            
            const response = await fetch(this.filePath, {
                signal: controller.signal,
                cache: 'no-store'
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP错误: ${response.status}`);
            }
            
            const rawText = await response.text();
            const data = JSON.parse(rawText);
            
            if (!data.words || !Array.isArray(data.words)) {
                throw new Error('词库数据格式错误: 缺少words字段');
            }
            
            // 过滤有效单词
            this.words = data.words
                .filter(w => w.word && w.mean)
                .map(w => ({
                    word: w.word,
                    mean: w.mean,
                    level: w.level || '其他'
                }));
            
            console.log(`词库加载完成: ${this.words.length} 个单词`);
            this.onLoad(this.words);
            return this.words;
            
        } catch (error) {
            console.error('词库加载失败:', error);
            this.words = [];
            this.onError(error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * 获取按级别筛选的单词
     */
    getWordsByLevel(level) {
        return this.words.filter(w => w.level === level);
    }

    /**
     * 获取所有级别
     */
    getLevels() {
        const levels = new Set(this.words.map(w => w.level));
        return Array.from(levels);
    }

    /**
     * 检查是否已加载
     */
    isReady() {
        return this.words.length > 0;
    }
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WordBankLoader;
}
