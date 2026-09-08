/**
 * 🎓 CampusConnect — Student Dashboard Scripts
 * Extracted from dashboard.html inline <script>
 */

// 📱 Sidebar Toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar) sidebar.classList.toggle('show');
    if (overlay) overlay.classList.toggle('show');
}

// No-results helper
function checkEmpty(count) {
    const noRes = document.getElementById('noResults');
    if (noRes) {
        noRes.className = count === 0 ? 'text-center py-5 d-block' : 'd-none';
    }
}

// 🔍 Search
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', function () {
        const q = this.value.toLowerCase();
        const cards = document.querySelectorAll('.event-item');
        let visible = 0;

        cards.forEach(card => {
            const titleEl = card.querySelector('.event-title');
            const venueIcon = card.querySelector('.bi-geo-alt');
            const title = titleEl?.textContent?.toLowerCase() ?? '';
            const venue = venueIcon?.nextElementSibling?.textContent?.toLowerCase() ?? '';

            if (title.includes(q) || venue.includes(q)) {
                card.style.display = 'block';
                visible++;
            } else {
                card.style.display = 'none';
            }
        });
        checkEmpty(visible);
    });
}

// 🏷️ Category Filter
function filterCategory(cat, btn) {
    document.querySelectorAll('.sidebar .nav-link, .btn-filter-pill').forEach(l => l.classList.remove('active'));
    document.querySelectorAll(`.sidebar .nav-link[onclick*="'${cat}'"], .btn-filter-pill[onclick*="'${cat}'"]`).forEach(el => el.classList.add('active'));
    if (btn) btn.classList.add('active');

    if (window.innerWidth < 992) {
        const sidebar = document.getElementById('sidebar');
        if (sidebar && sidebar.classList.contains('show')) toggleSidebar();
    }

    const cards = document.querySelectorAll('.event-item');
    let visible = 0;

    cards.forEach((card, i) => {
        const cardCat = card.dataset.category;
        if (cat === 'all' || cardCat === cat) {
            card.style.display = 'block';
            card.style.animationDelay = `${Math.min(i, 12) * 0.04}s`;
            card.classList.remove('animate-in');
            requestAnimationFrame(() => card.classList.add('animate-in'));
            visible++;
        } else {
            card.style.display = 'none';
        }
    });

    checkEmpty(visible);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ⏳ Status Filter
function filterStatus(status, btn) {
    document.querySelectorAll('.sidebar .nav-link').forEach(l => l.classList.remove('active'));
    if (btn) btn.classList.add('active');

    if (window.innerWidth < 992) {
        const sidebar = document.getElementById('sidebar');
        if (sidebar && sidebar.classList.contains('show')) toggleSidebar();
    }

    const cards = document.querySelectorAll('.event-item');
    let visible = 0;

    cards.forEach((card, i) => {
        const badge = card.querySelector('.status-badge-target');
        const cardStatus = badge ? badge.getAttribute('data-status') : '';

        if (cardStatus === status) {
            card.style.display = 'block';
            card.style.animationDelay = `${Math.min(i, 12) * 0.04}s`;
            card.classList.remove('animate-in');
            requestAnimationFrame(() => card.classList.add('animate-in'));
            visible++;
        } else {
            card.style.display = 'none';
        }
    });
    checkEmpty(visible);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Modal Logic
function getDetailModal() {
    const modalEl = document.getElementById('eventDetailModal');
    if (!modalEl) return null;
    if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
        return bootstrap.Modal.getOrCreateInstance(modalEl);
    }
    return null;
}

function openDetailModal(btn) {
    const detailModal = getDetailModal();
    if (!detailModal) return;

    const title = btn.dataset.title;
    const desc = btn.dataset.desc;
    const date = btn.dataset.date;
    const endDate = btn.dataset.enddate;
    const time = btn.dataset.time;
    const endTime = btn.dataset.endtime;

    const titleEl = document.getElementById('detailTitle');
    if (titleEl) titleEl.innerText = title;
    const descEl = document.getElementById('detailDesc');
    if (descEl) descEl.innerText = desc;

    // Logic for Date Range Display
    let dateDisplay = `${date}`;
    if (endDate && endDate !== date) {
        dateDisplay += ` - ${endDate}`;
    }
    const dateEl = document.getElementById('detailDate');
    if (dateEl) dateEl.textContent = dateDisplay;

    // Logic for Time Range Display
    let timeDisplay = `${time}`;
    if (endTime) {
        timeDisplay += ` - ${endTime}`;
    }
    const timeEl = document.getElementById('detailTime');
    if (timeEl) timeEl.textContent = timeDisplay;

    const venueEl = document.getElementById('detailVenue');
    if (venueEl) venueEl.textContent = btn.dataset.venue;

    const cat = btn.dataset.cat;
    const catBadge = document.getElementById('detailCat');
    if (catBadge) {
        catBadge.textContent = cat;
        catBadge.className = 'badge-pill mb-2';
        if (cat === 'Technical') catBadge.classList.add('badge-tech');
        else if (cat === 'Cultural') catBadge.classList.add('badge-cultural');
        else if (cat === 'Sports') catBadge.classList.add('badge-sports');
        else if (cat === 'Workshop') catBadge.classList.add('badge-workshop');
        else if (cat === 'Seminar') catBadge.classList.add('badge-seminar');
        else catBadge.classList.add('glass');
    }

    const img = btn.dataset.img;
    const imgEl = document.getElementById('detailImg');
    const posterCol = document.getElementById('modalPosterCol');
    const detailsCol = document.getElementById('modalDetailsCol');

    if (imgEl) {
        imgEl.classList.remove('opacity-50', 'p-5');
        if (img && img !== 'null' && img.trim() !== '') {
            imgEl.src = img;
            imgEl.style.display = 'block';
            if (posterCol) {
                posterCol.style.display = 'flex';
                posterCol.style.setProperty('display', 'flex', 'important');
                posterCol.style.width = '';
            }
            if (detailsCol) detailsCol.className = 'flex-grow-1 overflow-y-auto custom-scrollbar';
        } else {
            imgEl.style.display = 'none';
            if (posterCol) posterCol.style.setProperty('display', 'none', 'important');
            if (detailsCol) detailsCol.className = 'flex-grow-1 overflow-y-auto custom-scrollbar';
        }
    }

    const link = btn.dataset.link;
    const btnEl = document.getElementById('detailLink');
    const calBtn = document.getElementById('calendarBtn');
    const qrContainer = document.getElementById('qrCodeContainer');

    if (qrContainer) {
        const scanText = document.createElement('small');
        scanText.className = 'text-muted d-block mb-3';
        scanText.textContent = 'Scan to Register';
        qrContainer.innerHTML = '';
        qrContainer.appendChild(scanText);
        qrContainer.style.display = 'none';
    }

    if (link) {
        const eventId = btn.dataset.id;
        if (btnEl) {
            btnEl.href = `/student/register-external/${eventId}`;
            btnEl.target = "_blank";
            btnEl.classList.remove('d-none');
            btnEl.classList.add('d-block');
        }

        if (qrContainer) {
            if (typeof generateQRCode === 'function') {
                generateQRCode('qrCodeContainer', link);
            }
            qrContainer.style.display = 'block';
        }
    } else if (btnEl) {
        btnEl.classList.remove('d-block');
        btnEl.classList.add('d-none');
    }

    if (calBtn) {
        calBtn.onclick = () => {
            if (typeof downloadICS === 'function') {
                downloadICS(title, desc, date, time, btn.dataset.venue);
            }
        };
    }

    detailModal.show();
}

// Auto-open from URL + Skeleton swap
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const openId = params.get('open');
    if (openId) {
        const sanitizedId = CSS.escape(openId);
        const btn = document.querySelector(`.event-card[data-id="${sanitizedId}"]`);
        if (btn) openDetailModal(btn);
    }

    // Skeleton loader → real content swap
    const skeletonGrid = document.getElementById('skeletonGrid');
    const eventsGrid = document.getElementById('eventsGrid');
    if (skeletonGrid && eventsGrid) {
        skeletonGrid.classList.add('hidden');
        eventsGrid.classList.remove('loading');
    }
});
