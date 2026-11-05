(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var hasIO = 'IntersectionObserver' in window;

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    var d = new Date(), t = pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
    $$('[data-now="time"]').forEach(function (e) { e.textContent = t; });
    var y = d.getFullYear(), ny = new Date(y + 1, 0, 1), today = new Date(y, d.getMonth(), d.getDate());
    var days = Math.round((ny - today) / 864e5);
    $$('[data-cd]').forEach(function (e) { e.textContent = '元旦 ' + days + ' 天'; });
  }
  tick(); setInterval(tick, 1000);

  function place(vd) {
    var k = +vd.dataset.k || 1, st = vd.firstElementChild, sr = st.getBoundingClientRect(), rows = [];
    $$('.n4-anno', vd).forEach(function (a) {
      var t = $(a.dataset.t, vd); if (!t) return;
      var r = t.getBoundingClientRect(), x = (r.left + r.width / 2 - sr.left) / k, y = (r.bottom - sr.top) / k;
      var row = 0, w = a.firstElementChild.offsetWidth || 80;
      rows.forEach(function (p) { if (Math.abs(p.x - x) < (p.w + w) / 2 + 10 && p.row === row) row++; });
      rows.push({ x: x, w: w, row: row });
      var ln = 18 + row * 40;
      a.style.setProperty('--ln', ln + 'px');
      a.style.left = x + 'px'; a.style.top = (y + ln) + 'px';
    });
  }
  var main = $('.vdk-main');
  if (main) {
    var go = function () { place(main); };
    window.addEventListener('resize', function () { setTimeout(go, 60); });
    window.addEventListener('load', function () { setTimeout(go, 120); });
    setTimeout(go, 200);
  }

  if (hasIO) {
    var sio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); sio.unobserve(e.target); } });
    }, { threshold: 0.45 });
    $$('.n4-stp').forEach(function (a) { sio.observe(a); });

    var pio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('pz', !e.isIntersecting); });
    }, { rootMargin: '120px 0px' });
    $$('.marq,.bigmq,.pmq,.thx-reel').forEach(function (m) { m.classList.add('pz'); pio.observe(m); });

    var dio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var c = e.target._c; if (!c || e.target.dataset.demo === 'hero') return;
        if (e.isIntersecting) { if (e.target._off) { e.target._off = 0; c.start(); } } else if (e.target._started) { e.target._off = 1; c.stop(); }
      });
    }, { threshold: 0.05 });
    $$('.isl-stack[data-demo]').forEach(function (s) { s._started = 1; dio.observe(s); });
  }

  $$('.chips-row').forEach(function (row) {
    var cs = $$('.chip', row); if (cs.length < 2 || !hasIO) return;
    var i = Math.max(0, cs.findIndex(function (c) { return c.classList.contains('on'); })), timer = null;
    function step() { i = (i + 1) % cs.length; cs.forEach(function (c, j) { c.classList.toggle('on', j === i); }); }
    new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { if (!timer) timer = setInterval(step, 2000); } else { clearInterval(timer); timer = null; }
    }, { threshold: 0.4 }).observe(row);
  });
})();
