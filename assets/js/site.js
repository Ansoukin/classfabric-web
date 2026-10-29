/* ClassFabric website — vanilla JS, progressive enhancement only. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var REPO = 'Ansoukin/ClassFabric';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }

  root.classList.add('js');

  /* theme */
  var saved = store('cf-theme');
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);
  var tbtn = $('#theme');
  if (tbtn) tbtn.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') ||
      (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next); store('cf-theme', next);
  });

  /* nav */
  var nav = $('.nav');
  function onScroll() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll(); addEventListener('scroll', onScroll, { passive: true });
  var mb = $('#menu'), links = $('.links');
  if (mb && links) mb.addEventListener('click', function () {
    var o = links.classList.toggle('open'); mb.setAttribute('aria-expanded', o);
  });

  /* reveal on scroll */
  var rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  /* island demo: plays only while on screen */
  $$('.isl-stack[data-demo]').forEach(function (stack) {
    var states = $$('.isl', stack), i = -1, timer = null, running = false;
    function show(n) {
      states.forEach(function (s, k) { s.classList.toggle('on', k === n); });
    }
    function step() {
      i = (i + 1) % states.length; show(i);
      var ms = parseInt(states[i].getAttribute('data-ms'), 10) || 3000;
      timer = setTimeout(step, ms);
    }
    if (reduce || !('IntersectionObserver' in window)) { show(0); return; }
    show(0);
    var vio = new IntersectionObserver(function (es) {
      var vis = es[0].isIntersecting;
      if (vis && !running) { running = true; i = -1; step(); }
      else if (!vis && running) { running = false; clearTimeout(timer); }
    }, { threshold: 0.35 });
    vio.observe(stack.closest('.hero-stage, .stage') || stack);
  });

  /* GitHub release info for download buttons */
  function fmtSize(b) { return b > 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.round(b / 1024) + ' KB'; }
  function applyRelease(r) {
    if (!r) return;
    var tag = r.tag_name || '';
    $$('[data-ver]').forEach(function (el) { el.textContent = tag; });
    var date = (r.published_at || '').slice(0, 10);
    $$('[data-date]').forEach(function (el) { el.textContent = date; });
    $$('[data-releaselink]').forEach(function (a) { if (r.html_url) a.href = r.html_url; });
    var assets = (r.assets || []).filter(function (a) { return !/\.(sha256|sig|txt|blockmap)$/i.test(a.name); });
    var win = assets.filter(function (a) { return /win|windows|x64|x86|arm64|\.exe$|\.msi$|\.zip$/i.test(a.name); });
    var primary = win[0] || assets[0];
    $$('[data-dl]').forEach(function (a) { if (primary) a.href = primary.browser_download_url; });
    var list = $('#assets');
    if (list) {
      list.innerHTML = '';
      if (!assets.length) { list.innerHTML = '<div class="none">这个版本暂时没有可下载的文件，请到 GitHub Releases 查看。</div>'; return; }
      assets.forEach(function (a) {
        var el = d.createElement('a'); el.href = a.browser_download_url; el.rel = 'noopener';
        var n = d.createElement('span'); n.textContent = a.name;
        var s = d.createElement('span'); s.textContent = fmtSize(a.size);
        el.appendChild(n); el.appendChild(s); list.appendChild(el);
      });
    }
  }
  if ($('[data-ver],[data-dl],#assets')) {
    var cached = null;
    try { cached = JSON.parse(sessionStorage.getItem('cf-rel') || 'null'); } catch (e) {}
    if (cached) applyRelease(cached);
    else if (window.fetch) {
      fetch('https://api.github.com/repos/' + REPO + '/releases?per_page=8', { headers: { Accept: 'application/vnd.github+json' } })
        .then(function (r) { if (!r.ok) throw 0; return r.json(); })
        .then(function (a) {
          var r = (a || []).filter(function (x) { return !x.draft; })[0];
          if (r) { try { sessionStorage.setItem('cf-rel', JSON.stringify(r)); } catch (e) {} applyRelease(r); }
          else { var l = $('#assets'); if (l) l.innerHTML = '<div class="none">还没有发布版本，请稍后再来，或到 GitHub 查看进展。</div>'; }
        })
        .catch(function () { var l = $('#assets'); if (l) l.innerHTML = '<div class="none">暂时无法读取版本信息，请点击上方按钮前往 GitHub Releases 下载。</div>'; });
    }
  }

  /* language (translate.js, loaded only when needed) */
  var LANGS = { zh: 'chinese_simplified', tw: 'chinese_traditional', en: 'english' };
  var CDNS = [
    'https://cdn.jsdelivr.net/npm/i18n-jsautotranslate@3.18.66/translate.js',
    'https://cdn.staticfile.net/i18n-jsautotranslate/3.18.66/translate.js',
    'https://unpkg.com/i18n-jsautotranslate@3.18.66/translate.js'
  ];
  function loadTranslate(done) {
    if (window.translate) return done(true);
    var k = 0;
    (function next() {
      if (k >= CDNS.length) return done(false);
      var s = d.createElement('script'); s.src = CDNS[k++]; s.async = true;
      s.onload = function () { done(!!window.translate); };
      s.onerror = function () { s.remove(); next(); };
      d.head.appendChild(s);
    })();
  }
  function setLang(code) {
    store('cf-lang', code);
    markLang(code);
    if (code === 'zh' && !window.translate) return;
    loadTranslate(function (ok) {
      if (!ok) return;
      try {
        translate.selectLanguageTag.show = false;
        translate.service.use('client.edge');
        translate.language.setLocal('chinese_simplified');
        translate.listener.start();
        translate.changeLanguage(LANGS[code]);
      } catch (e) { /* translation is optional */ }
    });
  }
  function markLang(code) {
    $$('.langmenu button').forEach(function (b) { b.setAttribute('aria-checked', b.getAttribute('data-lang') === code); });
  }
  var lb = $('#lang'), lm = $('.langmenu');
  if (lb && lm) {
    lb.addEventListener('click', function (e) { e.stopPropagation(); lm.classList.toggle('open'); });
    d.addEventListener('click', function () { lm.classList.remove('open'); });
    $$('button', lm).forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.getAttribute('data-lang')); lm.classList.remove('open'); });
    });
    var cur = store('cf-lang') || 'zh'; markLang(cur);
    if (cur !== 'zh') setLang(cur);
  }

  /* about: toc highlight */
  var toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    var secs = toc.map(function (a) { return $(a.getAttribute('href')); }).filter(Boolean);
    var tio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) toc.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    secs.forEach(function (s) { tio.observe(s); });
  }
})();
