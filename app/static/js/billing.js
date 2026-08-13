/** Stripe checkout from Pricing page — V1.1 */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.checkout-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const planId = btn.dataset.plan;
      if (!planId) return;
      btn.disabled = true;
      const label = btn.textContent;
      btn.textContent = 'Redirecting…';
      try {
        const res = await fetch('/api/billing/checkout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ plan_id: planId }),
        });
        const data = await res.json();
        if (res.ok && data.redirect_url) {
          window.location.href = data.redirect_url;
          return;
        }
        if (res.status === 401) {
          window.location.href = '/login?next=/pricing';
          return;
        }
        alert(data.detail || 'Checkout failed. Please sign in or try again.');
      } catch (e) {
        alert('Network error. Please try again.');
      }
      btn.disabled = false;
      btn.textContent = label;
    });
  });
});
