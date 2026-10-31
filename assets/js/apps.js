/* ClassFabric 官网：软件界面的交互复刻（换课 / 档案编辑 / 设置页）。纯原生 JS，无依赖。 */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var I = {
    doc: '<svg viewBox="0 0 24 24"><path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/></svg>',
    right: '<svg viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    swap: '<svg viewBox="0 0 24 24"><path d="M4 8h15M15 4l4 4-4 4M20 16H5M9 12l-4 4 4 4"/></svg>',
    x: '<svg viewBox="0 0 24 24"><path d="M5 5l14 14M19 5L5 19"/></svg>',
    back: '<svg viewBox="0 0 24 24"><path d="M20 12H5M11 6l-6 6 6 6"/></svg>',
    check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    chev: '<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>'
  };
  function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  var WIN_CTL = '<span class="ctl"><i><svg viewBox="0 0 10 10"><path d="M0 5h10"/></svg></i><i><svg viewBox="0 0 10 10"><rect x=".5" y=".5" width="9" height="9"/></svg></i><i><svg viewBox="0 0 10 10"><path d="M0 0l10 10M10 0L0 10"/></svg></i></span>';

  /* ================= 换课 ================= */
  var SUBJECTS = ['语文', '数学', '英语', '历史', '政治', '物理', '化学', '生物', '地理', '信息技术', '体育', '自习', '通用技术', '音乐', '美术'];
  var TIMES = ['08:00-08:35', '09:15-09:55', '10:05-10:45', '10:55-11:35', '11:45-12:25', '12:35-13:15', '13:25-14:05', '14:15-14:55', '15:05-15:45'];
  var DAY = ['语文', '语文', '数学', '数学', '英语', '英语', '物理', '物理', '化学'];
  function T(t) { return t.replace('-', '–'); }

  function initSwap(root) {
    var lessons = DAY.slice(), st;
    function reset() { st = { step: 0, first: -1, second: -1, mode: 'swap', pick: '', perm: false, open: false, done: false }; }
    reset();
    function sub(n) { return n.charAt(0); }
    function chars(skipFirst) {
      return lessons.map(function (n, i) {
        var cls = 'ls';
        if (st.step === 2 && st.mode === 'swap' && i === st.second) {
          return '<span class="ls sel2" data-i="' + i + '"><b>' + esc(n) + '</b><small>' + T(TIMES[i]) + '</small></span>';
        }
        if (st.step >= 1 && i === st.first) cls += ' gone';
        return '<span class="' + cls + '" data-i="' + i + '">' + esc(sub(n)) + '</span>';
      }).join('');
    }
    function render() {
      var temp = st.mode === 'replace' && st.step >= 1;
      var hint = st.step === 0 ? '选择要调换的课程。' : '选择要与刚刚选择的课程调换的课程。点击复选框可以切换调换模式。';
      var h = '<div class="wt"><span>换课</span>' + WIN_CTL + '</div><div class="sbody"><div class="top"><h2>换课</h2><span class="day">' + I.doc + '<b>周六' + (temp ? '（临时层）' : '') + '</b></span><span class="hint">' + I.right + hint + '</span></div>';
      if (st.done) {
        h += '<div class="mid done">' + I.check + '已完成换课</div>';
      } else if (st.step === 0) {
        h += '<div class="mid">' + chars() + '</div>';
      } else {
        var f = '<div class="first"><b>' + esc(lessons[st.first]) + '</b><small>' + T(TIMES[st.first]) + '</small></div>';
        var seg = '<div class="seg"><span class="' + (st.mode === 'replace' ? 'on' : '') + '" data-m="replace">' + I.right + (st.mode === 'replace' ? '<em>替换</em>' : '') + '</span><span class="' + (st.mode === 'swap' ? 'on' : '') + '" data-m="swap">' + I.swap + (st.mode === 'swap' ? '<em>交换</em>' : '') + '</span></div>';
        var right;
        if (st.mode === 'swap') right = '<div class="chs">' + chars() + '</div>';
        else {
          right = '<div class="to"><label>换课成…</label><div class="combo' + (st.open ? ' open' : '') + '" data-c><span>' + esc(st.pick) + '</span>' + I.chev + '</div>' +
            (st.open ? '<div class="fly open sl">' + SUBJECTS.map(function (n) { return '<div class="mi' + (n === st.pick ? ' on' : '') + '" data-n="' + n + '">' + n + '</div>'; }).join('') + '</div>' : '') + '</div>';
        }
        h += '<div class="mid two">' + f + seg + right + '</div>';
      }
      var ready = st.mode === 'swap' ? st.second >= 0 : !!st.pick;
      h += '</div><div class="bar"><span class="btn2" data-a="cancel">' + I.x + '取消</span>' + (st.step ? '<span class="btn2" data-a="back">' + I.back + '上一步</span>' : '') + '<span class="lnk">高级换课…</span><span class="sp"></span>' +
        (st.step && st.mode === 'swap' && ready ? '<label class="cbx"><input type="checkbox" data-a="perm"' + (st.perm ? ' checked' : '') + '><i>' + I.check + '</i>永久换课</label>' : '') +
        (ready && !st.done ? '<span class="btn2 acc" data-a="ok">' + I.check + '确认换课</span>' : '') + '</div>';
      root.innerHTML = h;
    }
    root.addEventListener('click', function (e) {
      var t = e.target;
      var ls = t.closest('.ls'); if (ls && !st.done) {
        var i = +ls.dataset.i;
        if (st.step === 0) { st.first = i; st.step = 1; }
        else if (st.mode === 'swap' && i !== st.first) { st.second = i; st.step = 2; }
        render(); return;
      }
      var m = t.closest('[data-m]'); if (m && st.step >= 1) { st.mode = m.dataset.m; st.second = -1; st.pick = ''; st.open = false; st.step = 1; render(); return; }
      if (t.closest('[data-c]')) { st.open = !st.open; render(); return; }
      var n = t.closest('.mi[data-n]'); if (n) { st.pick = n.dataset.n; st.open = false; render(); return; }
      var a = t.closest('[data-a]'); if (!a) return;
      var k = a.dataset.a;
      if (k === 'cancel') { reset(); render(); }
      else if (k === 'back') {
        if (st.mode === 'swap' && st.step === 2) { st.second = -1; st.step = 1; }
        else { st.first = -1; st.second = -1; st.pick = ''; st.open = false; st.mode = 'swap'; st.step = 0; }
        render();
      } else if (k === 'perm') { st.perm = a.checked; }
      else if (k === 'ok') {
        if (st.mode === 'swap') { var x = lessons[st.first]; lessons[st.first] = lessons[st.second]; lessons[st.second] = x; }
        else lessons[st.first] = st.pick;
        st.done = true; render();
        setTimeout(function () { var keep = lessons; reset(); lessons = keep; render(); }, 1600);
      }
    });
    render();
  }
  $$('[data-app="swap"]').forEach(initSwap);

  /* ============ 应用设置（可交互） ============ */
  var CHEV_UP = null;
  function initSettings(host){
    var tpl = document.getElementById('tpl-settings'); if(!tpl) return;
    host.appendChild(tpl.content.cloneNode(true));
    var root = host.querySelector('.sapp');
    if (host.dataset.h) root.style.setProperty('--h', host.dataset.h + 'px');
    function go(k){
      root.querySelectorAll('.pgx').forEach(function(p){p.classList.toggle('on', p.dataset.p===k)});
      root.querySelectorAll('.nv .it[data-go]').forEach(function(n){n.classList.toggle('on', n.dataset.go===k)});
    }
    go(host.dataset.start || 'remind');
    function sel(prov){
      root.querySelectorAll('.prov').forEach(function(p){p.classList.toggle('on', p===prov)});
      var i = +prov.dataset.prov, names=['上下课提醒','放学提醒','天气预警','行动提醒'];
      var pg = prov.closest('.pgx'); pg.querySelectorAll('.chan').forEach(function(c){c.hidden = i!==0});
      var d = pg.querySelector('.rdetail'); d.hidden=false; pg.querySelector('.rempty').hidden=true;
      d.querySelector('h3').textContent = names[i];
      d.querySelectorAll('.scr[data-pane="b"] .exp').forEach(function(e){e.hidden = i!==0});
      var inf = d.querySelector('.info'); if(inf) inf.hidden = false;
    }
    root.addEventListener('click', function(e){
      var t = e.target;
      var n = t.closest('.nv .it[data-go]'); if(n){ go(n.dataset.go); return; }
      var pv = t.closest('.prov'); if(pv){ sel(pv); return; }
      var ch = t.closest('.ch-h'); if(ch){ ch.closest('.chan').classList.toggle('shut'); return; }
      var ci = t.closest('.ci'); if(ci){ ci.parentNode.querySelectorAll('.ci').forEach(function(x){x.classList.toggle('on',x===ci)}); return; }
      var tb = t.closest('[data-tabs] > span'); if(tb){
        var bar = tb.parentNode, scope = bar.parentNode; bar.querySelectorAll('span').forEach(function(x){x.classList.toggle('on',x===tb)});
        scope.querySelectorAll(':scope > [data-pane]').forEach(function(p){p.hidden = p.dataset.pane !== tb.dataset.t}); return; }
      var tgl = t.closest('.tg'); if(tgl){ e.stopPropagation(); tgl.classList.toggle('on'); var l=tgl.querySelector('span'); if(l && /^[开关]$/.test(l.textContent)) l.textContent = tgl.classList.contains('on')?'开':'关';
        var sc = tgl.closest('.sc'); if(sc && /特殊高级设置/.test(sc.textContent)){ var dv=sc.nextElementSibling; if(dv) dv.classList.toggle('live', tgl.classList.contains('on')); } return; }
      var cbx = t.closest('.cb'); if(cbx){ cbx.classList.toggle('on'); return; }
      var eh = t.closest('.eh'); if(eh){ eh.parentNode.classList.toggle('open'); return; }
      var sg = t.closest('.num em i'); if(sg){ var nn = sg.closest('.num').querySelector('[data-edit]'); var v=parseInt(nn.textContent,10)||0; nn.textContent = Math.max(0, v + (+sg.dataset.s)*(v>=100?10:1)); return; }
      var so = t.closest('.sel[data-o]'); if(so){ var o = so.dataset.o.split('|'), vv = so.querySelector('.v'), k = o.indexOf(vv.textContent); vv.textContent = o[(k+1)%o.length]; return; }
      var dk = t.closest('.dock'); if(dk){ dk.parentNode.querySelectorAll('.dock').forEach(function(x){x.classList.toggle('on',x===dk)}); return; }
      var li = t.closest('.li'); if(li){
        var box = root.querySelector('#wchips') || li.closest('.pgx').querySelector('.chips2'); var sp = document.createElement('span'); sp.className='wc';
        sp.innerHTML = li.querySelector('svg').outerHTML + li.querySelector('.tx b').textContent; box.appendChild(sp); selChip(sp); return; }
      var wc = t.closest('.wc'); if(wc){ selChip(wc); return; }
      var rd = t.closest('.ib.red'); if(rd){ var cur = rd.closest('.pgx').querySelector('.wc.on'); if(cur) cur.remove(); return; }
      var x = t.closest('.ibar .x'); if(x){ x.parentNode.remove(); return; }
    });
    function selChip(c){ c.parentNode.querySelectorAll('.wc').forEach(function(x){x.classList.toggle('on',x===c)}); }
    // 滑块
    root.querySelectorAll('[data-sld]').forEach(function(s){
      function set(ev){ var r=s.getBoundingClientRect(), p=Math.max(0,Math.min(100,(ev.clientX-r.left)/r.width*100)); s.firstElementChild.style.width=p+'%'; s.lastElementChild.style.left=p+'%';
        var nb = s.parentNode.querySelector('.num [data-edit]'); if(nb) nb.textContent = Math.round(p/100*20); }
      s.addEventListener('pointerdown', function(ev){ s.setPointerCapture(ev.pointerId); set(ev); s.onpointermove=set; });
      s.addEventListener('pointerup', function(){ s.onpointermove=null; });
    });
  }
  $$('[data-app="settings"]').forEach(initSettings);
})();
