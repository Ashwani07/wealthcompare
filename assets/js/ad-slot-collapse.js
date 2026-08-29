/**
 * ad-slot-collapse.js
 *
 * .ad-slot reserves min-height:100px up front so a real, loading ad never
 * causes layout shift (CLS). But before AdSense approval — or on a dev
 * server, or with an ad blocker — nothing ever fills that space, and the
 * reserved box just sits there as a visible dead gap.
 *
 * AdSense sets data-ad-status="filled" or "unfilled" on each <ins> once it
 * finishes processing. This watches for that and collapses the wrapping
 * .ad-slot only when a slot is confirmed unfilled (or never processes at
 * all within FALLBACK_MS — script blocked / no account yet). Once ads are
 * actually approved and serving, this becomes a no-op: filled slots keep
 * their reserved space exactly as before.
 */
(function () {
    var FALLBACK_MS = 4000;

    function collapse(ins) {
        var slot = ins.closest(".ad-slot");
        if (slot) slot.classList.add("ad-slot--empty");
    }

    document.querySelectorAll(".adsbygoogle").forEach(function (ins) {
        var resolved = false;

        var observer = new MutationObserver(function () {
            var status = ins.getAttribute("data-ad-status");
            if (!status) return;
            resolved = true;
            observer.disconnect();
            if (status === "unfilled") collapse(ins);
        });
        observer.observe(ins, { attributes: true, attributeFilter: ["data-ad-status"] });

        setTimeout(function () {
            if (resolved) return;
            observer.disconnect();
            collapse(ins);
        }, FALLBACK_MS);
    });
})();
