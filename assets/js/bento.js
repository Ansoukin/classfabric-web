(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var hasIO = 'IntersectionObserver' in window;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 对比滑块 */
  $$('.n5-cmp').forEach(function (b) {
    var r = $('input', b), set = function (v) { b.style.setProperty('--p', v + '%'); };
    r.addEventListener('input', function () { set(r.value); });
    if (hasIO) new IntersectionObserver(function (es, io) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var t0 = performance.now();
      (function f(t) { var k = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - k, 3); if (!r._touched) { r.value = 100 - 50 * e; set(r.value); if (k < 1) requestAnimationFrame(f); } })(t0);
    }, { threshold: .6 }).observe(b);
    r.addEventListener('pointerdown', function () { r._touched = 1; });
  });

  /* 修复前 / 修复后：进入视口时自动演示一次，之后由访客自己切换 */
  $$('.n5-fix').forEach(function (c) {
    var tabs = $$('[role=tab]', c), timer = 0, touched = false;
    function set(s) { c.dataset.st = s; tabs.forEach(function (t) { t.setAttribute('aria-selected', t.dataset.s === s ? 'true' : 'false'); }); }
    tabs.forEach(function (t) { t.addEventListener('click', function () { touched = true; clearTimeout(timer); set(t.dataset.s); }); });
    if (hasIO && !reduce) new IntersectionObserver(function (es, io) {
      if (!es[0].isIntersecting) return; io.disconnect();
      set('before'); timer = setTimeout(function () { if (!touched) set('after'); }, 1800);
    }, { threshold: .5 }).observe($('.n5-fxl', c) || c);
  });
})();
