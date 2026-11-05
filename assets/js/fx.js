(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hover = window.matchMedia && matchMedia('(hover: hover)').matches;

  var bar = document.createElement('div'); bar.id = 'topbar'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
  function run() { bar.className = 'run'; }
  function done() { bar.className = 'done'; setTimeout(function () { bar.className = ''; }, 800); }
  if (document.readyState === 'complete') done(); else { run(); window.addEventListener('load', done); }
  window.addEventListener('pageshow', function (e) { if (e.persisted) done(); });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button || a.target || a.hasAttribute('download')) return;
    var u; try { u = new URL(a.href, location.href); } catch (x) { return; }
    if (u.origin === location.origin && u.pathname !== location.pathname) run();
  });

  var root = document.documentElement, tick = false;
  function onScroll() {
    var h = root.scrollHeight - innerHeight, y = window.pageYOffset;
    root.style.setProperty('--sp', (h > 0 ? Math.min(1, y / h) : 0).toFixed(4));
    tick = false;
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  var SEL = '.axc,.fcard,.cd,.sub-i,.stp4 li,.fit2>div,.thx-t,.tu,.ac,.infob,.hist li a,.acc-i,.pc,.repo';
  if (hover && !reduce) {
    document.addEventListener('pointermove', function (e) {
      var t = e.target.closest && e.target.closest(SEL); if (!t) return;
      if (!t.__rfx) { var f = document.createElement('span'); f.className = 'rfx'; f.setAttribute('aria-hidden', 'true'); t.appendChild(f); t.classList.add('rvl'); t.__rfx = f; }
      var r = t.getBoundingClientRect();
      t.style.setProperty('--mx', (e.clientX - r.left) + 'px'); t.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });
  }

  $$('img.sk-i').forEach(function (img) {
    var host = img.parentElement;
    function ok() { img.classList.add('ok'); if (host) host.classList.add('ok'); }
    if (img.complete && img.naturalWidth) ok(); else { img.addEventListener('load', ok); img.addEventListener('error', ok); }
  });

  var th = $('#theme');
  if (th) th.addEventListener('click', function () { root.classList.add('tt'); setTimeout(function () { root.classList.remove('tt'); }, 520); });
})();
