/**
 * 🎓 CampusConnect - Main Application Scripts
 * Premium UI Package 2026
 */

document.addEventListener('DOMContentLoaded', () => {
    // Check for Flash Messages from server
    const successMsg = document.getElementById('flashSuccessMsg')?.value;
    const errorMsg = document.getElementById('flashErrorMsg')?.value;

    if (successMsg) showToast(successMsg, 'success');
    if (errorMsg) showToast(errorMsg, 'error');

    // Initialize Tooltips/Popovers if any (Bootstrap)

    // Global Button Loading State Handler
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function () {
            const btn = this.querySelector('button[type="submit"]');
            if (btn && !btn.classList.contains('no-loader')) {
                btn.classList.add('btn-loading');
            }
        });
    });

    // ⌘K / Ctrl+K Keyboard Shortcut → Focus Search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
                searchInput.select();
            }
        });
    }
});

/**
 * Custom Toast Notification System
 * @param {string} msg - The message to display
 * @param {string} type - 'success', 'error', 'info'
 */
function showToast(msg, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast-item ${type}`;

    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-exclamation-circle-fill',
        info: 'bi-info-circle-fill'
    };

    // Build icon
    const icon = document.createElement('i');
    icon.className = `bi ${icons[type] || icons.info} toast-icon`;

    // Build message content (textContent to prevent XSS)
    const content = document.createElement('div');
    content.className = 'toast-content';
    content.textContent = msg;

    // Build close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'toast-close';
    const closeIcon = document.createElement('i');
    closeIcon.className = 'bi bi-x';
    closeBtn.appendChild(closeIcon);
    closeBtn.addEventListener('click', function () {
        toast.classList.add('hide');
        setTimeout(() => toast.remove(), 300);
    });

    toast.appendChild(icon);
    toast.appendChild(content);
    toast.appendChild(closeBtn);

    container.appendChild(toast);

    // Auto remove after 5s
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.add('hide');
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

/**
 * Generate and Download .ics file for an event
 */
function downloadICS(title, desc, dateStr, timeStr, venue) {
    // Basic .ics format
    // dateStr example: "Tue, Feb 17, 2026"
    // timeStr example: "1:30 PM"

    // Explicit parsing: handles "Tue, Feb 17, 2026", "Tue, Feb 17", "Feb 17 2026", etc.
    const months = { Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5, Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11 };
    const currentYear = new Date().getFullYear();
    const dateParts = (dateStr || '').replace(/,/g, '').trim().split(/\s+/);
    
    let monthIndex = 0;
    let day = 1;
    let year = currentYear;

    if (dateParts.length >= 4) {
        // e.g. "Tue Feb 17 2026"
        monthIndex = months[dateParts[1]] !== undefined ? months[dateParts[1]] : 0;
        day = parseInt(dateParts[2], 10) || 1;
        year = parseInt(dateParts[3], 10) || currentYear;
    } else if (dateParts.length === 3) {
        if (months[dateParts[0]] !== undefined) {
            // "Feb 17 2026"
            monthIndex = months[dateParts[0]];
            day = parseInt(dateParts[1], 10) || 1;
            year = parseInt(dateParts[2], 10) || currentYear;
        } else {
            // "Tue Feb 17"
            monthIndex = months[dateParts[1]] !== undefined ? months[dateParts[1]] : 0;
            day = parseInt(dateParts[2], 10) || 1;
            year = currentYear;
        }
    } else if (dateParts.length === 2) {
        // e.g. "Feb 17"
        monthIndex = months[dateParts[0]] !== undefined ? months[dateParts[0]] : 0;
        day = parseInt(dateParts[1], 10) || 1;
        year = currentYear;
    }

    const timeParts = (timeStr || '').trim().match(/^(\d{1,2}):(\d{2})\s*(AM|PM)?$/i);
    let hours = timeParts ? parseInt(timeParts[1], 10) : 10;
    const minutes = timeParts ? parseInt(timeParts[2], 10) : 0;
    if (timeParts && timeParts[3]) {
        const period = timeParts[3].toUpperCase();
        if (period === 'PM' && hours < 12) hours += 12;
        if (period === 'AM' && hours === 12) hours = 0;
    }

    const start = new Date(year, monthIndex, day, hours, minutes);
    const end = new Date(start.getTime() + 2 * 60 * 60 * 1000); // Default 2 hours

    const formatDate = (date) => {
        const pad = (num) => String(num).padStart(2, '0');
        return `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}T${pad(date.getHours())}${pad(date.getMinutes())}${pad(date.getSeconds())}`;
    };

    const safeTitle = (title || 'Campus Event').trim();
    const safeDesc = (desc || '').replace(/\n/g, '\\n');
    const safeVenue = (venue || 'Campus Venue').trim();

    const icsContent = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//CampusConnect//Event Manager//EN',
        'BEGIN:VEVENT',
        `SUMMARY:${safeTitle}`,
        `DESCRIPTION:${safeDesc}`,
        `LOCATION:${safeVenue}`,
        `DTSTART:${formatDate(start)}`,
        `DTEND:${formatDate(end)}`,
        'STATUS:CONFIRMED',
        'END:VEVENT',
        'END:VCALENDAR'
    ].join('\r\n');

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.setAttribute('download', `${safeTitle.replace(/\s+/g, '_')}.ics`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(link.href);

    showToast('Event added to prep-list! (ICS Downloaded)', 'success');
}

/**
 * Generate QR Code using a public API
 */
function generateQRCode(containerId, url) {
    const container = document.getElementById(containerId);
    if (!container || !url) return;

    const qrWrapper = document.createElement('div');
    qrWrapper.className = 'qr-container';
    const qrImg = document.createElement('img');
    qrImg.className = 'qr-img-override';
    qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(url)}`;
    qrImg.alt = 'Registration QR Code';
    qrWrapper.appendChild(qrImg);

    container.innerHTML = ''; // Clear container
    container.appendChild(qrWrapper);
}


