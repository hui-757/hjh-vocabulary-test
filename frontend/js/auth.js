/**
 * 用户认证模块
 * 负责注册、登录、登出、Token 管理与用户信息缓存
 */

const AUTH = {
    // API 基础地址
    API_BASE: 'http://localhost:5000/api',
    
    // localStorage 键名
    TOKEN_KEY: 'hjh_auth_token',
    USER_KEY: 'hjh_user_info',
    
    /**
     * 获取存储的 Token
     */
    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    },
    
    /**
     * 保存 Token
     */
    setToken(token) {
        localStorage.setItem(this.TOKEN_KEY, token);
    },
    
    /**
     * 清除 Token（登出）
     */
    clearToken() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
    },
    
    /**
     * 获取缓存的用户信息
     */
    getCachedUser() {
        try {
            const raw = localStorage.getItem(this.USER_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch {
            return null;
        }
    },
    
    /**
     * 缓存用户信息
     */
    setCachedUser(user) {
        localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    },
    
    /**
     * 检查是否已登录
     */
    isLoggedIn() {
        return !!this.getToken();
    },
    
    /**
     * 检查当前用户是否为管理员
     */
    isAdmin() {
        const user = this.getCachedUser();
        return user && user.role === 'admin';
    },
    
    /**
     * 保存测试记录
     */
    async saveRecord(result, wrongAnswers) {
        return this.request('/records', {
            method: 'POST',
            body: JSON.stringify({ result, wrongAnswers })
        });
    },
    
    /**
     * 获取当前用户的测试记录列表
     */
    async fetchRecords() {
        return this.request('/records', { method: 'GET' });
    },
    
    /**
     * 获取单次测试记录详情
     */
    async fetchRecordDetail(recordId) {
        return this.request(`/records/${recordId}`, { method: 'GET' });
    },
    
    /**
     * 获取个人错题本
     */
    async fetchPersonalMistakes() {
        return this.request('/mistakes/personal', { method: 'GET' });
    },
    
    /**
     * 获取全服错题统计（管理员）
     */
    async fetchGlobalMistakes() {
        return this.request('/mistakes/global', { method: 'GET' });
    },
    
    /**
     * 获取当前管理员级别（null=非管理员，1=一级，2=二级）
     */
    getAdminLevel() {
        const user = this.getCachedUser();
        if (!user || user.role !== 'admin') return null;
        // 兼容旧数据：没有admin_level的admin视为一级
        return user.admin_level === undefined ? 1 : user.admin_level;
    },
    
    /**
     * 发送 API 请求（自动携带 Token）
     */
    async request(url, options = {}) {
        const token = this.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const fullUrl = `${this.API_BASE}${url}`;
        console.log(`[AUTH.request] ${options.method || 'GET'} ${fullUrl}`);
        
        try {
            const response = await fetch(fullUrl, {
                ...options,
                headers
            });
            
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                console.warn(`[AUTH.request] HTTP ${response.status}:`, data);
            }
            return { ok: response.ok, status: response.status, data };
        } catch (error) {
            console.error('[AUTH.request] 网络错误:', error);
            return { ok: false, status: 0, data: { message: '网络错误，请检查后端服务是否启动' }, error };
        }
    },
    
    /**
     * 用户注册
     */
    async register(username, password, nickname, role = 'user') {
        const result = await this.request('/register', {
            method: 'POST',
            body: JSON.stringify({ username, password, nickname, role })
        });
        
        if (result.ok && result.data.success) {
            this.setCachedUser(result.data.user);
        }
        
        return result;
    },
    
    /**
     * 用户登录
     */
    async login(username, password) {
        const result = await this.request('/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        if (result.ok && result.data.success) {
            this.setToken(result.data.token);
            this.setCachedUser(result.data.user);
        }
        
        return result;
    },
    
    /**
     * 用户登出
     */
    async logout() {
        await this.request('/logout', { method: 'POST' });
        this.clearToken();
    },
    
    /**
     * 获取当前用户信息（从服务器刷新）
     */
    async fetchProfile() {
        const result = await this.request('/profile', { method: 'GET' });
        if (result.ok && result.data.success) {
            this.setCachedUser(result.data.user);
        }
        return result;
    },
    
    /**
     * 获取所有用户列表（管理员）
     */
    async fetchUsers() {
        return this.request('/users', { method: 'GET' });
    },
    
    /**
     * 更新用户角色（仅一级管理员）
     */
    async updateUserRole(userId, role, adminLevel) {
        return this.request(`/users/${userId}/role`, {
            method: 'PUT',
            body: JSON.stringify({ role, admin_level: adminLevel })
        });
    },
    
    /**
     * 初始化：尝试从缓存恢复登录态
     */
    async init() {
        if (this.isLoggedIn()) {
            const result = await this.fetchProfile();
            if (!result.ok) {
                // Token 失效，清除
                this.clearToken();
            }
        }
    },
    
    /**
     * 显示登录弹窗
     */
    showLoginModal() {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.style.display = 'flex';
            this.switchAuthTab('login');
        }
    },
    
    /**
     * 关闭登录弹窗
     */
    hideLoginModal() {
        const modal = document.getElementById('auth-modal');
        if (modal) modal.style.display = 'none';
    },
    
    /**
     * 切换登录/注册标签
     */
    switchAuthTab(tab) {
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.auth-panel').forEach(p => p.classList.remove('active'));
        
        const activeTab = document.querySelector(`.auth-tab[data-tab="${tab}"]`);
        const activePanel = document.getElementById(`${tab}-panel`);
        
        if (activeTab) activeTab.classList.add('active');
        if (activePanel) activePanel.classList.add('active');
    }
};


/**
 * 初始化页面头部的用户区域
 * 在 index.html 的 DOMContentLoaded 中调用
 */
function initUserHeader() {
    const container = document.getElementById('user-header');
    if (!container) return;
    
    const user = AUTH.getCachedUser();
    
    if (user) {
        // 已登录：显示头像 + 昵称 + 测试记录按钮
        container.innerHTML = `
            <div class="user-badge" onclick="goToProfile()">
                <div class="user-avatar">${user.nickname ? user.nickname[0].toUpperCase() : '?'}</div>
                <span class="user-name">${user.nickname || user.username}</span>
            </div>
            <button class="btn btn-outline btn-sm" onclick="goToRecords()">
                测试记录
            </button>
        `;
    } else {
        // 未登录：显示登录按钮
        container.innerHTML = `
            <button class="btn btn-outline btn-sm" onclick="AUTH.showLoginModal()">
                登录 / 注册
            </button>
        `;
    }
}

/**
 * 跳转测试记录页面
 */
function goToRecords() {
    window.location.href = 'records.html';
}

/**
 * 跳转个人中心
 */
function goToProfile() {
    window.location.href = 'profile.html';
}


// 导出（兼容模块环境）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AUTH;
}
