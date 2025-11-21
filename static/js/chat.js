
function toggleChat() {
    const chatbox = document.getElementById('ai-chatbox');
    chatbox.classList.toggle('open');

    // Lưu trạng thái chat vào localStorage
    if (chatbox.classList.contains('open')) {
        localStorage.setItem('chatOpen', 'true');
    } else {
        localStorage.removeItem('chatOpen');
    }
}

function addMessage(text, type = 'bot') {
    const messages = document.getElementById('ai-messages');
    const div = document.createElement('div');
    div.className = `ai-message ${type}`;
    div.innerHTML = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

// Hàm cập nhật danh sách sự kiện không reload
async function refreshEventsList() {
    try {
        const currentFilter = new URLSearchParams(window.location.search).get('filter') || 'all';
        const res = await fetch(`/api/events?filter=${currentFilter}`);
        const data = await res.json();

        // Cập nhật HTML của danh sách sự kiện
        const eventsContainer = document.querySelector('.events-container');
        if (eventsContainer && data.html) {
            eventsContainer.innerHTML = data.html;
        }
    } catch (err) {
        console.error('Lỗi khi refresh danh sách:', err);
    }
}

async function sendMessage(e) {
    e.preventDefault();
    const input = document.getElementById('ai-input');
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    input.value = '';

    addMessage('<i>Đang xử lý...</i>', 'bot');

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();

        // Xóa "Đang xử lý..."
        document.querySelector('.ai-messages > .ai-message:last-child').remove();

        if (data.success) {
            const event = data.event;
            addMessage(`
                ✓ <b>Đã tạo sự kiện thành công!</b><br>
                📅 ${event.event}<br>
                🕒 ${event.start_time.replace('T', ' ')}<br>
                ${event.location ? '📍 ' + event.location : ''}
            `, 'success');

            // Cập nhật danh sách sự kiện KHÔNG reload trang
            await refreshEventsList();

            // Hiển thị thông báo nhẹ
//            showNotification('Sự kiện mới đã được thêm!');

        } else {
            addMessage(`❌ ${data.message || 'Không hiểu yêu cầu. Vui lòng thử lại!'}`, 'bot');
        }
    } catch (err) {
        document.querySelector('.ai-messages > .ai-message:last-child')?.remove();
        addMessage('⚠️ Lỗi kết nối. Vui lòng thử lại!', 'bot');
    }
}

// Hàm hiển thị thông báo nhẹ
function showNotification(text) {
    const notification = document.createElement('div');
    notification.className = 'notification-toast';
    notification.textContent = text;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// CSS animation cho notification
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Khôi phục trạng thái chat khi load trang
window.onload = () => {
    if (localStorage.getItem('chatOpen') === 'true') {
        const chatbox = document.getElementById('ai-chatbox');
        if (chatbox) {
            chatbox.classList.add('open');
        }
    }
}