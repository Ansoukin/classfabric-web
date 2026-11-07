(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var hasIO = 'IntersectionObserver' in window;
  var DAYS = '日一二三四五六';

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function daysToNY() {
    var d = new Date(), y = d.getFullYear();
    return Math.round((new Date(y + 1, 0, 1) - new Date(y, d.getMonth(), d.getDate())) / 864e5);
  }
  function tick() {
    var d = new Date(), t = pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
    $$('[data-now="time"]').forEach(function (e) { e.textContent = t; });
    var n = daysToNY();
    $$('[data-cd]').forEach(function (e) { e.textContent = '元旦 ' + n + ' 天'; });
  }
  tick(); setInterval(tick, 1000);

  var TICK = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--tick')) || 2) * 1000;
  var cd2 = $$('[data-cd2]');
  cd2.forEach(function (e) { e._n0 = +e.dataset.cd2; e._n = e._n0; });
  if (cd2.length) setInterval(function () {
    if (document.hidden) return;
    cd2.forEach(function (e) {
      e._n = e._n <= 1 ? e._n0 : e._n - 1;
      e.textContent = e.dataset.fmt ? e.dataset.fmt.replace('{n}', e._n) : e._n;
    });
  }, TICK);

  function place(vd) {
    var k = +vd.dataset.k || 1, st = vd.firstElementChild, sr = st.getBoundingClientRect(), rows = [];
    $$('.n5-anno', vd).forEach(function (a) {
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

  var stage = $('.n5-stage');
  if (stage && hasIO) {
    var chs = $$('.n5-ch', stage), cur = 0;
    var setActive = function (i) {
      if (i === cur) return;
      cur = i;
      chs.forEach(function (c, k) { c.classList.toggle('on', k === i); c.classList.toggle('past', k < i); });
      if (i === 0 && main) setTimeout(function () { place(main); }, 760);
    };
    var sio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) setActive(+e.target.closest('.n5-ch').dataset.i); });
    }, { rootMargin: '-42% 0px -42% 0px' });
    $$('.n5-tx', stage).forEach(function (t) { sio.observe(t); });
  }

  if (hasIO) {
    var pio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('pz', !e.isIntersecting); });
    }, { rootMargin: '120px 0px' });
    $$('.n5-lane,.bigmq').forEach(function (m) { m.classList.add('pz'); pio.observe(m); });

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
      if (es[0].isIntersecting) { if (!timer) timer = setInterval(step, 2400); } else { clearInterval(timer); timer = null; }
    }, { threshold: 0.4 }).observe(row);
  });

  var ln = $('#lnav');
  if (ln && hasIO) {
    var links = $$('.ls a', ln), map = {};
    links.forEach(function (a) { var t = $(a.getAttribute('href')); if (t) map[t.id] = a; });
    var vis = {};
    var nio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { vis[e.target.id] = e.isIntersecting; });
      var c = null;
      Object.keys(map).forEach(function (id) { if (vis[id]) c = id; });
      links.forEach(function (a) { a.classList.toggle('on', c && map[c] === a); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { nio.observe(document.getElementById(id)); });
  }

  $$('[data-sw]').forEach(function (sw) {
    var tabs = $$('.n4-swt', sw), ps = $$('.n4-swp', sw), cur = 0;
    function go(i) {
      cur = i;
      tabs.forEach(function (t, k) { t.classList.toggle('on', k === i); t.setAttribute('aria-selected', k === i); });
      ps.forEach(function (p, k) { p.classList.toggle('on', k === i); });
    }
    tabs.forEach(function (t, i) { t.addEventListener('click', function () { if (i === cur) { t.classList.remove('on'); void t.offsetWidth; t.classList.add('on'); } else go(i); }); });
    sw.addEventListener('animationend', function (e) { if (e.animationName === 'n4fill') go((cur + 1) % tabs.length); });
    sw.classList.add('pz');
    if (hasIO) new IntersectionObserver(function (es) { sw.classList.toggle('pz', !es[0].isIntersecting); }, { threshold: 0.35 }).observe(sw);
    else sw.classList.remove('pz');
  });

  $$('.n5-ths').forEach(function (box) {
    var bs = $$('.n5-th', box);
    bs.forEach(function (b) {
      b.addEventListener('click', function () {
        bs.forEach(function (x) {
          var on = x === b;
          x.classList.toggle('on', on); x.setAttribute('aria-pressed', on);
          var t = $('.tg', x); if (t) t.classList.toggle('on', on);
        });
      });
    });
  });

  var FF = { sans: 'inherit', serif: '"Songti SC","Noto Serif CJK SC","Source Han Serif SC",serif', mono: 'ui-monospace,"Cascadia Code",Consolas,monospace' };
  $$('.n5-tune').forEach(function (t) {
    var isl = $('.n5-tisl', t);
    $$('.n5-rg', t).forEach(function (r) {
      var ap = function () {
        var v = +r.value, k = r.dataset.k;
        r.style.setProperty('--v', ((v - r.min) / (r.max - r.min) * 100) + '%');
        isl.style.setProperty(k === 's' ? '--k' : k === 'o' ? '--op' : '--rd', v / 100);
      };
      r.addEventListener('input', ap); ap();
    });
    var fb = $$('[data-ff]', t);
    fb.forEach(function (b) {
      b.addEventListener('click', function () {
        fb.forEach(function (x) { x.classList.toggle('on', x === b); });
        isl.style.setProperty('--ff', FF[b.dataset.ff]);
      });
    });
  });

  function fill(inner, c, tpl) {
    var sig = [c.t, c.text, (c.kids || []).map(function (k) { return k.t + k.text; }).join()].join('|');
    if (inner._sig === sig) return;
    inner._sig = sig;
    var t = c.t, el;
    inner.innerHTML = '';
    var span = function (cls, txt) { var s = document.createElement('span'); s.className = cls; if (txt != null) s.textContent = txt; return s; };
    if (t === '文本') inner.appendChild(span('wt', c.text || '你好，我是文本'));
    else if (t === '分割线') inner.appendChild(span('sep'));
    else if (t === '日期') { var d = new Date(); inner.appendChild(span('wt', '周' + DAYS[d.getDay()] + ' ' + pad(d.getMonth() + 1) + '/' + pad(d.getDate()))); }
    else if (t === '时钟') { el = span('wt'); el.setAttribute('data-now', 'time'); inner.appendChild(el); tick(); }
    else if (t === '倒计时') { el = span('wt'); el.innerHTML = '距离 <b></b> 还有 <b></b> 天'; var bs = el.querySelectorAll('b'); bs[0].textContent = c.text || '元旦'; bs[1].textContent = daysToNY(); inner.appendChild(el); }
    else if (tpl[t]) inner.appendChild(tpl[t].cloneNode(true));
    else if (c.kids && c.kids.length) c.kids.forEach(function (k) { var s = span('wxk'); s.style.display = 'flex'; fill(s, k, tpl); inner.appendChild(s); });
    else inner.appendChild(span('wt dim', t));
  }

  function sync(isl, rows, tpl) {
    var total = rows.reduce(function (a, r) { return a + r.items.length; }, 0);
    var have = {}, used = {};
    $$('.wxw', isl).forEach(function (w) { have[w.dataset.id] = w; });
    var rowEls = $$('.n5-row', isl);
    while (rowEls.length < rows.length) {
      var d = document.createElement('div'); d.className = 'isl static on n5-row'; isl.appendChild(d); rowEls.push(d);
    }
    rows.forEach(function (row, r) {
      var host = rowEls[r], prev = null;
      host.classList.toggle('empty', !row.items.length);
      row.items.forEach(function (c) {
        var w = have[c.id]; used[c.id] = 1;
        if (!w) {
          w = document.createElement('span'); w.className = 'wxw'; w.dataset.id = c.id;
          w.innerHTML = '<span class="wxi"></span>'; host.appendChild(w);
          (function (w) {
            requestAnimationFrame(function () {
              w.style.maxWidth = w.scrollWidth + 'px'; w.classList.add('in');
              setTimeout(function () { if (w.classList.contains('in')) w.style.maxWidth = 'none'; }, 650);
            });
          })(w);
        }
        fill(w.firstChild, c, tpl);
        var want = prev ? prev.nextSibling : host.firstChild;
        if (w.parentNode !== host || (w !== want && w.previousSibling !== prev)) host.insertBefore(w, want);
        prev = w;
      });
    });
    Object.keys(have).forEach(function (id) {
      if (!used[id]) { var w = have[id]; w.style.maxWidth = w.offsetWidth + 'px'; void w.offsetWidth; w.classList.remove('in'); w.style.maxWidth = '0px'; setTimeout(function () { if (w.parentNode) w.remove(); }, 620); }
    });
    for (var i = rows.length; i < rowEls.length; i++) rowEls[i].remove();
    if (!total) setTimeout(function () { if (!$$('.wxw.in', isl).length) isl.innerHTML = ''; }, 560);
  }

  document.addEventListener('wxdraw', function (e) {
    var host = e.target.closest && e.target.closest('.n5-mix'); if (!host) return;
    var isl = $('[data-wx-island]', host), tpl = {};
    $$('[data-wx-tpl] [data-k]', host).forEach(function (n) { tpl[n.dataset.k] = n; });
    var tp = $('[data-wx-tpl]', host);
    if (tp && tp.content) $$('[data-k]', tp.content).forEach(function (n) { tpl[n.dataset.k] = n; });
    sync(isl, e.detail, tpl);
  });
  $$('.n5-mix .wxpg').forEach(function (pg) { pg.dispatchEvent(new Event('wxreq')); });
})();
