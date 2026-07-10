/**
 * Tool page — calculator and AI form handler
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var form = document.getElementById('toolForm');
        if (!form) return;

        var slug = form.dataset.slug;
        var toolType = form.dataset.type;
        var resultBox = document.getElementById('toolResult');
        var resultContent = document.getElementById('toolResultContent');
        var loading = document.getElementById('toolLoading');
        var loadingText = document.getElementById('toolLoadingText');
        var submitBtn = document.getElementById('toolSubmitBtn');
        var postCta = document.getElementById('toolPostCta');
        var usageBadge = document.getElementById('usageBadge');

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            if (submitBtn.disabled) return;

            var data = {};
            form.querySelectorAll('input, select, textarea').forEach(function (el) {
                if (el.name) data[el.name] = el.value;
            });

            submitBtn.disabled = true;
            loading.classList.remove('d-none');
            loadingText.textContent = toolType === 'ai' ? 'Generating...' : 'Calculating...';
            resultBox.classList.add('d-none');

            fetch('/api/tools/' + slug + '/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(function (res) { return res.json().then(function (j) { return { ok: res.ok, json: j }; }); })
            .then(function (r) {
                loading.classList.add('d-none');
                submitBtn.disabled = false;
                var json = r.json;
                if (!json.success) {
                    showError(json.error || 'An error occurred. Please try again.');
                    if (json.limit_reached && postCta) postCta.classList.remove('d-none');
                    return;
                }
                showResult(json.result, toolType);
                if (toolType === 'ai') {
                    if (postCta) postCta.classList.remove('d-none');
                    if (json.usage && usageBadge) updateUsageBadge(json.usage);
                    if (typeof gtag === 'function') gtag('event', 'tool_use', { tool_slug: slug, tool_type: 'ai' });
                } else if (typeof gtag === 'function') {
                    gtag('event', 'tool_use', { tool_slug: slug, tool_type: 'calculator' });
                }
            })
            .catch(function () {
                loading.classList.add('d-none');
                submitBtn.disabled = false;
                showError('Network error. Please check your connection and try again.');
            });
        });

        function updateUsageBadge(usage) {
            var limit = usage.limit > 0 ? usage.limit : '∞';
            usageBadge.innerHTML = 'AI uses today: <strong>' + usage.used + '</strong> / ' + limit;
        }

        function showResult(result, type) {
            resultBox.classList.remove('d-none');
            if (type === 'ai' && result.text) {
                resultContent.innerHTML = '<div class="ai-result-text">' + escapeHtml(result.text).replace(/\n/g, '<br>') + '</div>';
            } else if (result.summary) {
                var html = '<p class="fw-semibold text-primary mb-3">' + escapeHtml(result.summary) + '</p><dl class="row mb-0">';
                Object.keys(result).forEach(function (key) {
                    if (key !== 'summary') {
                        html += '<dt class="col-sm-5 text-secondary">' + formatKey(key) + '</dt>';
                        html += '<dd class="col-sm-7 fw-medium">' + escapeHtml(String(result[key])) + '</dd>';
                    }
                });
                html += '</dl>';
                resultContent.innerHTML = html;
            } else {
                resultContent.innerHTML = '<pre class="mb-0">' + escapeHtml(JSON.stringify(result, null, 2)) + '</pre>';
            }
            resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        function showError(msg) {
            resultBox.classList.remove('d-none');
            resultContent.innerHTML = '<div class="alert alert-warning mb-0">' + escapeHtml(msg) + '</div>';
        }

        var copyBtn = document.getElementById('copyResultBtn');
        if (copyBtn) {
            copyBtn.addEventListener('click', function () {
                navigator.clipboard.writeText(resultContent.innerText).then(function () {
                    copyBtn.textContent = 'Copied!';
                    setTimeout(function () { copyBtn.textContent = 'Copy'; }, 2000);
                });
            });
        }

        var clearBtn = document.getElementById('clearResultBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', function () {
                resultBox.classList.add('d-none');
                form.reset();
            });
        }

        function escapeHtml(str) {
            return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
        }

        function formatKey(key) {
            return key.replace(/_/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
        }
    });
})();
