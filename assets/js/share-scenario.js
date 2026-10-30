/**
 * share-scenario.js
 * Enables URL query parameter synchronization and a "Share calculation" button.
 */

function initShareScenario(fields, onPopStateCallback) {
    // 1. Read query params on load and fill inputs
    const params = new URLSearchParams(window.location.search);
    let hasParams = false;

    fields.forEach(f => {
        if (params.has(f.param)) {
            const val = params.get(f.param);
            const el = document.getElementById(f.id);
            if (el) {
                if (el.type === "checkbox") {
                    el.checked = val === "1" || val === "true";
                } else {
                    el.value = val;
                }
                hasParams = true;
            }
        }
    });

    // 2. Handle back/forward navigation
    window.addEventListener("popstate", () => {
        const p = new URLSearchParams(window.location.search);
        fields.forEach(f => {
            if (p.has(f.param)) {
                const el = document.getElementById(f.id);
                if (el) {
                    if (el.type === "checkbox") {
                        el.checked = p.get(f.param) === "1" || p.get(f.param) === "true";
                    } else {
                        el.value = p.get(f.param);
                    }
                }
            }
        });
        if (typeof onPopStateCallback === "function") {
            onPopStateCallback();
        }
    });

    return hasParams;
}

function updateUrlParams(fields) {
    const params = new URLSearchParams();
    fields.forEach(f => {
        const el = document.getElementById(f.id);
        if (el) {
            if (el.type === "checkbox") {
                if (el.checked) params.set(f.param, "1");
            } else if (el.value !== "") {
                params.set(f.param, el.value);
            }
        }
    });
    const newQuery = params.toString() ? "?" + params.toString() : window.location.pathname;
    window.history.replaceState({}, "", newQuery);
}

function shareCurrentCalculation(buttonId, fields) {
    updateUrlParams(fields);
    const url = window.location.href;
    const btn = document.getElementById(buttonId);
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(() => {
            const originalText = btn.textContent;
            btn.textContent = "Link copied! ✓";
            btn.classList.add("is-copied");
            setTimeout(() => {
                btn.textContent = originalText;
                btn.classList.remove("is-copied");
            }, 2500);
        }).catch(() => {
            prompt("Copy this link to share your calculation:", url);
        });
    } else {
        prompt("Copy this link to share your calculation:", url);
    }
}
