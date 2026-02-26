/**
 * 🎓 CampusConnect — Admin Dashboard Scripts
 * Extracted from admin_dashboard.html inline <script>
 *
 * Usage: Before loading this file, define window.__adminData with:
 *   - csrfName:  the CSRF parameter name
 *   - csrfToken: the CSRF token value
 *   - categoryCounts: { Technical: n, Cultural: n, ... }
 */

// 📱 Sidebar Toggle Function
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar) sidebar.classList.toggle('show');
    if (overlay) overlay.classList.toggle('show');
}

// 🔍 Search Functionality & Shortcuts
const searchInput = document.getElementById('searchInput');

// Command+K or Ctrl+K to focus search
if (searchInput) {
    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
        }
    });
}

// 🏷️ Category Filter
function filterCategory(category, btn) {
    // Update Active State
    document.querySelectorAll('.sidebar .nav-link').forEach(l => l.classList.remove('active'));
    btn.classList.add('active');

    if (window.innerWidth < 992) toggleSidebar();

    let rows = document.querySelectorAll('#eventsTable tbody tr');
    rows.forEach(row => {
        let rowCategory = row.getAttribute('data-category');
        // Handle empty rows
        if (row.querySelector('td[colspan]')) return;

        if (category === 'all' || rowCategory === category) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// ⏳ Status Filter
function filterStatus(status, btn) {
    // Update Active State
    document.querySelectorAll('.sidebar .nav-link').forEach(l => l.classList.remove('active'));
    btn.classList.add('active');

    if (window.innerWidth < 992) toggleSidebar();

    let rows = document.querySelectorAll('#eventsTable tbody tr');
    rows.forEach(row => {
        let rowStatus = row.getAttribute('data-status');
        // Handle empty rows
        if (row.querySelector('td[colspan]')) return;

        if (rowStatus === status) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// 📝 Edit Modal Populate
const editModalEl = document.getElementById('editEventModal');
const editModal = editModalEl ? new bootstrap.Modal(editModalEl) : null;

function openEditModal(btn) {
    if (!editModal) return;
    document.getElementById('editId').value = btn.dataset.id;
    document.getElementById('editTitle').value = btn.dataset.title;
    document.getElementById('editCategory').value = btn.dataset.category;
    document.getElementById('editVenue').value = btn.dataset.venue;
    document.getElementById('editDesc').value = btn.dataset.desc;
    document.getElementById('editDateTime').value = btn.dataset.datetime;
    document.getElementById('editEndDateTime').value = btn.dataset.enddatetime || ''; // Handle null safely
    document.getElementById('editLink').value = btn.dataset.link || '';
    document.getElementById('editResponsesLink').value = btn.dataset.responses || '';
    document.getElementById('editCapacity').value = btn.dataset.capacity || '';

    // Show existing image preview if it exists
    const previewImg = document.getElementById('editPreviewImg');
    const previewBox = document.getElementById('editPreviewBox');
    const uploadZone = document.getElementById('editUploadZone');

    if (btn.dataset.image) {
        previewImg.src = btn.dataset.image;
        previewBox.style.display = 'flex';
        uploadZone.style.display = 'none';
    } else {
        previewImg.src = '';
        previewBox.style.display = 'none';
        uploadZone.style.display = 'flex';
    }

    editModal.show();
}

// 🗑️ Delete Logic — reuses a single form to avoid DOM accumulation
let pendingDeleteForm = null;

function setDeleteId(id) {
    // Clean up any previous form
    if (pendingDeleteForm && pendingDeleteForm.parentNode) {
        pendingDeleteForm.remove();
    }

    const data = window.__adminData || {};
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/admin/delete-event/' + id;
    form.style.display = 'none';

    if (data.csrfName && data.csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = data.csrfName;
        csrfInput.value = data.csrfToken;
        form.appendChild(csrfInput);
    }

    document.body.appendChild(form);
    pendingDeleteForm = form;

    const confirmBtn = document.getElementById('confirmDeleteBtn');
    if (confirmBtn) {
        confirmBtn.onclick = (e) => {
            e.preventDefault();
            form.submit();
        };
    }
}

// 📊 Chart + Count-Up + Upload — runs on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
    const data = window.__adminData || {};

    // 📊 Chart Logic
    const ctx = document.getElementById('categoryChart');
    if (ctx) {
        const categoryCounts = data.categoryCounts || {};
        const labels = ['Technical', 'Cultural', 'Sports', 'Workshop', 'Seminar'];
        const chartData = labels.map(l => categoryCounts[l] || 0);
        const colors = ['#7C3AED', '#06B6D4', '#10B981', '#F59E0B', '#EC4899'];
        const total = chartData.reduce((a, b) => a + b, 0);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: chartData,
                    backgroundColor: colors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 600,
                    easing: 'easeOutQuart'
                },
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#7A7A9A', usePointStyle: true, boxWidth: 8 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const pct = total > 0 ? Math.round(context.parsed / total * 100) : 0;
                                return ` ${context.label}: ${context.parsed} (${pct}%)`;
                            }
                        }
                    }
                },
                cutout: '75%'
            }
        });
    }

    // 📊 Stat Number Count-Up Animation
    const counters = document.querySelectorAll('[data-countup]');
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-countup') || 0;
        if (target <= 0) { counter.textContent = 0; return; }
        const duration = 1000;
        const start = performance.now();
        function step(now) {
            const progress = Math.min((now - start) / duration, 1);
            counter.textContent = Math.floor(progress * target);
            if (progress < 1) requestAnimationFrame(step);
            else counter.textContent = target;
        }
        requestAnimationFrame(step);
    });

    // 📂 Custom Drag and Drop JS
    function initUploadZone(zoneId, inputId, previewBoxId, previewImgId) {
        const zone = document.getElementById(zoneId);
        const input = document.getElementById(inputId);
        const previewBox = document.getElementById(previewBoxId);
        const previewImg = document.getElementById(previewImgId);
        if (!zone || !input) return;

        zone.addEventListener('click', () => input.click());

        input.addEventListener('change', e => {
            if (e.target.files[0]) showPreview(e.target.files[0]);
        });
        zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-active'); });
        zone.addEventListener('dragleave', () => zone.classList.remove('drag-active'));
        zone.addEventListener('drop', e => {
            e.preventDefault(); zone.classList.remove('drag-active');
            const file = e.dataTransfer.files[0];
            if (file) {
                const dt = new DataTransfer(); dt.items.add(file);
                input.files = dt.files;
                showPreview(file);
            }
        });

        function showPreview(file) {
            const reader = new FileReader();
            reader.onload = e => {
                previewImg.src = e.target.result;
                previewBox.style.display = 'flex';
                zone.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    }

    initUploadZone('createUploadZone', 'createImageFile', 'createPreviewBox', 'createPreviewImg');
    initUploadZone('editUploadZone', 'editImageFile', 'editPreviewBox', 'editPreviewImg');

    window.clearCreateBanner = function () {
        document.getElementById('createImageFile').value = '';
        document.getElementById('createPreviewBox').style.display = 'none';
        document.getElementById('createUploadZone').style.display = 'flex';
    };

    window.clearEditBanner = function () {
        document.getElementById('editImageFile').value = '';
        document.getElementById('editPreviewBox').style.display = 'none';
        document.getElementById('editUploadZone').style.display = 'flex';
    };
});
