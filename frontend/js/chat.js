const API_URL = CONFIG.API_URL;
let currentUser = null;
let currentChat = null;
let ws = null;
let chats = {};
let users = {};
let allUsers = [];
let reconnectAttempts = 0;
let maxReconnectAttempts = 10;
let reconnectDelay = 1000;

class ChatApp {
    constructor() {
        this.bindEvents();
        this.checkAuth();
    }

    bindEvents() {
        document.getElementById('login-btn').addEventListener('click', () => this.login());
        document.getElementById('message-form').addEventListener('submit', (e) => this.sendMessage(e));
        document.getElementById('create-chat-btn').addEventListener('click', () => this.createChat());
        document.getElementById('add-participant-btn').addEventListener('click', () => this.addParticipant());
        
        const messageInput = document.getElementById('message-input');
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage(e);
            }
        });
        messageInput.addEventListener('input', () => {
            messageInput.style.height = 'auto';
            messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
        });

        document.getElementById('participantsModal').addEventListener('show.bs.modal', () => {
            this.loadParticipants();
            this.loadAllUsers();
        });
    }

    checkAuth() {
        const savedUser = localStorage.getItem('chatUser');
        if (savedUser) {
            currentUser = JSON.parse(savedUser);
            this.showChatScreen();
            this.connectWebSocket();
            this.loadChats();
        }
    }

    async checkServerConnection() {
        try {
            const response = await fetch(`${API_URL}/health`, { 
                method: 'GET',
                signal: AbortSignal.timeout(5000)
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    async login() {
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const loginBtn = document.getElementById('login-btn');

        if (!username || !email) {
            this.showError('Заполните все поля');
            return;
        }

        if (username.length < 3) {
            this.showError('Имя должно быть не менее 3 символов');
            return;
        }

        loginBtn.disabled = true;
        loginBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Проверка сервера...';

        const serverAvailable = await this.checkServerConnection();
        if (!serverAvailable) {
            this.showError(`Сервер недоступен на ${API_URL}. Запустите бэкенд: make app`);
            loginBtn.disabled = false;
            loginBtn.innerHTML = '<i class="bi bi-box-arrow-in-right me-2"></i>Войти';
            return;
        }

        loginBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Вход...';

        try {
            const response = await fetch(`${API_URL}/users/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password: 'default' })
            });

            if (response.ok) {
                const user = await response.json();
                currentUser = user;
                localStorage.setItem('chatUser', JSON.stringify(user));
                this.showChatScreen();
                this.connectWebSocket();
                this.loadChats();
            } else {
                try {
                    const existingUsers = await fetch(`${API_URL}/users/`).then(r => r.json());
                    const existing = existingUsers.find(u => u.email === email || u.username === username);
                    
                    if (existing) {
                        currentUser = existing;
                        localStorage.setItem('chatUser', JSON.stringify(existing));
                        this.showChatScreen();
                        this.connectWebSocket();
                        this.loadChats();
                    } else {
                        const error = await response.json();
                        this.showError(error.detail || 'Ошибка авторизации');
                    }
                } catch (e) {
                    this.showError('Не удалось найти пользователя. Проверьте подключение к серверу.');
                }
            }
        } catch (error) {
            this.showError('Ошибка соединения: ' + error.message);
        } finally {
            loginBtn.disabled = false;
            loginBtn.innerHTML = '<i class="bi bi-box-arrow-in-right me-2"></i>Войти';
        }
    }

    showError(message) {
        const errorEl = document.getElementById('auth-error');
        errorEl.textContent = message;
        errorEl.classList.remove('d-none');
        setTimeout(() => errorEl.classList.add('d-none'), 5000);
    }

    showChatScreen() {
        document.getElementById('auth-screen').classList.add('d-none');
        document.getElementById('chat-screen').classList.remove('d-none');
        document.getElementById('current-username').textContent = currentUser.username;
    }

    updateWsStatus(connected) {
        const statusEl = document.getElementById('ws-status');
        if (connected) {
            statusEl.innerHTML = '<i class="bi bi-circle-fill me-1 text-success" style="font-size: 8px;"></i>Подключено';
        } else {
            statusEl.innerHTML = '<i class="bi bi-circle-fill me-1 text-danger" style="font-size: 8px;"></i>Отключено';
        }
    }

    connectWebSocket() {
        if (reconnectAttempts >= maxReconnectAttempts) {
            this.showToast('Ошибка', 'Не удалось подключиться к серверу. Обновите страницу.');
            this.updateWsStatus(false);
            return;
        }

        const wsUrl = `${CONFIG.WS_URL}/ws/${currentUser.id}`;
        ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            console.log('WebSocket connected');
            reconnectAttempts = 0;
            reconnectDelay = 1000;
            this.updateWsStatus(true);
            this.showToast('Подключено', 'Соединение установлено');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateWsStatus(false);
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.updateWsStatus(false);
            reconnectAttempts++;
            const delay = Math.min(reconnectDelay * Math.pow(2, reconnectAttempts - 1), 30000);
            setTimeout(() => this.connectWebSocket(), delay);
        };
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'message':
                this.receiveMessage(data);
                break;
            case 'new_chat':
                this.loadChats();
                this.showToast('Новый чат', data.title);
                break;
            case 'joined':
                console.log('Joined chat:', data.chat_id);
                break;
            case 'participant_added':
                this.loadChats();
                this.showToast('Участник добавлен', `Пользователь добавлен в чат`);
                break;
            case 'error':
                this.showToast('Ошибка', data.message);
                break;
        }
    }

    async loadChats() {
        try {
            const response = await fetch(`${API_URL}/chats/`);
            if (response.ok) {
                const chatsList = await response.json();
                this.renderChats(chatsList);
            }
        } catch (error) {
            console.error('Error loading chats:', error);
        }
    }

    renderChats(chatsList) {
        const container = document.getElementById('chats-list');
        container.innerHTML = '';

        if (chatsList.length === 0) {
            container.innerHTML = '<div class="text-muted text-center p-3">Нет чатов</div>';
            return;
        }

        chatsList.forEach(chat => {
            chats[chat.id] = chat;
            const chatEl = document.createElement('div');
            chatEl.className = `chat-item ${currentChat === chat.id ? 'active' : ''}`;
            chatEl.innerHTML = `
                <div class="d-flex align-items-center">
                    <div class="chat-avatar me-2">
                        <i class="bi bi-chat-fill"></i>
                    </div>
                    <div>
                        <div class="fw-bold">${this.escapeHtml(chat.title)}</div>
                        <small class="text-muted">${chat.participants.length} участников</small>
                    </div>
                </div>
            `;
            chatEl.addEventListener('click', (e) => this.selectChat(chat.id, e));
            container.appendChild(chatEl);
        });
    }

    async selectChat(chatId, e) {
        currentChat = chatId;
        
        document.querySelectorAll('.chat-item').forEach(el => el.classList.remove('active'));
        if (e && e.currentTarget) {
            e.currentTarget.classList.add('active');
        }

        const chat = chats[chatId];
        if (chat) {
            document.getElementById('chat-title').textContent = chat.title;
            document.getElementById('chat-participants-count').textContent = `${chat.participants.length} участников`;
        }

        document.getElementById('no-chat-selected').classList.add('d-none');
        document.getElementById('chat-container').classList.remove('d-none');

        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'join_chat', chat_id: chatId }));
        }

        await this.loadMessages(chatId);
    }

    async loadMessages(chatId) {
        try {
            const response = await fetch(`${API_URL}/messages/chat/${chatId}`);
            if (response.ok) {
                const messages = await response.json();
                await this.loadUsers();
                this.renderMessages(messages);
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    async loadUsers() {
        try {
            const response = await fetch(`${API_URL}/users/`);
            if (response.ok) {
                allUsers = await response.json();
                allUsers.forEach(u => {
                    users[u.id] = u;
                });
            }
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }

    renderMessages(messagesList) {
        const container = document.getElementById('messages');
        container.innerHTML = '';

        messagesList.forEach(msg => {
            this.appendMessage(msg, false);
        });

        container.scrollTop = container.scrollHeight;
    }

    appendMessage(msg, isNew = true) {
        const container = document.getElementById('messages');
        const isSent = msg.sender_id === currentUser.id;
        const senderName = users[msg.sender_id]?.username || msg.sender_id.substring(0, 8);
        
        const msgEl = document.createElement('div');
        msgEl.className = `message ${isSent ? 'sent' : 'received'} ${isNew ? 'new' : ''}`;
        msgEl.innerHTML = `
            ${!isSent ? `<div class="sender">${this.escapeHtml(senderName)}</div>` : ''}
            <div class="text">${this.escapeHtml(msg.text)}</div>
            <div class="time">${this.formatTime(msg.timestamp)}</div>
        `;
        container.appendChild(msgEl);
        container.scrollTop = container.scrollHeight;
    }

    receiveMessage(data) {
        if (currentChat === data.chat_id) {
            this.appendMessage({
                sender_id: data.sender_id,
                text: data.text,
                timestamp: new Date().toISOString()
            });
        }
    }

    async sendMessage(e) {
        e.preventDefault();
        
        const input = document.getElementById('message-input');
        const text = input.value.trim();

        if (!text || !currentChat) return;

        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'message',
                chat_id: currentChat,
                text: text
            }));

            input.value = '';
            input.style.height = 'auto';
        } else {
            this.showToast('Ошибка', 'Нет соединения с сервером');
        }
    }

    async createChat() {
        const title = document.getElementById('chat-name').value.trim();
        if (!title) {
            this.showToast('Ошибка', 'Введите название чата');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/chats/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: title,
                    type: 'group',
                    creator_id: currentUser.id,
                    participants: [currentUser.id]
                })
            });

            if (response.ok) {
                const chat = await response.json();
                document.getElementById('chat-name').value = '';
                bootstrap.Modal.getInstance(document.getElementById('newChatModal')).hide();
                await this.loadChats();
                this.selectChat(chat.id);
                this.showToast('Чат создан', chat.title);
            } else {
                const error = await response.json();
                this.showToast('Ошибка', error.detail || 'Не удалось создать чат');
            }
        } catch (error) {
            this.showToast('Ошибка', error.message);
        }
    }

    async loadParticipants() {
        if (!currentChat) return;
        
        try {
            const response = await fetch(`${API_URL}/chats/${currentChat}/participants`);
            if (response.ok) {
                const participants = await response.json();
                this.renderParticipants(participants);
            }
        } catch (error) {
            console.error('Error loading participants:', error);
        }
    }

    renderParticipants(participants) {
        const container = document.getElementById('participants-list');
        container.innerHTML = '';

        participants.forEach(p => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <span>${this.escapeHtml(p.username || p.user_id.substring(0, 8))}</span>
                ${p.user_id === currentUser.id ? '<span class="badge bg-primary">Вы</span>' : ''}
            `;
            container.appendChild(li);
        });
    }

    async loadAllUsers() {
        await this.loadUsers();
        
        const container = document.getElementById('all-users-list');
        container.innerHTML = '';

        const chat = chats[currentChat];
        const participantIds = chat ? chat.participants : [];

        allUsers.forEach(u => {
            const isInChat = participantIds.includes(u.id);
            const div = document.createElement('div');
            div.className = 'list-group-item d-flex justify-content-between align-items-center';
            div.innerHTML = `
                <span>${this.escapeHtml(u.username)} <small class="text-muted">(${u.email})</small></span>
                ${!isInChat ? `<button class="btn btn-sm btn-outline-primary add-user-btn" data-user-id="${u.id}">+</button>` : '<span class="badge bg-success">В чате</span>'}
            `;
            container.appendChild(div);
        });

        document.querySelectorAll('.add-user-btn').forEach(btn => {
            btn.addEventListener('click', () => this.addUserToChat(btn.dataset.userId));
        });
    }

    async addUserToChat(userId) {
        if (!currentChat) return;

        try {
            const response = await fetch(`${API_URL}/chats/${currentChat}/participants`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId })
            });

            if (response.ok) {
                this.showToast('Успешно', 'Пользователь добавлен');
                await this.loadChats();
                await this.loadParticipants();
                await this.loadAllUsers();
            } else {
                const error = await response.json();
                this.showToast('Ошибка', error.detail || 'Не удалось добавить');
            }
        } catch (error) {
            this.showToast('Ошибка', error.message);
        }
    }

    async addParticipant() {
        const input = document.getElementById('add-participant-input');
        const searchTerm = input.value.trim();
        
        if (!searchTerm || !currentChat) {
            this.showToast('Ошибка', 'Введите email или имя пользователя');
            return;
        }

        const user = allUsers.find(u => 
            u.email.toLowerCase() === searchTerm.toLowerCase() || 
            u.username.toLowerCase() === searchTerm.toLowerCase()
        );

        if (!user) {
            this.showToast('Ошибка', 'Пользователь не найден');
            return;
        }

        await this.addUserToChat(user.id);
        input.value = '';
    }

    showToast(title, message) {
        document.getElementById('toast-title').textContent = title;
        document.getElementById('toast-message').textContent = message;
        const toast = new bootstrap.Toast(document.getElementById('notification-toast'));
        toast.show();
    }

    formatTime(timestamp) {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
