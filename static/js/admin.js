/* =============================================
   VoidCloth - Admin JavaScript
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {

    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar-wrapper');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Auto-dismiss alerts
    document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // Mark active sidebar link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.admin-sidebar .nav-link').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Confirm dialogs
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            const msg = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });

    // File input image preview
    document.querySelectorAll('input[type=file][data-preview]').forEach(function (input) {
        input.addEventListener('change', function () {
            const previewId = this.getAttribute('data-preview');
            const preview = document.getElementById(previewId);
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // DataTable-like search on tables
    const tableSearch = document.getElementById('tableSearch');
    if (tableSearch) {
        tableSearch.addEventListener('keyup', function () {
            const query = this.value.toLowerCase();
            document.querySelectorAll('table tbody tr').forEach(function (row) {
                row.style.display = row.textContent.toLowerCase().includes(query) ? '' : 'none';
            });
        });
    }

    // Status color badge mapper
    const statusMap = {
        'pending': 'warning',
        'confirmed': 'info',
        'packed': 'primary',
        'shipped': 'info',
        'delivered': 'success',
        'cancelled': 'danger',
        'approved': 'success',
        'rejected': 'danger',
        'active': 'success',
        'inactive': 'secondary',
    };
    document.querySelectorAll('[data-status]').forEach(function (el) {
        const status = el.getAttribute('data-status').toLowerCase();
        const cls = statusMap[status] || 'secondary';
        el.classList.add('badge', `bg-${cls}`);
        el.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    });

});
