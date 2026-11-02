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

  var desk = $('#heroDesk');
  if (desk) {
    var stage = $('.vdks', desk), cfapp = $('.cfapp', desk), cur = $('#hCur'), tray = $('#hTrayIco'), win = $('.hwin', desk), tmenu = $('.htray', desk), hisl = $('.hisl', desk), editor = $('.ed2', desk);
    var steps = $$('#dsteps li'), replay = $('#dreplay'), hstack = $('.isl-stack', desk);
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var token = 0, manual = false, started = false, STOP = {};
    var TODAY = new Date().getDay();
    function pos(el, fx, fy) {
      var d = stage.getBoundingClientRect(), r = el.getBoundingClientRect();
      var k = d.width / stage.offsetWidth || 1; return [(r.left - d.left + r.width * (fx == null ? .5 : fx)) / k, (r.top - d.top + r.height * (fy == null ? .5 : fy)) / k];
    }
    function wait(ms) { var t = token; return sleep(ms).then(function () { if (t !== token) throw STOP; }); }
    function move(el, fx, fy) { var p = pos(el, fx, fy); cur.style.transform = 'translate(' + p[0] + 'px,' + p[1] + 'px)'; return wait(900); }
    function click() { cur.classList.remove('click'); void cur.offsetWidth; cur.classList.add('click'); return wait(350); }
    function setStep(i) { steps.forEach(function (s, k) { s.classList.toggle('on', k === i); s.classList.toggle('done', k < i); }); }
    function setState(s) {
      tmenu.style.opacity = s === 1 ? 1 : 0; tmenu.style.pointerEvents = s === 1 ? 'auto' : 'none';
      var showWin = s === 2 || s === 4;
      win.style.opacity = showWin ? 1 : 0; win.style.transform = showWin ? 'none' : 'translateY(10px) scale(.98)'; win.style.pointerEvents = showWin ? 'auto' : 'none';
      hisl.style.opacity = s === 3 || s === 4 ? 1 : 0;
      if (cfapp) { cfapp.classList.toggle('on', showWin); cfapp.classList.toggle('run', !showWin); }
      if (hstack._c) { if (s === 3 || s === 4) hstack._c.start(); else hstack._c.stop(); }
    }
    [win, tmenu, hisl].forEach(function (e) { e.style.transition = 'opacity .45s,transform .45s'; });
    function qs(sel) { return $(sel, editor); }
    async function loop() {
      var t = token;
      try {
        cur.style.transform = 'translate(' + (stage.offsetWidth * .55) + 'px,' + (stage.offsetHeight * .5) + 'px)';
        cur.classList.add('on');
        for (;;) {
          if (editor.__reset) editor.__reset();
          setState(0); setStep(-1); await wait(900);
          setStep(0); await move(tray, .5, .5); await click(); setState(1); await wait(700);
          var mi = $('.mi[data-k="edit"]', tmenu);
          setStep(1); await move(mi, .3, .5); mi.classList.add('mon'); await click(); setState(2); mi.classList.remove('mon'); await wait(1000);
          setStep(2);
          var nb = qs('.nb[data-new="' + TODAY + '"]'); await move(nb, .5, .5); await click(); nb.click(); await wait(800);
          var ok = qs('[data-pok]'); await move(ok, .5, .5); await click(); ok.click(); await wait(700);
          var c0 = qs('td.c[data-d="' + TODAY + '"][data-r="0"]'); await move(c0, .5, .5); await click(); c0.click(); await wait(300);
          var names = ['语文', '数学', '英语', '物理', '化学'];
          for (var i = 0; i < names.length; i++) {
            var chip = qs('[data-sub="' + names[i] + '"]'); await move(chip, .5, .5); await click(); chip.click(); await wait(180);
          }
          await wait(900);
          setState(3); setStep(3); cur.classList.remove('on'); await wait(18000);
          cur.classList.add('on');
        }
      } catch (e) { if (e !== STOP) throw e; }
    }
    function takeOver() {
      if (manual) return; manual = true; token++; cur.classList.remove('on'); setState(4); setStep(-1);
      if (replay) replay.hidden = false;
    }
    function restart() {
      manual = false; token++; if (replay) replay.hidden = true; if (editor.__reset) editor.__reset(); loop();
    }
    desk.addEventListener('pointerdown', function (e) {
      if (!started) return;
      if (!manual) { takeOver(); return; }
      if (e.target.closest('#hTrayIco')) { var open = tmenu.style.opacity === '1'; tmenu.style.opacity = open ? 0 : 1; tmenu.style.pointerEvents = open ? 'none' : 'auto'; return; }
      var m = e.target.closest('.htray .mi');
      if (m) { tmenu.style.opacity = 0; tmenu.style.pointerEvents = 'none'; if (m.dataset.k === 'edit') setState(4); }
    });
    if (replay) replay.addEventListener('click', restart);
    if (!reduce) inView(desk, function () { started = true; loop(); }, 0.3); else { started = true; manual = true; setState(4); }
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

  var rels = null, chan = 'stable';
  function fmt(n) { return n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.round(n / 1024) + ' KB'; }
  function pick() { if (!rels) return null; for (var i = 0; i < rels.length; i++) { var r = rels[i]; if (!r.draft && (chan === 'pre' ? r.prerelease : !r.prerelease)) return r; } return null; }
  function fillRel() {
    var r = pick(), box = $('#assets'), dl = $('[data-dl]');
    $$('[data-badge]').forEach(function (e) { e.hidden = chan !== 'pre'; });
    var tip = $('#chanTip'); if (tip) tip.textContent = chan === 'pre' ? '最新预览版' : '最新稳定版';
    if (!r) {
      $$('[data-ver]').forEach(function (e) { e.textContent = chan === 'pre' ? '暂无预览版' : '—'; });
      $$('[data-date]').forEach(function (e) { e.textContent = '—'; });
      if (box) box.innerHTML = '<div class="none">' + (chan === 'pre' ? '目前没有发布预览版，请先使用稳定版。' : '暂无可下载的版本。') + '</div>';
      if (dl) dl.classList.add('dis'); return;
    }
    if (dl) { dl.classList.remove('dis'); }
    $$('[data-ver]').forEach(function (e) { e.textContent = r.tag_name; });
    $$('[data-date]').forEach(function (e) { e.textContent = (r.published_at || '').slice(0, 10); });
    $$('[data-releaselink]').forEach(function (e) { e.href = r.html_url; });
    if (dl) { var big = (r.assets || []).slice().sort(function (a, b) { return /installer/i.test(b.name) - /installer/i.test(a.name); })[0]; dl.href = big ? big.browser_download_url : r.html_url; }
    if (box) {
      var KIND = [
        [/installer/i, '安装程序', '按向导安装，自带运行时，适合大多数用户。', 0, 'M12 3v10m0 0l-4-4m4 4l4-4M5 17v2a2 2 0 002 2h10a2 2 0 002-2v-2'],
        [/selfcontained/i, '免安装 · 自带运行时', '解压即用，无需另装运行时，体积较大。', 1, 'M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z'],
        [/full/i, '免安装 · 依赖运行时', '解压即用，需本机已有对应的 .NET 桌面运行时，体积较小。', 2, 'M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z']
      ];
      function kind(n) { for (var i = 0; i < KIND.length; i++) if (KIND[i][0].test(n)) return KIND[i]; return [0, '其他文件', '', 3, 'M7 3h7l4 4v14H7zM14 3v4h4']; }
      var as = (r.assets || []).slice().sort(function (a, b) { return kind(a.name)[3] - kind(b.name)[3]; });
      box.innerHTML = as.length ? as.map(function (a, i) {
        var k = kind(a.name);
        return '<a class="ac' + (k[3] === 0 ? ' rec' : '') + '" href="' + a.browser_download_url + '" rel="noopener"><span class="ai"><svg viewBox="0 0 24 24"><path d="' + k[4] + '"/></svg></span><span class="at"><b>' + k[1] + (k[3] === 0 ? '<u>推荐</u>' : '') + '</b>' + (k[2] ? '<span>' + k[2] + '</span>' : '') + '<code>' + a.name + '</code></span><span class="am"><em>' + fmt(a.size) + '</em><i class="dlb"><svg viewBox="0 0 24 24"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 20h14"/></svg></i></span></a>';
      }).join('') : '<div class="none">该版本暂无文件，请前往 GitHub 查看。</div>';
    }
  }
  $$('[data-chan]').forEach(function (b) { b.addEventListener('click', function () {
    chan = b.dataset.chan; $$('[data-chan]').forEach(function (x) { x.classList.toggle('on', x === b); }); fillRel(); }); });
  if (window.fetch && ($('[data-ver]') || $('#assets'))) {
    var cache = null; try { cache = JSON.parse(localStorage.getItem('cf_rels') || 'null'); } catch (e) { }
    if (cache && Date.now() - cache.t < 36e5) { rels = cache.r; fillRel(); }
    else fetch('https://api.github.com/repos/' + REPO + '/releases?per_page=20').then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .then(function (r) { rels = r; fillRel(); try { localStorage.setItem('cf_rels', JSON.stringify({ t: Date.now(), r: r })); } catch (e) { } })
      .catch(function () {
        $$('[data-ver]').forEach(function (e) { e.textContent = '见 GitHub'; });
        var box = $('#assets'); if (box) box.innerHTML = '<div class="none">暂时无法读取版本信息，请前往 <a href="https://github.com/' + REPO + '/releases" rel="noopener">GitHub Releases</a> 下载。</div>';
      });
  }

  var tb = $('#theme');
  if (tb) tb.addEventListener('click', function () {
    var cur = document.documentElement.dataset.theme;
    if (!cur) cur = (window.matchMedia && matchMedia('(prefers-color-scheme: light)').matches) ? 'light' : 'dark';
    var nx = cur === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = nx;
    try { localStorage.setItem('cf_theme', nx); } catch (e) { }
  });

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
