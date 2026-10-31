(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var REPO = 'Ansoukin/ClassFabric';

  /* ---------- fit scaling ---------- */
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
  window.addEventListener('resize', fitAll);
  window.addEventListener('load', fitAll);
  fitAll();

  /* ---------- helpers ---------- */
  function inView(el, cb, th) {
    if (!('IntersectionObserver' in window)) { cb(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.disconnect(); cb(); } });
    }, { threshold: th || 0.25 });
    io.observe(el);
  }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  /* ---------- reveal ---------- */
  var rv = $$('.rv');
  if ('IntersectionObserver' in window) {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } });
    }, { threshold: 0.08 });
    rv.forEach(function (e) { rio.observe(e); });
  } else rv.forEach(function (e) { e.classList.add('in'); });

  /* ---------- island stacks ---------- */
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

  /* ---------- editor tabs / grid ---------- */
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

  /* ---------- automation flyout ---------- */
  var btnAct = $('#btnAct'), flyAct = $('#flyAct');
  if (btnAct && flyAct) btnAct.addEventListener('click', function () { flyAct.classList.toggle('open'); });

  /* ---------- swap dialog ---------- */
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

  /* ---------- hero demo ---------- */
  var desk = $('#heroDesk');
  if (desk) {
    var cur = $('#hCur'), tray = $('#hTrayIco'), win = $('.hwin', desk), tmenu = $('.htray', desk), hisl = $('.hisl', desk);
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    function pos(el, fx, fy) {
      var d = desk.getBoundingClientRect(), r = el.getBoundingClientRect();
      var k = d.width / desk.offsetWidth || 1; return [(r.left - d.left + r.width * (fx == null ? .5 : fx)) / k, (r.top - d.top + r.height * (fy == null ? .5 : fy)) / k];
    }
    function move(el, fx, fy) { var p = pos(el, fx, fy); cur.style.transform = 'translate(' + p[0] + 'px,' + p[1] + 'px)'; return sleep(950); }
    function click() { cur.classList.remove('click'); void cur.offsetWidth; cur.classList.add('click'); return sleep(350); }
    desk.classList.add('stage0');
    var hstack = $('.isl-stack', desk);
    function setState(s) { // 0: nothing, 1: tray menu, 2: window, 3: island
      tmenu.style.opacity = s === 1 ? 1 : 0;
      win.style.opacity = s === 2 ? 1 : (s === 3 ? 0 : 0);
      win.style.transform = s === 2 ? 'none' : 'translateY(10px) scale(.98)';
      hisl.style.opacity = s === 3 ? 1 : 0;
    }
    [win, tmenu, hisl].forEach(function (e) { e.style.transition = 'opacity .45s,transform .45s'; });
    async function loop() {
      cur.style.transform = 'translate(' + (desk.clientWidth * .55) + 'px,' + (desk.clientHeight * .55) + 'px)';
      cur.classList.add('on');
      for (;;) {
        setState(0); if (hstack._c) hstack._c.stop();
        await sleep(800);
        await move(tray, .5, .5); await click();
        setState(1); await sleep(600);
        var mi = $('.mi[data-k="edit"]', tmenu);
        await move(mi, .3, .5); mi.classList.add('hl'); await click();
        setState(2); mi.classList.remove('hl'); await sleep(900);
        var cells = $$('td.c[data-i]', win), chips = $$('.chips span[data-s]', win);
        for (var i = 0; i < Math.min(cells.length, 5); i++) {
          await move(cells[i], .5, .5); await click(); cells[i].click();
          var s = (cells[i].dataset.s || '语数英物化')[0];
          var ch = chips.filter(function (c) { return c.dataset.s === '语数英物化'[i]; })[0] || chips[i];
          if (ch) { await move(ch, .5, .5); await click(); ch.click(); }
        }
        await sleep(700);
        setState(3); if (hstack._c) hstack._c.start();
        await sleep(19000);
      }
    }
    if (!reduce) inView(desk, loop, 0.3); else { setState(3); }
  }

  /* ---------- progress bar ---------- */
  var b40 = $('#bar40 i');
  if (b40) inView(b40, function () { b40.style.width = '40%'; });
  var mig = $('#mig');
  if (mig) inView(mig, function () { $$('div', mig).forEach(function (d, i) { setTimeout(function () { d.classList.add('ok'); }, 300 + i * 350); }); });

  /* ---------- nav ---------- */
  var nav = $('#nav');
  function sc() { nav && nav.classList.toggle('solid', window.scrollY > 20); }
  window.addEventListener('scroll', sc, { passive: true }); sc();
  var menu = $('#menu'), links = $('#links');
  if (menu) menu.addEventListener('click', function () {
    var o = links.classList.toggle('open'); menu.setAttribute('aria-expanded', o);
  });

  /* ---------- release info ---------- */
  var cache = null;
  try { cache = JSON.parse(localStorage.getItem('cf_rel') || 'null'); } catch (e) { }
  function fmt(n) { return n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.round(n / 1024) + ' KB'; }
  function fillRel(r) {
    $$('[data-ver]').forEach(function (e) { e.textContent = r.tag_name; });
    $$('[data-date]').forEach(function (e) { e.textContent = (r.published_at || '').slice(0, 10); });
    $$('[data-releaselink]').forEach(function (e) { e.href = r.html_url; });
    var box = $('#assets');
    if (box) {
      var as = r.assets || [];
      box.innerHTML = as.length ? as.map(function (a) {
        return '<a href="' + a.browser_download_url + '" rel="noopener"><span>' + a.name + '</span><em>' + fmt(a.size) + '</em></a>';
      }).join('') : '<div class="none">该版本暂无文件，请前往 GitHub 查看。</div>';
    }
  }
  if (cache && cache.r && Date.now() - cache.t < 36e5) fillRel(cache.r);
  else if (window.fetch && ($('[data-ver]') || $('#assets'))) {
    fetch('https://api.github.com/repos/' + REPO + '/releases/latest').then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .then(function (r) { fillRel(r); try { localStorage.setItem('cf_rel', JSON.stringify({ t: Date.now(), r: r })); } catch (e) { } })
      .catch(function () {
        $$('[data-ver]').forEach(function (e) { e.textContent = '见 GitHub'; });
        var box = $('#assets'); if (box) box.innerHTML = '<div class="none">暂时无法读取版本信息，请前往 <a href="https://github.com/' + REPO + '/releases" rel="noopener">GitHub Releases</a> 下载。</div>';
      });
  }

  /* ---------- theme ---------- */
  var tb = $('#theme');
  if (tb) tb.addEventListener('click', function () {
    var cur = document.documentElement.dataset.theme;
    if (!cur) cur = (window.matchMedia && matchMedia('(prefers-color-scheme: light)').matches) ? 'light' : 'dark';
    var nx = cur === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = nx;
    try { localStorage.setItem('cf_theme', nx); } catch (e) { }
  });

  /* ---------- toc highlight ---------- */
  var toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    var tio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) toc.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    $$('.prose section[id]').forEach(function (s) { tio.observe(s); });
  }
})();

/* ---------- V11 additions ---------- */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  // desk scale on scroll (Apple-like)
  var desk = $('#heroDesk');
  if (desk && !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var tick = false;
    function upd() {
      tick = false;
      var r = desk.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh - r.top) / (vh * 0.95)));
      desk.style.transform = 'scale(' + (0.9 + 0.1 * p).toFixed(4) + ')';
    }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }
  // video lazy play
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
  // gallery
  var tabs = $$('.gtabs button'), imgs = $$('.gimg'), cap = $('#gcap'), n = 0, timer = null;
  function go(i) {
    n = i;
    tabs.forEach(function (t, k) { t.classList.toggle('on', k === i); t.setAttribute('aria-selected', k === i); });
    imgs.forEach(function (m, k) { m.classList.toggle('on', k === i); });
    if (cap && imgs[i]) cap.textContent = imgs[i].dataset.cap;
  }
  tabs.forEach(function (t, i) { t.addEventListener('click', function () { clearInterval(timer); go(i); }); });
  var gf = $('#gframe');
  if (gf) {
    var lb = document.createElement('div'); lb.className = 'lb'; lb.innerHTML = '<img alt="">'; document.body.appendChild(lb);
    gf.addEventListener('click', function () { lb.firstChild.src = imgs[n].src; lb.classList.add('on'); clearInterval(timer); });
    lb.addEventListener('click', function () { lb.classList.remove('on'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') lb.classList.remove('on'); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting) { o.disconnect(); timer = setInterval(function () { go((n + 1) % imgs.length); }, 5000); } }); }, { threshold: 0.5 }).observe(gf);
    }
  }
})();
