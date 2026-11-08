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

  /* 修复流程：进入视口时依次点亮 */
  $$('.n5-fix').forEach(function (c) {
    if (!hasIO || reduce) return;
    c.classList.add('arm');
    new IntersectionObserver(function (es, io) {
      if (!es[0].isIntersecting) return; io.disconnect(); c.classList.add('on');
    }, { threshold: .35 }).observe(c);
  });
  /* 打字机：「当 ___」循环改写为各类触发器（取自自动化页的触发器列表）。仅在可见时运行，单个定时器，只改一个文本节点 */
  var TRIG = ['规则集更新时', '收到信号时', '调用 Uri 时', '从托盘菜单运行时', 'cron', '应用启动时', '应用退出时', '上课时', '课间休息时', '放学时', '当前时间状态变化时', '特定时间点前'];
  $$('[data-tw]').forEach(function (el) {
    if (!hasIO || reduce) return;
    var ch = el.closest('.n5-ch'), txt = document.createTextNode(el.textContent), s = txt.nodeValue, i = -1, mode = 'hold', vis = false, timer = 0, rz = 0;
    el.textContent = ''; el.appendChild(txt);
    /* 预留最宽文案的宽度，避免逐字打出时反复换行抖动；窗口尺寸变化后重新测量 */
    function measure() {
      var m = document.createElement('span'), w = 0;
      m.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap';
      el.appendChild(m);
      TRIG.concat([txt.nodeValue]).forEach(function (x) { m.textContent = x; w = Math.max(w, m.offsetWidth); });
      el.removeChild(m); el.style.minWidth = Math.ceil(w + 4) + 'px';
    }
    function step() {
      timer = 0; if (!vis || document.hidden) return;
      if (ch && !ch.classList.contains('on')) { timer = setTimeout(step, 500); return; }
      var d;
      if (mode === 'hold') { mode = 'del'; d = 40; }
      else if (mode === 'del') {
        if (s.length) { s = s.slice(0, -1); d = 34; } else { i = (i + 1) % TRIG.length; mode = 'type'; d = 240; }
      } else {
        var t = TRIG[i];
        if (s.length < t.length) { s = t.slice(0, s.length + 1); d = 78; } else { mode = 'hold'; d = 1700; }
      }
      txt.nodeValue = s; timer = setTimeout(step, d);
    }
    function run(on) { vis = on; el.classList.toggle('tw-on', on); clearTimeout(timer); timer = 0; if (on) { mode = 'hold'; if (i >= 0) { mode = 'type'; } timer = setTimeout(step, 600); } }
    measure();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(measure, 200); });
    document.addEventListener('visibilitychange', function () { if (vis && !document.hidden && !timer) timer = setTimeout(step, 300); });
    new IntersectionObserver(function (es) { run(es[0].isIntersecting); }, { threshold: .2 }).observe(el);
  });
})();
