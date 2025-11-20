// static/js/reminder-popup.js
// Nhắc nhở thông minh – chạy hoàn hảo khi tách file riêng

(() => {
    'use strict';

    // Lấy dữ liệu từ Flask (đã truyền qua window.APP_EVENTS)
    const events = window.APP_EVENTS || [];
    if (events.length === 0) return;

    let reminderTimeout = null;

    // Chuyển giờ:phút → số phút từ 00:00
    function timeToMinutes(timeStr) {
        if (!timeStr) return null;
        const [h, m] = timeStr.split(':').map(Number);
        return h * 60 + m;
    }

    // Kiểm tra nhắc nhở
    function checkReminders() {
    const now = new Date();
    const currentMinutes = now.getHours() * 60 + now.getMinutes();

    events.forEach(event => {
        // Bỏ qua nếu đã hoàn thành hoặc đã nhắc rồi
        if (event.completed || localStorage.getItem('reminded_' + event.id)) {
            return;
        }

        const timeRange = (event.time || '').trim();
        if (!timeRange) return;

        const startTime = timeRange.split(' - ')[0].trim(); // "19:00"
        const reminderMinutes = parseInt(event.reminder_minutes) || 0;
        if (!startTime || reminderMinutes === 0) return;

        const eventMinutes = timeToMinutes(startTime);
        if (eventMinutes === null) return;

        const triggerTime = eventMinutes - reminderMinutes; // Ví dụ: 19:00 - 15 = 18:45

        // Điều kiện CHUẨN: hiện tại đã qua giờ nhắc, nhưng chưa qua giờ bắt đầu
        const isInReminderWindow = currentMinutes >= triggerTime && currentMinutes < eventMinutes;

        if (isInReminderWindow) {
            showReminderPopup(event);
            localStorage.setItem('reminded_' + event.id, 'true');
            console.log(`Đã nhắc: ${event.name} - lúc ${startTime} (nhắc trước ${reminderMinutes} phút)`);
        }
    });
}

    // Hiển thị popup nhắc nhở
    function showReminderPopup(event) {
        const title = document.getElementById('reminder-title');
        const detail = document.getElementById('reminder-detail');
        const modal = document.getElementById('reminder-modal');

        if (!title || !detail || !modal) return;

        title.textContent = event.name || 'Sự kiện';
        detail.innerHTML = `
            <strong>Thời gian:</strong> ${event.time || 'Không rõ'}<br>
            <strong>Địa điểm:</strong> ${event.location || 'Không có'}<br>
            <strong>Nhắc trước:</strong> ${event.reminder_minutes} phút
        `;

        modal.classList.add('show');

        // Phát âm thanh
        const sound = document.getElementById('reminder-sound');
        if (sound) sound.play().catch(() => {});

        // Tự đóng sau 30 giây
        clearTimeout(reminderTimeout);
        reminderTimeout = setTimeout(() => modal.classList.remove('show'), 30000);
    }

    // Đóng popup
    window.closeReminder = function() {
        const modal = document.getElementById('reminder-modal');
        if (modal) modal.classList.remove('show');
        clearTimeout(reminderTimeout);
    };

    // Khởi động hệ thống nhắc nhở
    setInterval(checkReminders, 60000);  // Mỗi phút kiểm tra 1 lần
    checkReminders();                    // Kiểm tra ngay khi load
})();