/**
 * 词汇测评核心模块
 * 包含测评逻辑、抽样算法、评分系统等
 */

class VocabularyExam {
    constructor(options = {}) {
        this.wordBank = options.wordBank || [];
        this.totalQuestions = options.totalQuestions || 50;
        this.optionsPerQuestion = options.optionsPerQuestion || 6;
        this.consecutiveWrongLimit = options.consecutiveWrongLimit || 4;
        this.totalWrongLimit = options.totalWrongLimit || 7;
        this.autoNextDelay = options.autoNextDelay || 1000;
        
        // 测评状态
        this.examWords = [];
        this.currentQuestion = 0;
        this.correctCount = 0;
        this.consecutiveWrong = 0;
        this.totalWrong = 0;
        this.selectedOption = null;
        this.answers = []; // 记录每题答案（含级别和难度）
        
        // 回调函数
        this.onQuestionChange = options.onQuestionChange || (() => {});
        this.onAnswer = options.onAnswer || (() => {});
        this.onExamEnd = options.onExamEnd || (() => {});
    }

    /**
     * 单词分布规则（分层抽样）
     */
    static getDistribution() {
        return [
            { level: '小学', difficulty: 1, count: 4 },
            { level: '小学', difficulty: 2, count: 6 },
            { level: '小学', difficulty: 3, count: 6 },
            { level: '初中', difficulty: 1, count: 6 },
            { level: '初中', difficulty: 2, count: 6 },
            { level: '初中', difficulty: 3, count: 6 },
            { level: '高中', difficulty: 1, count: 6 },
            { level: '高中', difficulty: 2, count: 6 },
            { level: '高中', difficulty: 3, count: 4 }
        ];
    }

    /**
     * 按规则抽样（避免重复和修改原始数据）
     */
    sampleWords() {
        const distribution = VocabularyExam.getDistribution();
        const result = [];
        const usedIndices = new Set(); // 追踪已使用的单词索引
        
        distribution.forEach(item => {
            const levelWords = this.wordBank.filter(w => w.level === item.level);
            
            for (let i = 0; i < item.count; i++) {
                if (levelWords.length === 0) break;
                
                // 找到该级别中未被使用的单词
                const availableWords = levelWords.filter((_, idx) => 
                    !usedIndices.has(`${item.level}_${idx}`)
                );
                
                if (availableWords.length === 0) {
                    // 如果没有未使用的，允许重复
                    const randomIndex = Math.floor(Math.random() * levelWords.length);
                    result.push({
                        ...levelWords[randomIndex],
                        difficulty: item.difficulty
                    });
                } else {
                    const randomIndex = Math.floor(Math.random() * availableWords.length);
                    const selectedWord = availableWords[randomIndex];
                    const originalIndex = levelWords.indexOf(selectedWord);
                    usedIndices.add(`${item.level}_${originalIndex}`);
                    
                    result.push({
                        ...selectedWord,
                        difficulty: item.difficulty
                    });
                }
            }
        });
        
        return result;
    }

    /**
     * 开始测评
     */
    start() {
        this.examWords = this.sampleWords();
        this.currentQuestion = 0;
        this.correctCount = 0;
        this.consecutiveWrong = 0;
        this.totalWrong = 0;
        this.selectedOption = null;
        this.answers = [];
        
        return this.examWords;
    }

    /**
     * 生成选项（防止无限循环，确保正确答案在选项中）
     */
    generateOptions(correctMean) {
        const distractors = this.wordBank
            .map(w => w.mean)
            .filter(mean => mean !== correctMean);
        
        // 去重
        const uniqueDistractors = [...new Set(distractors)];
        
        // Fisher-Yates 洗牌
        const shuffled = [...uniqueDistractors];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        
        // 取需要的干扰项数量
        const neededDistractors = Math.min(
            this.optionsPerQuestion - 1,
            shuffled.length
        );
        
        const options = [correctMean, ...shuffled.slice(0, neededDistractors)];
        
        // 干扰项不够时用占位符补充
        while (options.length < this.optionsPerQuestion) {
            options.push(`选项${options.length + 1}`);
        }
        
        // Fisher-Yates 打乱选项顺序
        for (let i = options.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [options[i], options[j]] = [options[j], options[i]];
        }
        
        return options;
    }

    /**
     * 提交答案
     */
    submitAnswer(selectedOption) {
        const currentWord = this.examWords[this.currentQuestion];
        const isCorrect = selectedOption === currentWord.mean;
        
        this.answers.push({
            word: currentWord.word,
            selected: selectedOption,
            correct: currentWord.mean,
            isCorrect,
            level: currentWord.level,
            difficulty: currentWord.difficulty
        });
        
        if (isCorrect) {
            this.correctCount++;
            this.consecutiveWrong = 0;
        } else {
            this.consecutiveWrong++;
            this.totalWrong++;
        }
        
        const shouldEnd = this.consecutiveWrong >= this.consecutiveWrongLimit ||
                         this.totalWrong >= this.totalWrongLimit;
        
        this.onAnswer({
            isCorrect,
            correctAnswer: currentWord.mean,
            shouldEnd
        });
        
        return { isCorrect, shouldEnd };
    }

    /**
     * 下一题
     */
    nextQuestion() {
        if (this.consecutiveWrong >= this.consecutiveWrongLimit ||
            this.totalWrong >= this.totalWrongLimit) {
            return this.end();
        }
        
        this.currentQuestion++;
        
        if (this.currentQuestion >= this.examWords.length) {
            return this.end();
        }
        
        this.selectedOption = null;
        this.onQuestionChange(this.currentQuestion);
        
        return { hasNext: true, index: this.currentQuestion };
    }

    /**
     * 结束测评
     */
    end() {
        const result = this.calculateResult();
        this.onExamEnd(result);
        return result;
    }

    /**
     * 计算测评结果
     */
    calculateResult() {
        const answeredCount = this.currentQuestion + 1;
        const correctRate = (this.correctCount / answeredCount) * 100;
        
        return {
            vocabularySize: this.calculateVocabulary(),
            level: this.getLevel(),
            correctCount: this.correctCount,
            totalAnswered: answeredCount,
            correctRate: correctRate.toFixed(1),
            suggestions: this.getSuggestions()
        };
    }

    /**
     * 计算词汇量（按级别和难度分别计算掌握率）
     */
    calculateVocabulary() {
        const baseVocabulary = {
            '小学': { 1: 300, 2: 600, 3: 1000 },
            '初中': { 1: 1500, 2: 2200, 3: 3000 },
            '高中': { 1: 4000, 2: 5000, 3: 6000 }
        };
        
        const weights = { '小学': 1.25, '初中': 1.1, '高中': 1.1 };
        
        // 按级别和难度统计正确率
        const stats = {};
        this.answers.forEach(answer => {
            const key = `${answer.level}_${answer.difficulty}`;
            if (!stats[key]) {
                stats[key] = { correct: 0, total: 0 };
            }
            stats[key].total++;
            if (answer.isCorrect) {
                stats[key].correct++;
            }
        });
        
        let totalVocabulary = 0;
        
        Object.keys(baseVocabulary).forEach(level => {
            let levelVocabulary = 0;
            
            Object.keys(baseVocabulary[level]).forEach(difficulty => {
                const key = `${level}_${difficulty}`;
                const stat = stats[key] || { correct: 0, total: 0 };
                
                // 该难度级别的掌握率
                const masteryRate = stat.total > 0 ? (stat.correct / stat.total) : 0;
                
                // 计算该难度的词汇量
                const difficultyVocabulary = baseVocabulary[level][difficulty] * masteryRate;
                levelVocabulary += difficultyVocabulary;
            });
            
            // 应用权重
            totalVocabulary += levelVocabulary * (weights[level] || 1);
        });
        
        return Math.round(totalVocabulary);
    }

    /**
     * 获取能力等级
     */
    getLevel() {
        const thresholds = [
            [10, '入门级'],
            [20, '小学水平'],
            [30, '初中水平'],
            [40, '高中水平'],
            [50, '优秀水平']
        ];
        
        for (const [threshold, level] of thresholds) {
            if (this.correctCount <= threshold) {
                return level;
            }
        }
        return '优秀水平';
    }

    /**
     * 获取学习建议
     */
    getSuggestions() {
        const suggestions = {
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
        };
        
        const level = this.getLevel();
        return suggestions[level] || ['继续保持学习，不断提高词汇量'];
    }

    /**
     * 获取当前进度百分比
     */
    getProgress() {
        return ((this.currentQuestion + 1) / this.examWords.length) * 100;
    }
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VocabularyExam;
}
