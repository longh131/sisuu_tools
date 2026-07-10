/**
 * Seller Toolkit — global JavaScript
 * Lucide icons loaded on idle to reduce main-thread blocking (Sprint 8)
 */
(function () {
    'use strict';

    var mainScript = document.querySelector('script[data-lucide-src]');
    var lucideSrc = mainScript ? mainScript.getAttribute('data-lucide-src') : '/static/vendor/lucide.min.js';

    function initLucideIcons() {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    function loadLucide() {
        if (document.querySelector('script[data-lucide-loaded]')) {
            initLucideIcons();
            return;
        }
        var script = document.createElement('script');
        script.src = lucideSrc;
        script.defer = true;
        script.setAttribute('data-lucide-loaded', '1');
        script.onload = initLucideIcons;
        document.body.appendChild(script);
    }

    function scheduleLucide() {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(loadLucide, { timeout: 2000 });
        } else {
            setTimeout(loadLucide, 100);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', scheduleLucide);
    } else {
        scheduleLucide();
    }
})();
