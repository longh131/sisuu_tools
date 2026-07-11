/**
 * Google Analytics 4 event tracking
 * Events: page_view (auto), tool_use, lead_subscribe, pricing_click
 */
(function () {
    'use strict';

    function track(eventName, params) {
        if (typeof gtag === 'function') {
            gtag('event', eventName, params || {});
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Pricing CTA clicks
        document.querySelectorAll('[data-cta^="pricing-"]').forEach(function (el) {
            el.addEventListener('click', function () {
                var plan = (el.dataset.cta || '').replace('pricing-', '');
                track('pricing_click', { plan: plan, link_url: el.href || '' });
            });
        });

        // Outbound CTA tracking (optional upgrade links)
        document.querySelectorAll('a[data-track]').forEach(function (el) {
            el.addEventListener('click', function () {
                track(el.dataset.track, { label: el.textContent.trim() });
            });
        });
    });

    window.stTrack = track;
})();
