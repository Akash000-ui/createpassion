/* =============================================
   VoidCloth - Main JavaScript
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 4 seconds
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 4000);
    });

    // Add to cart animation feedback
    document.querySelectorAll('.add-to-cart-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const original = this.innerHTML;
            this.innerHTML = '<i class="bi bi-check-circle-fill"></i> Added!';
            this.classList.add('btn-success');
            this.classList.remove('btn-dark', 'btn-warning');
            const self = this;
            setTimeout(function () {
                self.innerHTML = original;
                self.classList.remove('btn-success');
                self.classList.add('btn-dark');
            }, 2000);
        });
    });

    // Product image gallery (detail page)
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    thumbnails.forEach(function (thumb) {
        thumb.addEventListener('click', function () {
            const mainImg = document.querySelector('#main-product-image');
            if (mainImg) {
                mainImg.src = this.getAttribute('data-full');
            }
            thumbnails.forEach(t => t.classList.remove('border-warning', 'border-3'));
            this.classList.add('border-warning', 'border-3');
        });
    });

    // Quantity increment/decrement
    document.querySelectorAll('.qty-increment').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const input = this.closest('.qty-control').querySelector('input[type=number]');
            const max = parseInt(input.getAttribute('max') || 99);
            if (parseInt(input.value) < max) {
                input.value = parseInt(input.value) + 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    document.querySelectorAll('.qty-decrement').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const input = this.closest('.qty-control').querySelector('input[type=number]');
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    // Confirm delete dialogs
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            const msg = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });

    // Preview uploaded image before submit
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

});

// Toast notification helper
function showToast(message, type = 'success') {
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-bg-${type} border-0 position-fixed bottom-0 end-0 m-3`;
    toastEl.setAttribute('role', 'alert');
    toastEl.style.zIndex = 9999;
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body fw-semibold">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>`;
    document.body.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}
