
    function toggleChat() {
        const chatbox = document.getElementById('ai-chatbox');
        chatbox.classList.toggle('open');
    }

    function addMessage(text, type = 'bot') {
        const messages = document.getElementById('ai-messages');
        const div = document.createElement('div');
        div.className = `ai-message ${type}`;
        div.innerHTML = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
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
                addMessage(`✓ Đã tạo: <b>${data.event.event}</b><br>${data.event.start_time.replace('T', ' ')} ${data.event.location ? 'tại ' + data.event.location : ''}`, 'success');
                setTimeout(() => location.reload(), 1500); // Reload để thấy sự kiện mới
                toggleChat()
            } else {
                addMessage(` ${data.message || 'Không hiểu yêu cầu'}`, 'bot');
            }
        } catch (err) {
            document.querySelector('.ai-messages > .ai-message:last-child').remove();
            addMessage('Lỗi kết nối. Vui lòng thử lại!', 'bot');
        }
    }

    // Mở chat tự động lần đầu (tùy chọn)
    window.onload = () => {
        // toggleChat(); // Bỏ comment nếu muốn tự mở
    }