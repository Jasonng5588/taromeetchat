// ===== TaroMeet App JavaScript =====

// API Configuration - Dynamic URL
// 1. Web Localhost: Use localhost:8000
// 2. Web IP (LAN): Use IP:8000
// 3. Android Emulator: Use 10.0.2.2:8000
// 4. Real Device (built apk): Need manual IP or logic

let api_url = 'http://localhost:8000'; // Default
const isCapacitor = window.Capacitor !== undefined;

if (isCapacitor) {
    // Mobile Environment
    console.log('Environment: Capacitor/Mobile');
    // Default to LAN IP for real device
    api_url = 'http://192.168.100.213:8000';
} else {
    // Web Environment
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1') {
        api_url = 'http://localhost:8000';
    } else if (window.location.protocol === 'file:') {
        // Opened as file, assume local
        api_url = 'http://localhost:8000';
    } else {
        // Accessed via IP (e.g. 192.168.1.x), assume backend is on same host
        api_url = `http://${host}:8000`;
    }
}

const API_BASE = api_url;
console.log('TaroMeet API URL configured as:', API_BASE);

const DEMO_MODE = true; // Enabled - works without backend server


// App State
let state = {
    user: null,
    token: null,
    currentScreen: 'splash-screen',
    theme: 'light',
    language: 'zh'
};

// ===== Internationalization (i18n) =====
const translations = {
    zh: {
        // App
        appTagline: 'AI 情感陪伴助手',
        // Auth
        welcomeBack: '欢迎回来',
        loginSubtitle: '登录您的 TaroMeet 账户',
        createAccount: '创建账户',
        registerSubtitle: '开始您的心灵之旅',
        emailPlaceholder: '邮箱地址',
        passwordPlaceholder: '密码',
        usernamePlaceholder: '用户名',
        login: '登录',
        register: '注册',
        noAccount: '还没有账户？',
        haveAccount: '已有账户？',
        registerNow: '立即注册',
        loginNow: '立即登录',
        // Home
        goodMorning: '早上好',
        goodAfternoon: '下午好',
        goodEvening: '晚上好',
        dailyQuote: '每一天都是新的开始，相信自己，你值得被爱。',
        exploreFeatures: '探索功能',
        moodAssistant: '心情助理',
        moodDesc: 'AI 倾听你的心声',
        loveCoach: '恋爱教练',
        loveDesc: '提升你的魅力值',
        diary: '反省日记',
        diaryDesc: '每日自我成长',
        voiceCompanion: '语音陪伴',
        voiceDesc: '有人陪你聊天',
        tarot: '塔罗占卜',
        tarotDesc: '探索命运指引',
        unlockAi: '解锁无限 AI 对话',
        monthlyPrice: '每月仅需 RM 19.90',
        // Nav
        home: '首页',
        mood: '心情',
        tarotNav: '塔罗',
        profile: '我的',
        // Settings
        personalCenter: '个人中心',
        darkMode: '深色模式',
        language: '语言',
        upgradePremium: '升级会员',
        emotionReport: '情绪报告',
        notifications: '通知设置',
        helpCenter: '帮助中心',
        logout: '退出登录',
        todayUsage: '今日使用情况',
        aiChat: 'AI 对话',
        tarotReading: '塔罗占卜',
        freeVersion: '免费版',
        // Premium
        unlockAll: '解锁全部 AI 功能',
        unlimitedChat: '无限 AI 对话次数',
        unlimitedVoice: '无限语音陪伴时长',
        dailyTarot: '每日 10 次塔罗占卜',
        fullHistory: '完整历史记录',
        advancedReport: '高级情绪分析报告',
        subscribe: '立即订阅',
        cancelAnytime: '随时可取消，无风险',
        // Features
        moodTitle: 'AI 心情助理',
        moodIntro: '💝 告诉我你现在的心情，我会给你温暖的回应',
        writeMood: '写下你此刻的心情...',
        sendToAi: '发送给 AI',
        loveTitle: 'AI 恋爱教练',
        loveIntro: '💕 粘贴你们的聊天记录，我帮你分析如何回复更合适',
        pasteChat: '粘贴聊天记录在这里...',
        analyzeChat: '分析聊天',
        diaryTitle: 'AI 反省日记',
        diaryIntro: '📝 每天一句话，AI 帮你进行深度自我反省',
        diaryPrompt: '今天最让你印象深刻的一件事是什么？',
        writeInsight: '写下你今天的感悟...',
        startReflect: '开始反省',
        voiceTitle: '语音陪伴',
        voiceName: '小塔',
        voiceStatus: '在线陪伴中',
        voiceWelcome: '你好呀～我是小塔，今天想聊些什么呢？无论开心还是难过，我都在这里陪你。',
        inputMessage: '输入消息...',
        send: '发送',
        tarotTitle: '塔罗占卜',
        tarotIntro: '🔮 静心冥想，让塔罗牌为你揭示命运的指引',
        tarotQuestion: '心中默念你的问题（可选）',
        startTarot: '开始占卜',
        redraw: '重新占卜',
        tapToStart: '点击下方开始抽牌',
        // Toast messages
        loginSuccess: '登录成功！欢迎回来 💖',
        registerSuccess: '注册成功！开始你的心灵之旅 ✨',
        loggedOut: '已退出登录',
        copied: '已复制到剪贴板 ✓',
        enterMood: '请先输入你的心情',
        pasteFirst: '请先粘贴聊天记录',
        writeFirst: '请先写下你的感悟',
        aiThinking: 'AI 正在思考中...'
    },
    en: {
        // App
        appTagline: 'AI Emotional Companion',
        // Auth
        welcomeBack: 'Welcome Back',
        loginSubtitle: 'Login to your TaroMeet account',
        createAccount: 'Create Account',
        registerSubtitle: 'Start your soul journey',
        emailPlaceholder: 'Email address',
        passwordPlaceholder: 'Password',
        usernamePlaceholder: 'Username',
        login: 'Login',
        register: 'Register',
        noAccount: "Don't have an account?",
        haveAccount: 'Already have an account?',
        registerNow: 'Register now',
        loginNow: 'Login now',
        // Home
        goodMorning: 'Good morning',
        goodAfternoon: 'Good afternoon',
        goodEvening: 'Good evening',
        dailyQuote: 'Every day is a new beginning. Believe in yourself, you deserve to be loved.',
        exploreFeatures: 'Explore Features',
        moodAssistant: 'Mood Assistant',
        moodDesc: 'AI listens to your heart',
        loveCoach: 'Love Coach',
        loveDesc: 'Boost your charm',
        diary: 'Reflection Diary',
        diaryDesc: 'Daily self-growth',
        voiceCompanion: 'Voice Companion',
        voiceDesc: 'Someone to chat with',
        tarot: 'Tarot Reading',
        tarotDesc: 'Explore your destiny',
        unlockAi: 'Unlock Unlimited AI Chat',
        monthlyPrice: 'Only RM 19.90/month',
        // Nav
        home: 'Home',
        mood: 'Mood',
        tarotNav: 'Tarot',
        profile: 'Profile',
        // Settings
        personalCenter: 'Profile',
        darkMode: 'Dark Mode',
        language: 'Language',
        upgradePremium: 'Upgrade to Premium',
        emotionReport: 'Emotion Report',
        notifications: 'Notifications',
        helpCenter: 'Help Center',
        logout: 'Logout',
        todayUsage: "Today's Usage",
        aiChat: 'AI Chat',
        tarotReading: 'Tarot Reading',
        freeVersion: 'Free',
        // Premium
        unlockAll: 'Unlock All AI Features',
        unlimitedChat: 'Unlimited AI conversations',
        unlimitedVoice: 'Unlimited voice companion',
        dailyTarot: '10 tarot readings per day',
        fullHistory: 'Complete history',
        advancedReport: 'Advanced emotion analysis',
        subscribe: 'Subscribe Now',
        cancelAnytime: 'Cancel anytime, risk-free',
        // Features
        moodTitle: 'AI Mood Assistant',
        moodIntro: '💝 Tell me how you feel, and I will give you a warm response',
        writeMood: 'Write down how you feel...',
        sendToAi: 'Send to AI',
        loveTitle: 'AI Love Coach',
        loveIntro: '💕 Paste your chat history, and I will help you analyze how to reply better',
        pasteChat: 'Paste chat history here...',
        analyzeChat: 'Analyze Chat',
        diaryTitle: 'AI Reflection Diary',
        diaryIntro: '📝 One sentence a day, AI helps you with deep self-reflection',
        diaryPrompt: 'What impressed you the most today?',
        writeInsight: 'Write down your insights...',
        startReflect: 'Start Reflection',
        voiceTitle: 'Voice Companion',
        voiceName: 'Luna',
        voiceStatus: 'Online',
        voiceWelcome: "Hi there~ I'm Luna. What would you like to chat about today? Whether happy or sad, I'm here with you.",
        inputMessage: 'Type a message...',
        send: 'Send',
        tarotTitle: 'Tarot Reading',
        tarotIntro: '🔮 Clear your mind and let the tarot reveal your destiny',
        tarotQuestion: 'Think of your question (optional)',
        startTarot: 'Draw Cards',
        redraw: 'Draw Again',
        tapToStart: 'Tap below to draw cards',
        // Toast messages
        loginSuccess: 'Login successful! Welcome back 💖',
        registerSuccess: 'Registration successful! Start your journey ✨',
        loggedOut: 'Logged out',
        copied: 'Copied to clipboard ✓',
        enterMood: 'Please enter your mood first',
        pasteFirst: 'Please paste chat history first',
        writeFirst: 'Please write your insight first',
        aiThinking: 'AI is thinking...'
    }
};

// ===== Theme & Language Functions =====
function toggleTheme() {
    const isDark = document.getElementById('theme-toggle').checked;
    state.theme = isDark ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('taromeet_theme', state.theme);
}

function changeLanguage(lang) {
    state.language = lang;
    localStorage.setItem('taromeet_language', lang);
    applyTranslations();
}

function applyTranslations() {
    const t = translations[state.language];

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (t[key]) {
            el.textContent = t[key];
        }
    });

    // Update placeholders
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => input.placeholder = t.emailPlaceholder);

    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => input.placeholder = t.passwordPlaceholder);

    // Update document title
    document.title = `TaroMeet - ${t.appTagline}`;
}

function initThemeAndLanguage() {
    // Load saved theme
    const savedTheme = localStorage.getItem('taromeet_theme') || 'light';
    state.theme = savedTheme;
    document.documentElement.setAttribute('data-theme', savedTheme);

    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.checked = savedTheme === 'dark';
    }

    // Load saved language
    const savedLang = localStorage.getItem('taromeet_language') || 'zh';
    state.language = savedLang;

    const langSelect = document.getElementById('language-select');
    if (langSelect) {
        langSelect.value = savedLang;
    }

    applyTranslations();
}

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    // Auto-login with demo user - skip login screen
    state.token = 'demo_token';
    state.user = {
        username: 'Demo User',
        email: 'demo@taromeet.com'
    };
    localStorage.setItem('taromeet_token', 'demo_token');
    localStorage.setItem('taromeet_user', JSON.stringify(state.user));

    // Setup event listeners
    setupEventListeners();

    // Initialize theme and language
    initThemeAndLanguage();

    // Production ready - no debug output

    // Show splash and then go directly to home
    setTimeout(() => {
        showScreen('home-screen');
        updateUserUI();
    }, 2000);
});

// ===== Event Listeners =====
function setupEventListeners() {
    // Login form
    document.getElementById('login-form').addEventListener('submit', handleLogin);

    // Register form
    document.getElementById('register-form').addEventListener('submit', handleRegister);

    // Bottom navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const screen = item.dataset.screen;
            showScreen(screen);

            // Update active state
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            item.classList.add('active');
        });
    });

    // Emoji buttons for mood
    document.querySelectorAll('.emoji-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.emoji-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const mood = btn.dataset.mood;
            const input = document.getElementById('mood-input');
            if (!input.value) {
                input.value = `我今天感觉${mood}`;
            }
        });
    });
}

// ===== Screen Navigation =====
function showScreen(screenId) {
    // Hide current screen
    const currentScreen = document.querySelector('.screen.active');
    if (currentScreen) {
        currentScreen.classList.remove('active');
    }

    // Show new screen
    const newScreen = document.getElementById(screenId);
    if (newScreen) {
        newScreen.classList.add('active');
        state.currentScreen = screenId;
    }
}

// ===== Authentication =====
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    showLoading();

    // Demo mode - simulate login
    if (DEMO_MODE) {
        await new Promise(r => setTimeout(r, 1000));
        const demoUser = {
            username: email.split('@')[0] || 'Demo User',
            email: email
        };
        state.token = 'demo_token';
        state.user = demoUser;
        localStorage.setItem('taromeet_token', 'demo_token');
        localStorage.setItem('taromeet_user', JSON.stringify(demoUser));
        hideLoading();
        updateUserUI();
        showScreen('home-screen');
        showToast(translations[state.language].loginSuccess);
        return;
    }

    try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '登录失败');
        }

        const data = await response.json();

        state.token = data.access_token;
        state.user = data.user;

        localStorage.setItem('taromeet_token', data.access_token);
        localStorage.setItem('taromeet_user', JSON.stringify(data.user));

        hideLoading();
        updateUserUI();
        showScreen('home-screen');
        showToast(translations[state.language].loginSuccess);

    } catch (error) {
        hideLoading();
        showToast(error.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();

    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    showLoading();

    // Demo mode - simulate registration
    if (DEMO_MODE) {
        await new Promise(r => setTimeout(r, 1000));
        const demoUser = {
            username: username,
            email: email
        };
        state.token = 'demo_token';
        state.user = demoUser;
        localStorage.setItem('taromeet_token', 'demo_token');
        localStorage.setItem('taromeet_user', JSON.stringify(demoUser));
        hideLoading();
        updateUserUI();
        showScreen('home-screen');
        showToast(translations[state.language].registerSuccess);
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") === -1) {
            // Received non-JSON response (likely HTML error page)
            const text = await response.text();
            console.error('API Error (Non-JSON):', text);
            throw new Error(`连接错误(${response.status}): ${text.substring(0, 50)}...`);
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '注册失败');
        }

        const data = await response.json();

        state.token = data.access_token;
        state.user = data.user;

        localStorage.setItem('taromeet_token', data.access_token);
        localStorage.setItem('taromeet_user', JSON.stringify(data.user));

        hideLoading();
        updateUserUI();
        showScreen('home-screen');
        showToast(translations[state.language].registerSuccess);

    } catch (error) {
        hideLoading();
        console.error('Register error:', error);

        // Handle "Unexpected token" specifically
        if (error.message.includes('Unexpected token') || error.message.includes('JSON')) {
            showToast('连接服务器失败，请检查后端是否已启动');
        } else {
            showToast(error.message);
        }
    }
}

function logout() {
    state.token = null;
    state.user = null;
    localStorage.removeItem('taromeet_token');
    localStorage.removeItem('taromeet_user');
    showScreen('login-screen');
    showToast('已退出登录');
}

function updateUserUI() {
    if (state.user) {
        document.getElementById('home-username').textContent = state.user.username;
        document.getElementById('settings-username').textContent = state.user.username;
        document.getElementById('settings-email').textContent = state.user.email;

        // Update greeting based on time
        const hour = new Date().getHours();
        let greeting = '你好';
        if (hour >= 5 && hour < 12) greeting = '早上好';
        else if (hour >= 12 && hour < 18) greeting = '下午好';
        else greeting = '晚上好';

        document.querySelector('.greeting-text').textContent = greeting;
    }
}

// ===== API Helper =====
async function apiRequest(endpoint, method = 'GET', body = null) {
    // In demo mode, use demo responses
    if (DEMO_MODE) {
        return getDemoResponse(endpoint, body);
    }

    const headers = {
        'Content-Type': 'application/json'
    };

    if (state.token) {
        headers['Authorization'] = `Bearer ${state.token}`;
    }

    const options = {
        method,
        headers
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, options);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || '请求失败');
    }

    return response.json();
}

// ===== Demo Mode Responses =====
async function getDemoResponse(endpoint, body) {
    await new Promise(r => setTimeout(r, 1500)); // Simulate API delay

    if (endpoint === '/mood/analyze') {
        // Use the 500+ responses from mood-responses.js with no short-term repetition
        return getMoodResponse();
    }


    if (endpoint === '/love/analyze') {
        return {
            analysis: '从对话来看，对方似乎有些疲惫，可能需要一些关心和理解。你的回复稍微简短了一些，可以尝试更多地表达关心。',
            suggestions: ['辛苦了～今天累了就早点休息，我陪你聊天解解乏', '怎么了？愿意跟我说说吗？我在呢', '要不要一起看个轻松的视频放松一下？'],
            tips: '在对方疲惫时表达关心，是提高亲密度的好时机。记得语气温柔一些～',
            affection_score: 65 + Math.floor(Math.random() * 20)
        };
    }

    if (endpoint === '/diary/reflect') {
        return {
            reflection: '今天你记录下了这个重要的时刻，这本身就是一种成长。通过反思，你正在更深入地了解自己。',
            growth_insight: '每一次记录都是与内心的对话，你正在建立自我觉察的习惯，这是通往内心平静的重要一步。',
            tomorrow_suggestion: '明天试着对一个陌生人微笑，感受分享善意的快乐。',
            growth_score: 70 + Math.floor(Math.random() * 25)
        };
    }

    if (endpoint === '/voice/chat') {
        // Use context-aware responses that analyze user message keywords
        const userMessage = body?.message || '';
        return { response_text: getVoiceResponse(userMessage) };
    }

    if (endpoint === '/tarot/draw') {
        const allCards = [
            { name: 'The Star', meaning: '希望，灵感，宁静' },
            { name: 'The Lovers', meaning: '爱情，选择，和谐' },
            { name: 'The Sun', meaning: '成功，快乐，活力' },
            { name: 'The Moon', meaning: '直觉，潜意识，梦境' },
            { name: 'The Fool', meaning: '新开始，冒险，纯真' },
            { name: 'Strength', meaning: '勇气，力量，耐心' },
            { name: 'The World', meaning: '完成，成就，旅程' },
            { name: 'The Empress', meaning: '丰饶，创造，母性' },
            { name: 'Wheel of Fortune', meaning: '命运，转变，机遇' }
        ];
        const shuffled = allCards.sort(() => Math.random() - 0.5);
        const cards = shuffled.slice(0, 3);

        return {
            cards: cards,
            interpretation: `亲爱的，塔罗牌为你揭示了美好的指引。${cards[0].name}告诉我们${cards[0].meaning.split('，')[0]}正在向你走来。${cards[1].name}暗示你可能正面临关于${cards[1].meaning.split('，')[1]}的选择，相信你的直觉。${cards[2].name}带来了最灿烂的祝福，${cards[2].meaning.split('，')[0]}正在前方等待着你。总体而言，这是一个充满希望和光明的时期，勇敢地追随你的心吧。`
        };
    }

    throw new Error('Unknown endpoint');
}

// ===== Mood Analysis =====
async function analyzeMood() {
    const input = document.getElementById('mood-input');
    const moodText = input.value.trim();

    if (!moodText) {
        showToast('请先输入你的心情');
        return;
    }

    showLoading();

    try {
        const result = await apiRequest('/mood/analyze', 'POST', { mood_text: moodText });

        hideLoading();

        // Display response
        const responseDiv = document.getElementById('mood-response');
        responseDiv.classList.remove('hidden');

        document.getElementById('mood-emoji').textContent = result.emoji;
        document.getElementById('mood-encouragement').textContent = result.encouragement;
        document.getElementById('mood-suggestion').innerHTML = `💡 ${result.suggestion}`;

        // Clear input
        input.value = '';
        document.querySelectorAll('.emoji-btn').forEach(b => b.classList.remove('active'));

    } catch (error) {
        hideLoading();
        showToast(error.message);
    }
}

// ===== Love Coach =====
async function analyzeLove() {
    const input = document.getElementById('love-input');
    const chatContent = input.value.trim();

    if (!chatContent) {
        showToast('请先粘贴聊天记录');
        return;
    }

    showLoading();

    try {
        const result = await apiRequest('/love/analyze', 'POST', { chat_content: chatContent });

        hideLoading();

        // Display response
        const responseDiv = document.getElementById('love-response');
        responseDiv.classList.remove('hidden');

        // Affection meter
        document.getElementById('affection-fill').style.width = `${result.affection_score}%`;
        document.getElementById('affection-value').textContent = `${result.affection_score}%`;

        // Analysis
        document.getElementById('love-analysis').textContent = result.analysis;

        // Suggestions
        const suggestionsDiv = document.getElementById('love-suggestions');
        suggestionsDiv.innerHTML = result.suggestions.map((s, i) => `
            <div class="suggestion-item" onclick="copySuggestion(this)">
                <span>${i + 1}. ${s}</span>
                <button class="copy-btn">复制</button>
            </div>
        `).join('');

        // Tips
        document.getElementById('love-tips').textContent = result.tips;

    } catch (error) {
        hideLoading();
        showToast(error.message);
    }
}

function copySuggestion(element) {
    const text = element.querySelector('span').textContent.replace(/^\d+\.\s*/, '');
    navigator.clipboard.writeText(text).then(() => {
        showToast('已复制到剪贴板 ✓');
    });
}

// ===== Diary Reflection =====
async function reflectDiary() {
    const input = document.getElementById('diary-input');
    const content = input.value.trim();

    if (!content) {
        showToast('请先写下你的感悟');
        return;
    }

    showLoading();

    try {
        const result = await apiRequest('/diary/reflect', 'POST', { content });

        hideLoading();

        // Display response
        const responseDiv = document.getElementById('diary-response');
        responseDiv.classList.remove('hidden');

        // Growth meter
        document.getElementById('growth-fill').style.width = `${result.growth_score}%`;
        document.getElementById('growth-value').textContent = `${result.growth_score}%`;

        // Content
        document.getElementById('diary-reflection').textContent = result.reflection;
        document.getElementById('diary-insight').textContent = result.growth_insight;
        document.getElementById('diary-tomorrow').textContent = result.tomorrow_suggestion;

        // Clear input
        input.value = '';

    } catch (error) {
        hideLoading();
        showToast(error.message);
    }
}

// ===== Voice Companion =====
function handleVoiceEnter(event) {
    if (event.key === 'Enter') {
        sendVoiceMessage();
    }
}

async function sendVoiceMessage() {
    const input = document.getElementById('voice-input');
    const message = input.value.trim();

    if (!message) return;

    // Add user message
    const messagesDiv = document.getElementById('voice-messages');
    messagesDiv.innerHTML += `
        <div class="message user-message">
            <span class="message-avatar">👤</span>
            <div class="message-bubble">
                <p>${escapeHtml(message)}</p>
            </div>
        </div>
    `;

    input.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    try {
        const result = await apiRequest('/voice/chat', 'POST', { message });

        // Add AI response
        messagesDiv.innerHTML += `
            <div class="message ai-message">
                <span class="message-avatar">🌙</span>
                <div class="message-bubble">
                    <p>${escapeHtml(result.response_text)}</p>
                </div>
            </div>
        `;

        messagesDiv.scrollTop = messagesDiv.scrollHeight;

    } catch (error) {
        showToast(error.message);
    }
}

// ===== Tarot Reading =====
const TAROT_ICONS = {
    'The Fool': '🃏', 'The Magician': '🎩', 'The High Priestess': '🌙',
    'The Empress': '👑', 'The Emperor': '🛡️', 'The Hierophant': '📿',
    'The Lovers': '💕', 'The Chariot': '🏎️', 'Strength': '🦁',
    'The Hermit': '🔦', 'Wheel of Fortune': '🎡', 'Justice': '⚖️',
    'The Hanged Man': '🙃', 'Death': '🦋', 'Temperance': '☯️',
    'The Devil': '😈', 'The Tower': '🗼', 'The Star': '⭐',
    'The Moon': '🌕', 'The Sun': '☀️', 'Judgement': '📯',
    'The World': '🌍'
};

async function drawTarot() {
    const questionInput = document.getElementById('tarot-question');
    const question = questionInput.value.trim();

    showLoading();

    try {
        const result = await apiRequest('/tarot/draw', 'POST', {
            question: question || null,
            num_cards: 3
        });

        hideLoading();

        // Hide deck, show result
        document.getElementById('tarot-deck').classList.add('hidden');
        document.getElementById('tarot-result').classList.remove('hidden');

        // Display cards
        const cardsDiv = document.getElementById('drawn-cards');
        cardsDiv.innerHTML = result.cards.map(card => `
            <div class="tarot-card-item">
                <div class="card-icon">${TAROT_ICONS[card.name] || '🔮'}</div>
                <div class="card-name">${card.name}</div>
                <div class="card-meaning">${card.meaning}</div>
            </div>
        `).join('');

        // Display interpretation
        document.getElementById('tarot-interpretation').textContent = result.interpretation;

    } catch (error) {
        hideLoading();
        showToast(error.message);
    }
}

function resetTarot() {
    document.getElementById('tarot-deck').classList.remove('hidden');
    document.getElementById('tarot-result').classList.add('hidden');
    document.getElementById('tarot-question').value = '';
}

// ===== Utility Functions =====
function showLoading() {
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, duration);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== Bank Transfer Payment System with AI Receipt Verification =====
let currentPaymentStep = 1;
let receiptFile = null;

function showFPXPayment() {
    // Reset to step 1
    currentPaymentStep = 1;
    receiptFile = null;
    goToStep(1);
    document.getElementById('fpx-modal').classList.remove('hidden');

    // Reset receipt preview
    const preview = document.getElementById('receipt-preview');
    const placeholder = document.getElementById('upload-placeholder');
    if (preview) {
        preview.classList.add('hidden');
        preview.src = '';
    }
    if (placeholder) placeholder.classList.remove('hidden');

    const verifyBtn = document.getElementById('verify-btn');
    if (verifyBtn) verifyBtn.disabled = true;
}

function closeFPXModal() {
    document.getElementById('fpx-modal').classList.add('hidden');
}

function goToStep(step) {
    currentPaymentStep = step;

    // Hide all steps
    document.querySelectorAll('.payment-step').forEach(s => s.classList.add('hidden'));

    // Show current step
    const stepElement = document.getElementById(`payment-step${step}`);
    if (stepElement) stepElement.classList.remove('hidden');

    // Update step indicators
    for (let i = 1; i <= 3; i++) {
        const indicator = document.getElementById(`step${i}`);
        if (indicator) {
            if (i <= step) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        }
    }
}

function copyBankAccount() {
    const account = document.getElementById('bank-account').textContent;
    navigator.clipboard.writeText(account).then(() => {
        showToast('账号已复制 ✓');
    });
}

function previewReceipt(event) {
    const file = event.target.files[0];
    if (file) {
        receiptFile = file;

        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('receipt-preview');
            const placeholder = document.getElementById('upload-placeholder');

            preview.src = e.target.result;
            preview.classList.remove('hidden');
            placeholder.classList.add('hidden');

            // Enable verify button
            document.getElementById('verify-btn').disabled = false;
        };
        reader.readAsDataURL(file);
    }
}

async function verifyReceipt() {
    if (!receiptFile) {
        showToast('请先上传收据截图');
        return;
    }

    // Go to step 3 (verification in progress)
    goToStep(3);

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('receipt', receiptFile);

        // Call backend AI verification API
        const response = await fetch(`${API_BASE}/payment/verify-receipt`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${state.token}`
            },
            body: formData
        });

        if (response.ok) {
            const result = await response.json();

            if (result.success) {
                // Verification successful
                document.getElementById('fpx-modal').classList.add('hidden');
                document.getElementById('payment-success').classList.remove('hidden');

                // Update local state
                if (state.user) {
                    state.user.is_premium = true;
                    localStorage.setItem('taromeet_user', JSON.stringify(state.user));
                }

                // Update UI
                const badge = document.querySelector('.membership-badge');
                if (badge) {
                    badge.textContent = 'Premium';
                    badge.classList.remove('free');
                    badge.classList.add('premium');
                }
            } else {
                // Verification failed
                document.getElementById('fpx-modal').classList.add('hidden');
                document.getElementById('failed-reason').textContent = result.message || '收据信息不符，请检查后重试';
                document.getElementById('payment-failed').classList.remove('hidden');
            }
        } else {
            // API error
            const error = await response.json();
            document.getElementById('fpx-modal').classList.add('hidden');
            document.getElementById('failed-reason').textContent = error.detail || '验证失败，请重试';
            document.getElementById('payment-failed').classList.remove('hidden');
        }
    } catch (error) {
        // Network error - show message
        document.getElementById('fpx-modal').classList.add('hidden');
        document.getElementById('failed-reason').textContent = '网络错误，请检查网络连接后重试';
        document.getElementById('payment-failed').classList.remove('hidden');
    }
}

function closePaymentSuccess() {
    document.getElementById('payment-success').classList.add('hidden');
    showScreen('home-screen');
    showToast('恭喜！您已成为 Premium 会员 🎉');
}

function closePaymentFailed() {
    document.getElementById('payment-failed').classList.add('hidden');
    // Re-open payment modal for retry
    showFPXPayment();
    goToStep(2);  // Go directly to upload step
}

// ===== Helper Functions for New Features =====

// FAQ Toggle for Help Center
function toggleFaq(element) {
    element.classList.toggle('open');
}

// Save Notification Settings
function saveNotificationSettings() {
    const settings = {
        mood: document.getElementById('mood-notify')?.checked || false,
        tarot: document.getElementById('tarot-notify')?.checked || false,
        diary: document.getElementById('diary-notify')?.checked || false,
        promo: document.getElementById('promo-notify')?.checked || false
    };
    localStorage.setItem('taromeet_notifications', JSON.stringify(settings));
    showToast('通知设置已保存');
}

// Load Notification Settings
function loadNotificationSettings() {
    const saved = localStorage.getItem('taromeet_notifications');
    if (saved) {
        const settings = JSON.parse(saved);
        if (document.getElementById('mood-notify')) {
            document.getElementById('mood-notify').checked = settings.mood;
        }
        if (document.getElementById('tarot-notify')) {
            document.getElementById('tarot-notify').checked = settings.tarot;
        }
        if (document.getElementById('diary-notify')) {
            document.getElementById('diary-notify').checked = settings.diary;
        }
        if (document.getElementById('promo-notify')) {
            document.getElementById('promo-notify').checked = settings.promo;
        }
    }
}

// Call on page load
document.addEventListener('DOMContentLoaded', loadNotificationSettings);
