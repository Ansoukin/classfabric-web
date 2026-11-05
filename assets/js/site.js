(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var REPO = 'Ansoukin/ClassFabric';

  function fitAll() {
    var mobile = window.innerWidth <= 760;
    $$('.fitbox').forEach(function (b) {
      var f = b.firstElementChild; if (!f) return;
      var dw = +(mobile && b.dataset.dwm ? b.dataset.dwm : b.dataset.dw);
      var w = b.clientWidth || b.parentNode.clientWidth;
      if (!w) return;
      var s = w / dw;
      f.style.transform = 'scale(' + s + ')';
      f.style.transformOrigin = '0 0';
      f.style.width = dw + 'px';
      b.style.height = (f.offsetHeight * s) + 'px';
    });
  }
  function fitVd() {
    var mobile = window.innerWidth <= 760;
    $$('[data-vd]').forEach(function (vd) {
      var st = vd.firstElementChild, dw = +(mobile && vd.dataset.mw ? vd.dataset.mw : vd.dataset.w), dh = +(mobile && vd.dataset.mh ? vd.dataset.mh : vd.dataset.h);
      var w = vd.clientWidth; if (!w) return;
      var s = w / dw; vd.classList.toggle('m', mobile);
      st.style.setProperty('--dw', dw); st.style.setProperty('--dh', dh);
      st.style.transform = 'scale(' + s + ')'; vd.style.height = (dh * s) + 'px'; vd.dataset.k = s;
    });
  }
  window.addEventListener('resize', fitVd);
  window.addEventListener('load', fitVd);
  fitVd();
  window.addEventListener('resize', fitAll);
  window.addEventListener('load', fitAll);
  fitAll();

  function inView(el, cb, th) {
    if (!('IntersectionObserver' in window)) { cb(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.disconnect(); cb(); } });
    }, { threshold: th || 0.25 });
    io.observe(el);
  }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  var rv = $$('.rv');
  if ('IntersectionObserver' in window) {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } });
    }, { threshold: 0.08 });
    rv.forEach(function (e) { rio.observe(e); });
  } else rv.forEach(function (e) { e.classList.add('in'); });

  function cycle(stack, getList) {
    var token = 0;
    function show(el) {
      $$('.isl', stack).forEach(function (i) { i.classList.remove('on'); });
      void el.offsetWidth;
      el.classList.add('on');
    }
    async function run() {
      var my = ++token;
      while (my === token) {
        var list = getList();
        for (var i = 0; i < list.length; i++) {
          if (my !== token) return;
          show(list[i]);
          await sleep(+list[i].dataset.ms || 3000);
        }
      }
    }
    return { start: run, stop: function () { token++; } };
  }
  var remC = null, curGroup = 0;
  $$('.isl-stack[data-demo]').forEach(function (st) {
    var all = $$('.isl', st);
    var kind = st.dataset.demo;
    var c = cycle(st, function () {
      return kind === 'rem' ? all.filter(function (i) { return +i.dataset.g === curGroup; }) : all;
    });
    if (kind === 'rem') remC = c;
    inView(st, function () { if (kind === 'hero') return; c.start(); }, 0.3);
    if (kind === 'hero') st._c = c;
  });
  var tabs = $$('#remTabs .sub-i');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) { x.classList.remove('on'); });
      t.classList.add('on'); curGroup = +t.dataset.g;
      if (remC) remC.start();
    });
  });

  $$('.editor, .ed').forEach(function (ed) {
    var ts = $$('[data-tab]', ed), vs = $$('[data-v]', ed);
    ts.forEach(function (t) {
      t.addEventListener('click', function () {
        ts.forEach(function (x) { x.classList.toggle('on', x === t); });
        vs.forEach(function (v) { v.classList.toggle('on', v.dataset.v === t.dataset.tab); });
      });
    });
    var cells = $$('td.c[data-i]', ed), chips = $$('.chips span[data-s]', ed), cur = null;
    cells.forEach(function (c) {
      c.addEventListener('click', function () {
        cells.forEach(function (x) { x.classList.remove('sel'); });
        c.classList.add('sel'); cur = c;
      });
    });
    chips.forEach(function (ch) {
      ch.addEventListener('click', function () {
        chips.forEach(function (x) { x.classList.remove('on'); });
        ch.classList.add('on');
        if (cur) { cur.textContent = ch.dataset.s; cur.dataset.s = ch.dataset.s; }
      });
    });
  });


  var sw = $('#swap');
  if (sw) {
    var mid = $('#swMid'), hint = $('#swHint'), done = $('#swDone'), ok = $('#swOk'), perm = $('#swPerm'), back = $('#swBack'), cancel = $('#swCancel');
    var picks = $$('.pick', sw), first = null, second = null;
    var isl = $('#swIslIn');
    function say(t) { if (isl) { isl.className = 'isl static bar on'; isl.innerHTML = t; } }
    function reset() {
      first = second = null; done.style.display = 'none'; mid.style.display = 'flex';
      picks.forEach(function (p) { p.style.background = ''; });
      hint.textContent = '→ 选择要调换的课程。';
      ok.style.display = perm.style.display = back.style.display = 'none';
      say('课程「换课」演示：选择两节课进行调换');
    }
    picks.forEach(function (p) {
      p.addEventListener('click', function () {
        if (!first) { first = p; p.style.background = 'rgba(98,179,242,.35)'; hint.textContent = '→ 选择要与「' + p.dataset.n + '」交换的课程。'; back.style.display = 'inline-flex'; }
        else if (p !== first && !second) {
          second = p; p.style.background = 'rgba(98,179,242,.35)';
          hint.textContent = '→ 确认换课：' + first.dataset.n + ' ⇄ ' + p.dataset.n;
          ok.style.display = 'inline-flex'; perm.style.display = 'inline-flex';
        }
      });
    });
    ok.addEventListener('click', function () {
      mid.style.display = 'none'; done.style.display = 'flex';
      done.lastChild.nodeType === 3 && (done.lastChild.textContent = '已交换：' + first.dataset.n + ' 与 ' + second.dataset.n + ' 的位置对调');
      ok.style.display = perm.style.display = 'none';
      say('已换课：' + first.dataset.n + ' ⇄ ' + second.dataset.n);
    });
    back.addEventListener('click', reset); cancel.addEventListener('click', reset);
    reset();
  }

  var b40 = $('#bar40 i');
  if (b40) inView(b40, function () { b40.style.width = '40%'; });
  var mig = $('#mig');
  if (mig) inView(mig, function () { $$('div', mig).forEach(function (d, i) { setTimeout(function () { d.classList.add('ok'); }, 300 + i * 350); }); });

  var nav = $('#nav');
  function sc() { nav && nav.classList.toggle('solid', window.scrollY > 20); }
  window.addEventListener('scroll', sc, { passive: true }); sc();
  var menu = $('#menu'), links = $('#links');
  if (menu) menu.addEventListener('click', function () {
    var o = links.classList.toggle('open'); menu.setAttribute('aria-expanded', o);
  });

  var tb = $('#theme');
  if (tb) tb.addEventListener('click', function () {
    var cur = document.documentElement.dataset.theme;
    if (!cur) cur = (window.matchMedia && matchMedia('(prefers-color-scheme: light)').matches) ? 'light' : 'dark';
    var nx = cur === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = nx;
    try { localStorage.setItem('cf_theme', nx); } catch (e) { }
  });

  var toc = $$('.toc a');
  var secs = $$('.prose section[id]');
  if (toc.length && secs.length) {
    var tk = false;
    var upd = function () {
      tk = false;
      var cur = '', y = window.innerHeight * 0.3;
      secs.forEach(function (s) { if (s.getBoundingClientRect().top <= y) cur = s.id; });
      toc.forEach(function (a) { a.classList.toggle('on', cur !== '' && a.getAttribute('href') === '#' + cur); });
    };
    window.addEventListener('scroll', function () { if (!tk) { tk = true; requestAnimationFrame(upd); } }, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  }
})();

(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var v = $('#vid video');
  if (v && 'IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          if (!v.src) { v.src = v.dataset.src; v.addEventListener('error', function () { var f = $('#vid'); if (f) f.style.display = 'none'; }); }
          var pr = v.play(); if (pr && pr.catch) pr.catch(function () { });
        } else if (v.src) v.pause();
      });
    }, { threshold: 0.35 });
    vio.observe(v);
  }
  var gtabs = $$('[data-gt]'), gcap = $('#gcap'), gal = $('[data-gallery]');
  var GCAP = { tl: '以时间轴的方式直接拖动调整每一节课的时间。', sj: '自定义科目的名称、图标与主题色。', grid: '按周查看并填写课表，科目一键点选。', sw: '周视图与日历视图，可预定临时启用的课表。' };
  gtabs.forEach(function (b) {
    b.addEventListener('click', function () {
      gtabs.forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-selected', x === b); });
      var tab = gal && gal.querySelector('.e2tabs > span[data-v="' + b.dataset.gt + '"]'); if (tab) tab.click();
      if (gcap) gcap.textContent = GCAP[b.dataset.gt];
    });
  });
  if (gal) {
    var first = gal.querySelector('.e2tabs > span[data-v="tl"]');
    if (first) window.addEventListener('load', function () { first.click(); });
    $$('.e2tabs > span', gal).forEach(function (sp) {
      sp.addEventListener('click', function () { gtabs.forEach(function (x) { x.classList.toggle('on', x.dataset.gt === sp.dataset.v); }); if (gcap) gcap.textContent = GCAP[sp.dataset.v] || ''; });
    });
  }
  $$('[data-vtray]').forEach(function (vd) {
    var menu = $('[data-vmenu]', vd), win = $('[data-vwin]', vd), ico = $('.ctray', vd);
    if (!menu || !win || !ico) return;
    function showMenu(on) { menu.classList.toggle('open', on); }
    function showWin(on) { win.classList.toggle('shut', !on); }
    ico.addEventListener('click', function (e) { e.stopPropagation(); showMenu(!menu.classList.contains('open')); });
    menu.addEventListener('click', function (e) { var mi = e.target.closest('.mi'); if (!mi) return; showMenu(false); if (/换课/.test(mi.textContent)) showWin(true); });
    vd.addEventListener('click', function (e) { if (!e.target.closest('.vtray-menu') && !e.target.closest('.ctray')) showMenu(false); });
    win.addEventListener('swclose', function () { showWin(false); });
    win.addEventListener('click', function (e) { if (e.target.closest('.wt .ctl i:last-child')) showWin(false); });
  });
})();

(function () {
  var mt = document.getElementById('mtxt');
  if (mt) {
    var ws = Array.prototype.slice.call(mt.querySelectorAll('.mw'));
    var hlFrom = ws.length - 15;
    ws.forEach(function (w, i) { if (i >= hlFrom) w.classList.add('mhl'); });
    var tick = function () {
      var r = mt.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh * 0.82 - r.top) / (r.height + vh * 0.35)));
      var n = Math.round(p * ws.length * 1.08);
      ws.forEach(function (w, i) { w.classList.toggle('on', i < n); });
    };
    window.addEventListener('scroll', tick, { passive: true }); window.addEventListener('resize', tick); tick();
  }
  if (window.matchMedia && window.matchMedia('(hover:hover)').matches) {
    document.addEventListener('pointermove', function (e) {
      var t = e.target.closest && e.target.closest('.cd,.sub-i,.themes3 figure,.pc'); if (!t) return;
      var r = t.getBoundingClientRect(); t.style.setProperty('--mx', (e.clientX - r.left) + 'px'); t.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });
    Array.prototype.forEach.call(document.querySelectorAll('.themes3 figure'), function (f) {
      f.addEventListener('pointermove', function (e) { var r = f.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        f.style.transform = 'perspective(800px) rotateY(' + (x * 8) + 'deg) rotateX(' + (-y * 8) + 'deg) translateY(-6px)'; });
      f.addEventListener('pointerleave', function () { f.style.transform = ''; });
    });
  }
})();

(function () {
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function p2(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    var d = new Date(), wd = '日一二三四五六'.charAt(d.getDay());
    var t = '周' + wd + ' ' + p2(d.getMonth() + 1) + '/' + p2(d.getDate());
    $$('.idt').forEach(function (e) { e.textContent = t; });
    $$('[data-clock]').forEach(function (e) { e.innerHTML = p2(d.getHours()) + ':' + p2(d.getMinutes()) + '<br>' + d.getFullYear() + '/' + (d.getMonth() + 1) + '/' + d.getDate(); });
    $$('[data-wd]').forEach(function (e) { e.textContent = '周' + wd; });
  }
  tick(); setInterval(tick, 20000);
})();

(function () {
  Array.prototype.forEach.call(document.querySelectorAll('.pc img, .pva img'), function (img) {
    function fallback() {
      if (!img.parentNode) return;
      var s = document.createElement('span'); s.className = 'av'; var host = img.closest('.pvh, .pc') || img.parentNode, nb = host.querySelector('b'); s.textContent = nb ? nb.textContent.charAt(0) : '?';
      img.replaceWith(s);
    }
    img.addEventListener('error', fallback);
    if (img.complete && img.naturalWidth === 0) fallback();
  });
})();

(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  var linearOk = window.CSS && CSS.supports && CSS.supports('animation-timing-function', 'linear(0, 1)');
  function springCurve(zeta, w) {
    var wd = w * Math.sqrt(1 - zeta * zeta), pts = [], n = 40, T = 1.1;
    for (var i = 0; i <= n; i++) {
      var tt = i / n * T, v = 1 - Math.exp(-zeta * w * tt) * (Math.cos(wd * tt) + zeta * w / wd * Math.sin(wd * tt));
      pts.push(v.toFixed(4));
    }
    pts[n] = '1';
    return 'linear(' + pts.join(',') + ')';
  }
  var OPEN = linearOk ? springCurve(0.46, 13) : 'cubic-bezier(.34,1.56,.64,1)';
  var CLOSE = 'cubic-bezier(.3,.9,.3,1)';
  Array.prototype.forEach.call(document.querySelectorAll('[data-acc]'), function (acc) {
    var items = Array.prototype.slice.call(acc.querySelectorAll('.acc-i')), lock = 0;
    function panel(it) { return it.querySelector('.acc-p'); }
    function set(it, open, animate) {
      if (it.classList.contains('open') === open && !animate) return;
      var p = panel(it), from = p.getBoundingClientRect().height;
      it.classList.toggle('open', open);
      it.querySelector('button').setAttribute('aria-expanded', open);
      p.style.height = open ? 'auto' : '0px';
      var to = open ? p.scrollHeight : 0;
      if (reduce || !p.animate) return;
      if (p._a) p._a.cancel();
      p.style.height = to + 'px';
      p._a = p.animate([{ height: from + 'px' }, { height: to + 'px' }], { duration: open ? 900 : 320, easing: open ? OPEN : CLOSE });
      p._a.onfinish = function () { p.style.height = open ? 'auto' : '0px'; p._a = null; };
      var inner = p.firstElementChild;
      if (inner && inner.animate) inner.animate(open ? [{ opacity: 0, transform: 'translateY(-6px)' }, { opacity: 1, transform: 'none' }] : [{ opacity: 1 }, { opacity: 0 }], { duration: open ? 420 : 160, easing: 'ease-out', fill: 'backwards' });
    }
    function openOnly(it) { items.forEach(function (x) { if (x !== it) set(x, false); }); set(it, true); lock = performance.now() + 380; }
    items.forEach(function (it) {
      var btn = it.querySelector('button');
      btn.addEventListener('click', function () {
        if (it.classList.contains('open')) { set(it, false); lock = performance.now() + 380; } else openOnly(it);
      });
      if (canHover) it.addEventListener('pointermove', function () {
        if (!it.classList.contains('open') && performance.now() > lock) openOnly(it);
      });
    });
    items[0].classList.add('open'); items[0].querySelector('button').setAttribute('aria-expanded', true); panel(items[0]).style.height = 'auto';
  });
})();
