(function () {
  'use strict';
  var WI = {
    home: '<svg viewBox="0 0 24 24"><path d="M4 11l8-7 8 7M6 10v10h12V10"/></svg>',
    bell: '<svg viewBox="0 0 24 24"><path d="M6 17V11a6 6 0 0 1 12 0v6l1.5 2h-15zM10 21h4"/></svg>',
    plus: '<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',
    trash: '<svg viewBox="0 0 24 24"><path d="M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13"/></svg>',
    dots: '<svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="19" cy="12" r="1.3"/></svg>',
    up: '<svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
    down: '<svg viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    into: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v7M9 12l3 3 3-3"/></svg>',
    wrap: '<svg viewBox="0 0 24 24"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/></svg>',
    copy: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/></svg>',
    chevr: '<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>',
    chev: '<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>',
    tag: '<svg viewBox="0 0 24 24"><path d="M4 4h8l8 8-8 8-8-8zM8 8h.01"/></svg>',
    info: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/></svg>',
    x: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    eye: '<svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    lines: '<svg viewBox="0 0 24 24"><path d="M5 7h14M5 12h10M5 17h14"/></svg>',
    fill: '<svg viewBox="0 0 24 24"><path d="M12 3l7 8-7 8-7-8z"/><path d="M19 17a2 2 0 1 0 3 0c0-1-1.5-3-1.5-3S19 16 19 17z"/></svg>',
    font: '<svg viewBox="0 0 24 24"><path d="M3 19L9 5l6 14M5.5 14h7M16 19l2.5-6 2.5 6M17 17h3"/></svg>',
    gridi: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/></svg>',
    paint: '<svg viewBox="0 0 24 24"><path d="M5 20l-1-1 8-8 4 4-8 8zM12 11l5-8 4 4-8 5"/></svg>',
    half: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/></svg>',
    check2: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 9h16M9 4v16" opacity=".6"/></svg>',
    round: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/></svg>',
    split: '<svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M12 5v14"/></svg>',
    pin: '<svg viewBox="0 0 24 24"><path d="M9 4h6l-1 6 3 3H7l3-3zM12 13v7"/></svg>',
    width: '<svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="10" rx="2"/><path d="M7 12h10M7 12l2-2M7 12l2 2M17 12l-2-2M17 12l-2 2"/></svg>',
    margin: '<svg viewBox="0 0 24 24"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg>',
    code: '<svg viewBox="0 0 24 24"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg>',
    aL: '<svg viewBox="0 0 24 24"><path d="M5 5v14"/><rect x="8" y="7" width="9" height="4" rx="1"/><rect x="8" y="13" width="6" height="4" rx="1"/></svg>',
    aC: '<svg viewBox="0 0 24 24"><path d="M12 4v16"/><rect x="6" y="7" width="12" height="4" rx="1"/><rect x="8" y="13" width="8" height="4" rx="1"/></svg>',
    aR: '<svg viewBox="0 0 24 24"><path d="M19 5v14"/><rect x="7" y="7" width="9" height="4" rx="1"/><rect x="10" y="13" width="6" height="4" rx="1"/></svg>',
    aS: '<svg viewBox="0 0 24 24"><path d="M5 5v14M19 5v14"/><rect x="8" y="9" width="8" height="6" rx="1"/></svg>'
  };
  var CONTAINERS = ['轮播容器', '滚动容器', '分组容器', '堆叠容器'];
  var uid = 0;

  function guid() {
    var h = '0123456789abcdef', s = '';
    for (var i = 0; i < 36; i++) s += (i === 8 || i === 13 || i === 18 || i === 23) ? '-' : h.charAt(Math.floor(Math.random() * 16));
    return s;
  }
  function tg(on) { return '<span class="tg' + (on ? ' on' : '') + '"><i></i><span>' + (on ? '开' : '关') + '</span></span>'; }
  function sld(v) { return '<span class="sld" data-sld><i style="width:' + v + '%"></i><b style="left:' + v + '%"></b></span>'; }
  function card(icon, t, d, trail, cls) {
    return '<div class="sc wxs ' + (cls || '') + '"><span class="wxi">' + (WI[icon] || '') + '</span><div class="tx"><b>' + t + '</b><span>' + d + '</span></div>' + (trail || '') + '</div>';
  }
  function exp(icon, t, d, trailOn, open, body) {
    return '<div class="exp wxe' + (open ? ' open' : '') + '"><div class="eh"><span class="wxi">' + WI[icon] + '</span><div class="tx"><b>' + t + '</b><span>' + d + '</span></div>' + tg(trailOn) + '<span class="car">' + WI.chev + '</span></div><div class="eb">' + body + '</div></div>';
  }
  function combo(t) { return '<span class="sel wxsel" data-o="继承|是|否"><span class="v">' + t + '</span>' + WI.chev + '</span>'; }
  function head(icon, t) { return '<div class="wxh">' + WI[icon] + t + '</div>'; }

  function initPage(pg) {
    var root = pg.closest('.sapp');
    var lib = [];
    pg.querySelectorAll('.lib2 .li').forEach(function (li) {
      lib.push({ t: li.dataset.w, ico: li.querySelector('svg').outerHTML, d: li.querySelector('.tx span').textContent });
    });
    var src = pg.querySelector('.wxlibsrc'); if (src) src.remove();
    var st = { rows: [{ items: [] }], r: 0, cr: 0, i: -1, tab: 'lib', menu: null, sub: false, clip: null };
    var rowsEl = pg.querySelector('[data-wx-rows]'), tabsEl = pg.querySelector('[data-wx-tabs]'), paneEl = pg.querySelector('[data-wx-pane]');
    var toastEl = null, toastT = 0;

    function find(t) { for (var k = 0; k < lib.length; k++) if (lib[k].t === t) return lib[k]; return lib[0]; }
    function cur() { var r = st.rows[st.cr]; return r && st.i >= 0 ? r.items[st.i] : null; }

    function toast(msg) {
      if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'wxtoast'; root.appendChild(toastEl); }
      toastEl.innerHTML = '<span class="ti">' + WI.info + '</span><span>' + msg + '</span><span class="tx" data-wx="toastx">' + WI.x + '</span>';
      toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 3200);
    }

    function chipHtml(it, r, i) {
      var sel = r === st.cr && i === st.i;
      var kids = it.kids ? '<span class="wxk">' + it.kids.map(function (k) { return k.t; }).join('、') + '</span>' : '';
      var ctl = sel ? '<span class="wxm" data-wx="more">' + WI.dots + '</span><span class="wxd" data-wx="del">' + WI.trash + '</span>' : '';
      return '<div class="wxc' + (sel ? ' on' : '') + (sel && st.menu ? ' mo' : '') + '" data-i="' + i + '"><span class="wxci">' + it.ico + '</span><b>' + it.t + '</b>' + kids + ctl + '</div>';
    }
    function menuHtml() {
      var items = [['up', '向上移动一行', 'up'], ['down', '向下移动一行', 'down'], ['into', '移动到选中的容器', 'into', 1], ['wrap', '包裹到新容器', 'wrap', 0, 1], ['copy', '创建副本', 'copy']];
      var h = '<div class="wxmenu" data-menu>';
      items.forEach(function (m) {
        h += '<div class="wxmi' + (m[3] ? ' dis' : '') + (m[4] && st.sub ? ' wxon' : '') + '" data-wx="m-' + m[2] + '">' + WI[m[0]] + '<span>' + m[1] + '</span>' + (m[4] ? '<em>' + WI.chevr + '</em>' : '') + '</div>';
      });
      h += '</div>';
      if (st.sub) h += '<div class="wxmenu wxsub" data-sub>' + CONTAINERS.map(function (c) {
        var l = lib.filter(function (x) { return x.t === c; })[0];
        return '<div class="wxmi" data-wx="wrap-' + c + '">' + (l ? l.ico : '') + '<span>' + c + '</span></div>';
      }).join('') + '</div>';
      return h;
    }

    function drawRows() {
      var h = '';
      st.rows.forEach(function (row, r) {
        var act = r === st.r;
        h += '<div class="wxrow' + (act ? ' act' : '') + '" data-r="' + r + '"><span class="wxbar"></span><span class="wxgrip"><i></i><i></i></span><div class="wxchips">' +
          row.items.map(function (it, i) { return chipHtml(it, r, i); }).join('') + '</div>' +
          (act ? '<div class="wxtools"><span data-wx="rhome">' + WI.home + '</span><span class="acc" data-wx="rbell">' + WI.bell + '</span><span data-wx="radd">' + WI.plus + '</span><span class="red" data-wx="rdel">' + WI.trash + '</span></div>' : '') +
          (r === st.cr && st.i >= 0 && st.menu ? menuHtml() : '') + '</div>';
      });
      rowsEl.innerHTML = h;
      if (st.menu) placeMenu();
    }
    function placeMenu() {
      var m = rowsEl.querySelector('[data-menu]'); if (!m) return; var row = m.closest('.wxrow');
      var dots = row.querySelector('.wxm'); if (!dots) return;
      var rr = row.getBoundingClientRect(), dr = dots.getBoundingClientRect(), k = rr.width ? row.offsetWidth / rr.width : 1;
      var w = m.offsetWidth, left = (dr.left - rr.left + dr.width / 2) * k - w / 2;
      left = Math.max(6, Math.min(left, row.offsetWidth - w - 6));
      m.style.left = left + 'px'; m.style.top = (row.offsetHeight - 2) + 'px';
      var sub = rowsEl.querySelector('[data-sub]');
      if (sub) {
        var hl = m.querySelector('.wxon'), top = hl ? hl.offsetTop : 0, sw = sub.offsetWidth;
        var l2 = left + w - 2; if (l2 + sw > row.offsetWidth - 4) l2 = left - sw + 2;
        sub.style.left = l2 + 'px'; sub.style.top = (row.offsetHeight - 2 + top - 4) + 'px';
      }
    }

    function drawTabs() {
      var c = cur(), h = '<div class="wxtl">';
      h += '<span' + (st.tab === 'lib' ? ' class="on"' : '') + ' data-wx="tab-lib">组件库</span>';
      if (c) h += '<span' + (st.tab === 'comp' ? ' class="on"' : '') + ' data-wx="tab-comp">组件设置</span><span' + (st.tab === 'adv' ? ' class="on"' : '') + ' data-wx="tab-adv">高级设置</span>';
      h += '<span' + (st.tab === 'row' ? ' class="on"' : '') + ' data-wx="tab-row">行设置</span></div>';
      if (c) h += '<div class="wxhide">' + WI.tag + '<span class="cb wxcb"><i>' + WI.check + '</i>按规则则隐藏</span></div>';
      tabsEl.innerHTML = h;
    }

    function libPane() {
      return '<div class="grp">内置</div><div class="lib2">' + lib.map(function (l) {
        return '<div class="li" data-w="' + l.t + '">' + l.ico + '<span class="tx"><b>' + l.t + '</b><span>' + l.d + '</span></span></div>';
      }).join('') + '</div>';
    }
    function compPane(c) {
      var t = c.t;
      if (t === '文本') return card('lines', '文本内容', '要显示的文本。', '<span class="inp wxin" contenteditable="true" spellcheck="false"></span>') +
        card('fill', '自定义字体颜色', '选择要显示文本的颜色。', '<span class="wxclr"><i></i>' + WI.chev + '</span>' + tg(true)) +
        card('font', '字体大小', '修改要显示的文本的大小。', sld(0));
      if (t === '分割线') return '<div class="wxnone">此组件没有可调整的设置。</div>';
      if (t === '时钟') return card('clock', '显示秒', '在时钟上显示秒数。', tg(true)) + card('font', '字体大小', '修改要显示的文本的大小。', sld(0));
      if (t === '倒计时') return card('cal', '倒计时名称', '倒计时要显示的名称。', '<span class="inp wxin" contenteditable="true" spellcheck="false"></span>') + card('clock', '目标日期', '倒计时的目标日期。', combo('选择日期'));
      if (CONTAINERS.indexOf(t) >= 0) return '<div class="wxnone">容器内的组件：' + ((c.kids && c.kids.length) ? c.kids.map(function (k) { return k.t; }).join('、') : '暂无') + '</div>';
      return card('font', '字体大小', '修改要显示的文本的大小。', sld(0));
    }
    function advPane(c) {
      var al = ['aL', 'aC', 'aR', 'aS'].map(function (k, n) { return '<span class="' + (n === 0 ? 'on' : '') + '" data-wx="al">' + WI[k] + '</span>'; }).join('');
      return card('eye', '按规则则隐藏', '在指定规则满足时，自动隐藏此组件。注意此处的隐藏不会释放组件资源。', tg(false)) +
        head('paint', '外观') +
        card('half', '不透明度', '组件整体的不透明度。', sld(100)) +
        exp('paint', '自定义背景效果', '自定义主界面的背景效果，仅在较新版本的 Windows 上可用，可能会产生额外性能开销。', false, false, '').replace('<span class="tg"><i></i><span>关</span></span>', combo('继承')) +
        card('fill', '自定义背景颜色', '当前组件背景颜色，禁用时将使用上级默认值。', tg(false)) +
        card('check2', '自定义背景不透明度', '当前组件的背景的不透明度，禁用将使用上级默认值。', tg(false)) +
        card('round', '自定义背景圆角半径', '当前组件背景圆角半径，调至最大数值时左右边缘为半圆。', tg(false)) +
        head('font', '字体') +
        exp('font', '字体大小', '调整组件上各类字体的大小，将覆盖【外观】设置和主界面行中设置的字体大小。', false, false, '<div class="wxnone">开启后可分别调整各类字体的大小。</div>') +
        card('fill', '字体颜色', '调整字体颜色，将覆盖【外观】设置和主界面行中设置的值。', tg(false)) +
        head('gridi', '布局') +
        card('split', '对齐方式', '指定组件在显示容器中对齐的方式。', '<span class="wxal">' + al + '</span>') +
        card('pin', '固定宽度', '启用后，组件将使用固定宽度，不会自动适应内容宽度。', tg(false)) +
        exp('width', '宽度限制', '限制控件的最大和最小宽度。', false, true, '<div class="wxsub2">' + tg(false).replace('<span>关</span>', '<span></span>') + '<b>最小宽度</b></div><div class="wxsub2">' + tg(false).replace('<span>关</span>', '<span></span>') + '<b>最大宽度</b></div>').replace(/<span class="tg"><i><\/i><span>关<\/span><\/span><span class="car">/, '<span class="car">') +
        exp('margin', '自定义边距', '设置此组件与其他组件的距离。', false, false, '<div class="wxnone">开启后可分别设置上下左右的边距。</div>') +
        '<div class="wxid">' + WI.code + c.id + '</div>';
    }
    function rowPane() {
      return card('eye', '按规则则隐藏', '在指定规则满足时，自动隐藏此组件。注意此处的隐藏不会释放组件资源。', tg(false)) +
        card('split', '分体主界面', '启用后主界面会分开。', combo('继承')) +
        head('paint', '外观') +
        card('half', '不透明度', '主界面行整体的不透明度。', sld(100)) +
        exp('paint', '自定义背景效果', '自定义主界面的背景效果，仅在较新版本的 Windows 上可用，可能会产生额外性能开销。', false, false, '').replace('<span class="tg"><i></i><span>关</span></span>', combo('继承')) +
        card('fill', '自定义背景颜色', '当前主界面行背景颜色，禁用时将使用上级默认值。', tg(false)) +
        card('check2', '自定义背景不透明度', '当前主界面行的背景的不透明度，禁用将使用上级默认值。', tg(false)) +
        card('round', '自定义背景圆角半径', '当前主界面行背景圆角半径，调至最大数值时左右边缘为半圆。', tg(false)) +
        head('font', '字体') +
        exp('font', '字体大小', '调整组件上各类字体的大小，将覆盖【外观】设置和主界面行中设置的字体大小。', false, false, '<div class="wxnone">开启后可分别调整各类字体的大小。</div>') +
        card('fill', '字体颜色', '调整字体颜色，将覆盖【外观】设置和主界面行中设置的值。', tg(false));
    }
    function drawPane() {
      var c = cur(), keep = paneEl.scrollTop;
      if (st.tab === 'lib') paneEl.innerHTML = libPane();
      else if (st.tab === 'comp' && c) paneEl.innerHTML = compPane(c);
      else if (st.tab === 'adv' && c) paneEl.innerHTML = advPane(c);
      else paneEl.innerHTML = rowPane();
      paneEl.scrollTop = keep;
    }
    function draw() { drawRows(); drawTabs(); drawPane(); }

    function make(t) { var l = find(t); return { t: t, ico: l.ico, id: guid(), kids: CONTAINERS.indexOf(t) >= 0 ? [] : null }; }
    function addAt(r, idx, t) {
      var row = st.rows[r]; if (idx == null || idx > row.items.length) idx = row.items.length;
      row.items.splice(idx, 0, make(t)); st.r = r; st.cr = r; st.i = idx; st.tab = 'comp'; st.menu = null; st.sub = false; draw();
    }
    function moveRow(dir) {
      var c = cur(); if (!c) return;
      st.rows[st.cr].items.splice(st.i, 1);
      var dst = st.cr + dir, made = false;
      if (dst < 0) { st.rows.unshift({ items: [] }); dst = 0; made = true; st.r += 1; }
      else if (dst >= st.rows.length) { st.rows.push({ items: [] }); made = true; }
      st.rows[dst].items.push(c);
      st.cr = dst; st.i = st.rows[dst].items.length - 1; st.menu = null; st.sub = false; st.tab = 'comp';
      draw();
      toast(made ? (dir > 0 ? '已向下创建新主界面行。' : '已向上创建新主界面行。') : (dir > 0 ? '已向下移动一行。' : '已向上移动一行。'));
    }

    pg.addEventListener('click', function (e) {
      var t = e.target, a = t.closest('[data-wx]'), el;
      if (a) {
        var k = a.dataset.wx;
        if (k.indexOf('tab-') === 0) { st.tab = k.slice(4); st.menu = null; draw(); return; }
        if (k === 'more') { st.menu = !st.menu; st.sub = false; drawRows(); return; }
        if (k === 'del') { st.rows[st.cr].items.splice(st.i, 1); st.i = -1; st.menu = null; st.tab = 'lib'; draw(); return; }
        if (k === 'm-up') return moveRow(-1);
        if (k === 'm-down') return moveRow(1);
        if (k === 'm-into') return;
        if (k === 'm-wrap') { st.sub = !st.sub; drawRows(); return; }
        if (k === 'm-copy') { var c = cur(), cp = make(c.t); cp.kids = c.kids ? c.kids.slice() : null; st.rows[st.cr].items.splice(st.i + 1, 0, cp); st.i += 1; st.menu = null; st.sub = false; draw(); return; }
        if (k.indexOf('wrap-') === 0) { var cc = cur(), w = make(k.slice(5)); w.kids = [cc]; st.rows[st.cr].items[st.i] = w; st.menu = null; st.sub = false; st.tab = 'comp'; draw(); return; }
        if (k === 'radd') { st.rows.splice(st.r + 1, 0, { items: [] }); toast('已向下创建新主界面行。'); drawRows(); return; }
        if (k === 'rdel') { if (st.rows.length > 1) st.rows.splice(st.r, 1); else st.rows[0].items = []; st.r = Math.max(0, Math.min(st.r, st.rows.length - 1)); st.cr = st.r; st.i = -1; st.menu = null; st.tab = 'lib'; draw(); return; }
        if (k === 'al') { a.parentNode.querySelectorAll('span').forEach(function (x) { x.classList.toggle('on', x === a); }); return; }
        if (k === 'toastx') { toastEl.classList.remove('on'); return; }
        return;
      }
      if ((el = t.closest('.wxc'))) {
        st.r = st.cr = +el.closest('.wxrow').dataset.r; st.i = +el.dataset.i; st.menu = null; st.sub = false; st.tab = 'comp'; draw(); return;
      }
      if ((el = t.closest('.wxrow')) && !t.closest('.wxmenu') && !t.closest('.wxtools')) {
        st.r = st.cr = +el.dataset.r; st.i = -1; st.menu = null; st.sub = false; if (st.tab === 'comp' || st.tab === 'adv') st.tab = 'lib'; draw(); return;
      }
      if (st.menu && !t.closest('.wxmenu')) { st.menu = null; st.sub = false; drawRows(); }
    });

    var drag = null;
    pg.addEventListener('pointerdown', function (e) {
      var li = e.target.closest('.li'); if (!li || e.button) return;
      drag = { li: li, x: e.clientX, y: e.clientY, on: false, ghost: null, id: e.pointerId };
    });
    function dropTarget(x, y) {
      var rows = rowsEl.querySelectorAll('.wxrow'), hit = null;
      rows.forEach(function (r) { var b = r.getBoundingClientRect(); if (y >= b.top - 2 && y <= b.bottom + 2 && x >= b.left && x <= b.right) hit = r; });
      if (!hit) return null;
      var idx = 0, ch = hit.querySelectorAll('.wxc');
      ch.forEach(function (c, n) { var b = c.getBoundingClientRect(); if (x > b.left + b.width / 2) idx = n + 1; });
      return { el: hit, r: +hit.dataset.r, idx: idx };
    }
    document.addEventListener('pointermove', function (e) {
      if (!drag) return;
      if (!drag.on) {
        if (Math.abs(e.clientX - drag.x) + Math.abs(e.clientY - drag.y) < 6) return;
        drag.on = true; drag.li.classList.add('wxsrc');
        var g = drag.li.cloneNode(true); g.className = 'li wxghost'; g.style.width = drag.li.offsetWidth + 'px';
        document.body.appendChild(g); drag.ghost = g;
      }
      drag.ghost.style.left = (e.clientX - 30) + 'px'; drag.ghost.style.top = (e.clientY - 20) + 'px';
      var d = dropTarget(e.clientX, e.clientY);
      rowsEl.querySelectorAll('.wxrow').forEach(function (r) { r.classList.toggle('drop', !!d && r === d.el); });
    });
    document.addEventListener('pointerup', function (e) {
      if (!drag) return; var d0 = drag; drag = null;
      rowsEl.querySelectorAll('.wxrow').forEach(function (r) { r.classList.remove('drop'); });
      if (!d0.on) { addAt(st.r, null, d0.li.dataset.w); return; }
      d0.li.classList.remove('wxsrc'); if (d0.ghost) d0.ghost.remove();
      var d = dropTarget(e.clientX, e.clientY); if (d) addAt(d.r, d.idx, d0.li.dataset.w);
    });
    document.addEventListener('pointercancel', function () { if (!drag) return; if (drag.ghost) drag.ghost.remove(); drag.li.classList.remove('wxsrc'); drag = null; });

    pg.addEventListener('pointerdown', function (e) {
      var s = e.target.closest('[data-sld]'); if (!s) return;
      function set(ev) { var r = s.getBoundingClientRect(), k = r.width ? s.offsetWidth / r.width : 1, p = Math.max(0, Math.min(100, (ev.clientX - r.left) * k / s.offsetWidth * 100)); s.firstElementChild.style.width = p + '%'; s.lastElementChild.style.left = p + '%'; }
      s.setPointerCapture(e.pointerId); set(e); s.onpointermove = set; s.onpointerup = function () { s.onpointermove = null; };
    });
    document.addEventListener('click', function (e) { if (st.menu && e.composedPath().indexOf(pg) < 0) { st.menu = null; st.sub = false; drawRows(); } });
    draw();
  }

  function boot() { document.querySelectorAll('.sapp .wxpg').forEach(initPage); }
  boot();
})();
