/**
 * Email capture forms — lead generation
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.email-capture-form').forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                var wrap = form.closest('.email-capture');
                var msgEl = wrap ? wrap.querySelector('.email-capture-msg') : null;
                var email = form.querySelector('[name="email"]').value.trim();
                var source = wrap ? wrap.dataset.source || 'other' : 'other';
                var btn = form.querySelector('button[type="submit"]');
                if (btn) btn.disabled = true;

                fetch('/api/leads/subscribe', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, source: source })
                })
                .then(function (res) { return res.json(); })
                .then(function (json) {
                    if (btn) btn.disabled = false;
                    if (msgEl) {
                        msgEl.classList.remove('d-none');
                        msgEl.className = 'email-capture-msg small mt-2 ' +
                            (json.success ? 'text-success' : 'text-warning');
                        msgEl.textContent = json.message || json.error || 'Please try again.';
                    }
                    if (json.success) form.reset();
                    if (typeof gtag === 'function') {
                        gtag('event', 'lead_subscribe', { source: source });
                    }
                })
                .catch(function () {
                    if (btn) btn.disabled = false;
                    if (msgEl) {
                        msgEl.classList.remove('d-none');
                        msgEl.className = 'email-capture-msg small mt-2 text-warning';
                        msgEl.textContent = 'Network error. Please try again.';
                    }
                });
            });
        });
    });
})();
