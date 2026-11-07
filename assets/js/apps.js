
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
    chev: '<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>',
    cal: '<svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>',
    sync: '<svg viewBox="0 0 24 24"><path d="M20 11a8 8 0 0 0-14-4M4 4v4h4M4 13a8 8 0 0 0 14 4M20 20v-4h-4"/></svg>',
    info: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/></svg>',
    stack: '<svg viewBox="0 0 24 24"><path d="M12 4l9 5-9 5-9-5zM3 14l9 5 9-5"/></svg>',
    trash: '<svg viewBox="0 0 24 24"><path d="M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13"/></svg>',
    plus: '<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',
    undo: '<svg viewBox="0 0 24 24"><path d="M9 7L4 12l5 5M4 12h10a6 6 0 0 1 0 12"/></svg>',
    clock: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    book: '<svg viewBox="0 0 24 24"><rect x="6" y="3" width="12" height="18" rx="2"/><path d="M9 3v7l2-1.5 2 1.5V3"/></svg>',
    hist: '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 3-6.2M4 4v4h4M12 8v4l3 2"/></svg>',
    split: '<svg viewBox="0 0 24 24"><rect x="5" y="4" width="14" height="6" rx="1"/><rect x="5" y="14" width="14" height="6" rx="1"/><path d="M3 12h18"/></svg>',
    bolt: '<svg viewBox="0 0 24 24"><path d="M13 3L5 14h6l-1 7 8-11h-6z"/></svg>',
    copy: '<svg viewBox="0 0 24 24"><rect x="8" y="8" width="11" height="12" rx="2"/><path d="M5 16V6a2 2 0 0 1 2-2h8"/></svg>',
    redo: '<svg viewBox="0 0 24 24"><path d="M15 7l5 5-5 5M20 12H10a6 6 0 0 0 0 12"/></svg>',
    minus: '<svg viewBox="0 0 24 24"><path d="M5 12h14"/></svg>',
    dots: '<svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="19" cy="12" r="1.2"/></svg>',
    up: '<svg viewBox="0 0 24 24"><path d="M6 15l6-6 6 6"/></svg>',
    list: '<svg viewBox="0 0 24 24"><path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/></svg>',
    cal2: '<svg viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M5 9h14"/></svg>',
    fit: '<svg viewBox="0 0 24 24"><path d="M5 4h14M12 8v8M9 13l3 3 3-3M5 20h14"/></svg>',
    zin: '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/></svg>',
    zout: '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M8 11h6"/></svg>',
    loc: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>',
    gear: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/></svg>',
    layers: '<svg viewBox="0 0 24 24"><path d="M12 4l8 4-8 4-8-4zM4 12l8 4 8-4"/></svg>',
    cloud: '<svg viewBox="0 0 24 24"><path d="M7 18a4 4 0 0 1 0-8 5 5 0 0 1 9.7-1A4.5 4.5 0 0 1 17 18z"/></svg>',
    shield: '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>'
  };
  function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  var WIN_CTL = '<span class="ctl"><i><svg viewBox="0 0 10 10"><path d="M0 5h10"/></svg></i><i><svg viewBox="0 0 10 10"><rect x=".5" y=".5" width="9" height="9"/></svg></i><i><svg viewBox="0 0 10 10"><path d="M0 0l10 10M10 0L0 10"/></svg></i></span>';

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
      var h = '<div class="wt"><span>换课</span>' + WIN_CTL + '</div><div class="sbody"><div class="top"><h2>换课</h2><span class="day">' + I.doc + '<b>周' + '日一二三四五六'.charAt(new Date().getDay()) + (temp ? '（临时层）' : '') + '</b></span><span class="hint">' + I.right + hint + '</span></div>';
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
      var fl = root.querySelector('.fly.sl'), sg = root.closest('.vdks');
      if (fl && sg) {
        var sr = sg.getBoundingClientRect(), k = sr.width / sg.offsetWidth || 1, fr = fl.getBoundingClientRect();
        var room = (sr.bottom - fr.top) / k - (sg.closest('.m') ? 52 : 62);
        if (room < fl.scrollHeight) fl.style.maxHeight = Math.max(110, room) + 'px';
      }
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
      if (k === 'cancel') { reset(); render(); if (root.dataset.modal) root.dispatchEvent(new Event('swclose', { bubbles: true })); }
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
      var x = t.closest('.ibar .x'); if(x){ x.parentNode.remove(); return; }
    });
    root.querySelectorAll('[data-sld]').forEach(function(s){
      function set(ev){ var r=s.getBoundingClientRect(), p=Math.max(0,Math.min(100,(ev.clientX-r.left)/r.width*100)); s.firstElementChild.style.width=p+'%'; s.lastElementChild.style.left=p+'%';
        var nb = s.parentNode.querySelector('.num [data-edit]'); if(nb) nb.textContent = Math.round(p/100*20); }
      s.addEventListener('pointerdown', function(ev){ s.setPointerCapture(ev.pointerId); set(ev); s.onpointermove=set; });
      s.addEventListener('pointerup', function(){ s.onpointermove=null; });
    });
  }
  $$('[data-app="settings"]').forEach(initSettings);
  $$('[data-app="settings"][data-start="remind"]').forEach(function(h){ var f=h.querySelector('.prov'); if(f) f.click(); });

  function initEditor(root){
    var body = root.querySelector('.e2body');
    var PX = 1.8, T0 = 6*60, T1 = 18*60;
    var subj = [['语文','语','#e5576b'],['数学','数','#5a78d8'],['英语','英','#7e62d3'],['历史','历','#c58b3d'],['政治','政','#df4f6d'],['物理','物','#3a9ae2'],['化学','化','#2fb2a1'],['生物','生','#4faf53'],['地理','地','#8bb347'],['信息技术','信','#2f9cc9'],['体育','体','#f0872e'],['自习','自','#6c7d9d'],['通用技术','技','#a8774f'],['音乐','音','#c05fd0'],['美术','美','#e07a5f'],['选修','选','#5a8f7b'],['社团','社','#d4a017'],['心理','心','#7aa2f7'],['早读','早','#e9a23b'],['班会','班','#4aa3a3'],['测验','测','#b5546a']];
    subj = subj.map(function(x){return {n:x[0],a:x[1],c:x[2],o:x[0]==='体育'}});
    var SLOTS = [[480,515],[555,595],[605,645],[655,695],[705,745],[755,795],[805,845],[855,895],[905,945]];
    var blocks = [];
    SLOTS.forEach(function(sl,i){ if(i>0) blocks.push({s:SLOTS[i-1][1],e:sl[0],k:'b'}); blocks.push({s:sl[0],e:sl[1],k:'k'}); });
    I.edit = '<svg viewBox="0 0 24 24"><path d="M4 20l1-4L16.5 4.5a2.1 2.1 0 013 3L8 19z"/></svg>';
    I.grid = '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 10h16M4 15h16M10 4v16"/></svg>';
    I.tip = '<svg viewBox="0 0 24 24"><path d="M5 5l14 7-14 7z"/></svg>';
    var days = ['日','一','二','三','四','五','六'], NOW = new Date(), TODAY = NOW.getDay(), dates = [];
    function p2(n){ return (n<10?'0':'')+n; }
    for (var di=0; di<7; di++){ var dd = new Date(NOW.getFullYear(), NOW.getMonth(), NOW.getDate()-TODAY+di); dates.push(p2(dd.getMonth()+1)+'/'+p2(dd.getDate())); }
    var NOWTXT = NOW.getFullYear()+'/'+(NOW.getMonth()+1)+'/'+NOW.getDate();
    var SY = NOW.getMonth()>=8 ? NOW.getFullYear() : NOW.getFullYear()-1, WEEKN = (function(){ var a = new Date(SY,8,1); a.setDate(a.getDate()-a.getDay()); var b = new Date(NOW.getFullYear(),NOW.getMonth(),NOW.getDate()); b.setDate(b.getDate()-b.getDay()); return Math.max(1, Math.round((b-a)/864e5/7)+1); })();
    var sched = {};
    var SEED = root.dataset.seed === 'real';
    if (SEED) {
      sched[1] = SLOTS.map(function(x,r){ return r===0 ? '语文' : null; });
      sched[6] = ['语文','语文','数学','数学','英语','英语','物理','物理','化学'];
    }
    var st = {tinfo:false, v:'grid', cell:SEED?null:[TODAY,0], auto:true, tl:3, sj:0, hist:[], redo:[], pop:false, sv:'grid', cm:0, temp:{}, tpop:null, swd:false};
    function hm(m){ return ('0'+Math.floor(m/60)).slice(-2)+':'+('0'+m%60).slice(-2); }
    function pm(v){ var a=v.split(':'); return (+a[0])*60+(+a[1]); }
    function classes(){ return blocks.filter(function(b){return b.k==='k'}); }
    function snap(){ st.hist.push(JSON.stringify(blocks)); if(st.hist.length>60) st.hist.shift(); st.redo=[]; }
    function ic(n){ return I[n] || ''; }
    function esc(x){ return String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }

    function toolbar(items){ return '<div class="e2tool">'+items.map(function(x){ return x==='|' ? '<b></b>' : '<span class="'+(x[2]||'')+'" data-a="'+x[0]+'">'+(I[x[3]]||'')+'<em>'+x[1]+'</em></span>'; }).join('')+'</div>'; }

    function viewSw(on, three){
      return '<div class="vsw">'+(three?'<span class="'+(on==='list'?'on':'')+'">'+I.list+'</span>':'')+'<span class="'+(on==='grid'?'on':'')+'" data-sv="grid">'+I.grid+'</span><span class="'+(on==='cal'?'on':'')+'" data-sv="cal">'+I.cal2+'</span></div>';
    }
    function dayHead(i, readOnly){
      var has = !!sched[i];
      return '<th class="'+(i===TODAY?'today':'')+(has?' has':'')+'"><div class="h1"><span>周'+days[i]+'</span><small>'+dates[i]+'</small></div>'+
        (has ? '<div class="h2"><b>周'+days[i]+'</b><i>'+I.gear+'</i></div>' : readOnly ? '' : '<span class="nb" data-new="'+i+'">'+I.plus+'新课表</span>')+'</th>';
    }
    function tableHtml(readOnly){
      var cl = classes(), th='<th class="t0">时间</th>', any = Object.keys(sched).length > 0;
      days.forEach(function(d,i){ th += dayHead(i, readOnly); });
      var rows='';
      cl.forEach(function(b,r){
        var tr='<td class="t">'+hm(b.s)+'-'+hm(b.e)+'</td>';
        days.forEach(function(d,i){
          var v = sched[i] && sched[i][r];
          tr += sched[i] ? '<td class="c'+(st.cell&&st.cell[0]===i&&st.cell[1]===r?' sel':'')+(v?'':' no')+'" data-d="'+i+'" data-r="'+r+'">'+(v||'（无）')+'</td>' : '<td></td>';
        });
        rows += '<tr>'+tr+'</tr>';
      });
      return '<table class="tt2"><thead><tr>'+th+'</tr></thead>'+(any||readOnly?'<tbody>'+rows+'</tbody>':'')+'</table>'+(any||readOnly?'':'<div class="emp2"><svg viewBox="0 0 48 48"><rect x="6" y="6" width="36" height="36" rx="9" stroke-dasharray="9 7"/></svg><p>这里还没有课表。不妨先点击上方的【新课表】按钮创建课表吧</p></div>');
    }
    function dateRow(){ return '<div class="gh2"><span class="dp">'+NOWTXT+I.cal+'</span><span class="ar">←</span><span class="ar">→</span><span class="wk">第 '+WEEKN+' 周</span></div>'; }
    function gridView(){
      var chips = subj.map(function(s){ return '<span data-sub="'+esc(s.n)+'" title="'+esc(s.n)+'">'+esc(s.a)+'</span>'; }).join('');
      var any = Object.keys(sched).length > 0, sel = any && st.cell && sched[st.cell[0]];
      return toolbar(sel ? [['refresh','刷新','','sync'],'|',['day','周'+days[st.cell[0]],'dim','doc'],['info','详细信息','','info'],['layer','创建临时层','','stack'],['del','删除','','trash']] : [['refresh','刷新','','sync'],'|',['none','未选择课表','dim','']]) +
        '<div class="e2v grid"><div class="gmain">'+dateRow()+
        '<div class="gscroll">'+tableHtml(false)+'</div>'+viewSw('grid', true)+'</div>'+
        '<div class="side2"><div class="tb2"><span class="on">编辑科目</span><span>编辑课程</span></div><div class="chips3">'+chips+'</div>'+
        '<div class="cbx2'+(st.auto?' on':'')+'" data-auto><i>'+I.check+'</i>选完科目自动移动到下一个课程</div></div></div>'+
        (st.pop ? popup() : '');
    }
    var pp = {name:'周一', rule:0, days:[false,false,false,false,false,false,false], target:null, copy:false, range:false};
    var RI = {tag:'<svg viewBox="0 0 16 16"><path d="M2.5 2.5h5.6l5.4 5.4-5.6 5.6-5.4-5.4z M5.5 5.5h.01"/></svg>', week:'<svg viewBox="0 0 16 16"><rect x="2.5" y="3" width="11" height="10.5" rx="2"/><path d="M2.5 6.5h11"/></svg>', day:'<svg viewBox="0 0 16 16"><rect x="2.5" y="2.5" width="11" height="11" rx="2"/><path d="M5.5 6.5h5M5.5 9.5h3"/></svg>', loop:'<svg viewBox="0 0 16 16"><path d="M3 7a4 4 0 0 1 7-2.5L12 6.5M13 9a4 4 0 0 1-7 2.5L4 9.5M12 3.5v3h-3M4 12.5v-3h3"/></svg>'};
    function sel3(t){ return '<div class="sel2"><span>'+t+'</span>'+I.chev+'</div>'; }
    function popup(){
      var rules = [['每周','week'],['某天','day'],['循环','loop']];
      return '<div class="nfly" data-fly><div class="pop2"><h4>新建课表</h4><label>时间表</label>'+sel3('新时间表')+'<label>名称</label><input class="in2" data-pn value="'+esc(pp.name)+'">'+
        '<div class="cbx2'+(pp.copy?' on':'')+'" data-pcopy style="margin:12px 0 4px"><i>'+I.check+'</i>复制自</div><hr>'+
        '<div class="sh2">'+RI.tag+'触发规则</div><p class="hint2">课表只有在规则全部满足时才会生效。</p>'+
        '<div class="seg3">'+rules.map(function(x,i){return '<span class="'+(pp.rule===i?'on':'')+'" data-rule="'+i+'">'+RI[x[1]]+x[0]+'</span>';}).join('')+'</div>'+
        (pp.rule===0 ? '<div class="evr"><span>每</span><div class="sel2 sm">两周'+I.chev+'</div><span>的</span><div class="sel2 sm">每周启用'+I.chev+'</div></div>' : '')+
        '<label>当今天是:</label><div class="pills">'+days.map(function(d,i){return '<span class="'+(pp.days[i]?'on':'')+'" data-pd="'+i+'">'+d+'</span>';}).join('')+'</div>'+
        '<div class="cbx2'+(pp.range?' on':'')+'" data-prange style="margin:14px 0 4px"><i>'+I.check+'</i>并且今天处于以下日期范围</div>'+
        '<label>排除以下日期</label>'+sel3('选择日期')+'<label>附加以下日期</label>'+sel3('选择日期')+'<hr>'+
        '<div class="b2 acc cr" data-pok>'+I.check+'创建</div></div></div>';
    }
    function tlView(){
      var H = (T1-T0)*PX, lines='';
      for (var m=T0;m<=T1;m+=15){ var mj = m%30===0; lines += '<div class="hl'+(mj?'':' mn')+'" style="top:'+(m-T0)*PX+'px">'+(mj?'<span>'+hm(m)+'</span>':'')+'</div>'; }
      var bl = blocks.map(function(b,i){
        var sel = i===st.tl, d=b.e-b.s;
        return '<div class="tb3 '+b.k+(sel?' sel':'')+'" data-i="'+i+'" style="top:'+(b.s-T0)*PX+'px;height:'+d*PX+'px">'+
          (b.k==='k' ? '<div class="l1">'+I.book+'<span>'+hm(b.s)+':00 - '+hm(b.e)+':00</span></div><div class="l2">'+I.hist+'<span>'+dur(d)+'</span></div>' : '<div class="l1">'+I.clock+'<span>'+hm(b.s)+':00 - '+hm(b.e)+':00</span></div>')+
          (sel?'<span class="del" data-a="del">'+I.trash+'</span><i class="hd t" data-h="s"></i><i class="hd b" data-h="e"></i>':'')+'</div>'; }).join('');
      var tlOn = blocks.length>0; var b = blocks[st.tl] || blocks[0];
      if (!tlOn) b = {s:480,e:520,k:'k'};
      var bar = (b && blocks.length) ? '<div class="addbar" style="top:'+((b.e-T0)*PX+16)+'px"><span class="ab0">'+I.chev+'添加</span><span class="ab" data-a="addk">'+I.book+'上课</span><span class="ab" data-a="addb">'+I.clock+'课间</span><span class="ab x">'+I.x+'</span></div>' : '';
      function tri(w,v){ return '<div class="tri">'+['h','m','s'].map(function(k,j){ var n=[Math.floor(v/60),('0'+v%60).slice(-2),'00'][j]; return '<input data-tp="'+w+k+'" value="'+n+'" inputmode="numeric">'; }).join('')+'</div>'; }
      return '<div class="e2tool">'+[['addk','上课','book'],['addb','课间','clock'],['sep','分割线','split'],['act','行动','bolt'],'|',['dup','创建副本','copy'],['undo','','undo'],['redo','','redo'],'|',['del','删除','minus'],['refresh','刷新','sync'],'|',['info','时间表信息','info'],'|',['more','','dots']].map(function(x){ return x==='|'?'<b></b>':'<span class="'+(x[0]==='undo'&&!st.hist.length||x[0]==='redo'&&!st.redo.length?'dim':'')+'" data-a="'+x[0]+'">'+I[x[2]]+(x[1]?'<em>'+x[1]+'</em>':'')+'</span>'; }).join('')+'</div>'+
        '<div class="e2v tlv"><div class="llist"><div class="ltool"><span data-a="tladd">'+I.plus+'<em>添加</em></span><span class="'+(tlOn?'':'dim')+'">'+I.copy+'<em>复制</em></span></div>'+(tlOn?'<div class="li2 on">新时间表</div>':'')+'<div class="lbot"><span>时间点时长</span>'+I.up+'</div></div>'+
        '<div class="cvw"><div class="cvs">'+(tlOn?'<div class="cvin" style="height:'+(H+20)+'px">'+lines+bl+bar+'</div>':'<div class="emp2 big"><svg viewBox="0 0 48 48"><rect x="6" y="6" width="36" height="36" rx="9" stroke-dasharray="9 7"/></svg><p>啥都没有</p></div>')+'</div>'+
        '<div class="zbar"><span class="zi">'+I.list+'</span><span class="zi">'+I.cal2+'</span><span class="sp"></span><span class="zb on">'+I.fit+'</span><span class="zi" data-z="-1">'+I.zout+'</span><em>'+Math.round(PX/0.006)+'%</em><span class="zi" data-z="1">'+I.zin+'</span><span class="zi">'+I.loc+'</span></div></div>'+
        (st.tinfo ? tinfoPanel() : !tlOn ? '<div class="side2 sd3"></div>' : '')+'<div class="side2 sd3"'+(st.tinfo||!tlOn?' hidden':'')+'><h5>编辑时间点</h5><label>开始时间</label>'+tri('s',b.s)+'<label>结束时间</label>'+tri('e',b.e)+
        '<label>类型</label><div class="pl2"><span class="'+(b.k==='k'?'on':'')+'" data-ty="k">'+I.book+'上课</span><span class="'+(b.k==='b'?'on':'')+'" data-ty="b">'+I.clock+'课间休息</span></div>'+
        (b.k==='k' ? '<div class="cbx2'+(b.hide?' on':'')+'" data-hide><i>'+I.check+'</i>默认隐藏</div><p class="hint">若默认隐藏一个时间点，那么只有在处于此时间点时，此时间点才会显示。</p><hr><div class="sh">'+I.book+'默认课程</div><div class="selw"><select class="in2" data-def><option value=""></option>'+subj.map(function(s){return '<option'+(b.def===s.n?' selected':'')+'>'+esc(s.n)+'</option>';}).join('')+'</select></div><div class="ov">'+I.up+'覆盖现有课程</div>'
                    : '<label>课间名称</label><input class="in2" data-bn value="'+esc(b.name||'')+'">')+
        '<hr><div class="sh">'+I.gear+'更多选项</div>'+
        [['上课提醒设置','layers',0],['课程显示设置','book',0],['天气提醒设置','cloud',1]].map(function(x){ return '<div class="mo2">'+I[x[1]]+'<span>'+x[0]+'</span>'+(x[2]?'':'<i class="lay">'+I.layers+'</i>')+'<span class="tg"><i></i><span>关</span></span><em>'+I.chev+'</em></div>'; }).join('')+'</div></div>';
    }
    function tinfoPanel(){
      return '<div class="side2 sd3 tinfo"><h5>时间表信息</h5><label>名称</label><input class="in2" value="新时间表"><hr><div class="sh">'+I.gear+'更多选项</div>'+
        [['放学提醒设置'],['上课提醒设置'],['课程显示设置']].map(function(x){ return '<div class="mo2">'+I.layers+'<span>'+x[0]+'</span><i class="lay">'+I.layers+'</i><span class="tg"><i></i><span>关</span></span>'+I.chev+'</div>'; }).join('')+'</div>';
    }
    function dur(d){ return ('0'+Math.floor(d/60)).slice(-2)+':'+('0'+d%60).slice(-2)+':00'; }
    var SJI = ['doc','book','cal','clock','bolt','cloud','shield','layers','gear','hist','split','list'];
    function sjView(){
      var grip = '<svg viewBox="0 0 24 24" class="grip"><path d="M9 6h.01M15 6h.01M9 12h.01M15 12h.01M9 18h.01M15 18h.01" stroke-width="3"/></svg>';
      var rows = subj.map(function(s,i){ return '<div class="sjr'+(i===st.sj?' on':'')+'" data-si="'+i+'"><span>'+grip+'</span><span class="ico">'+I[SJI[i%SJI.length]]+'</span><span><i class="sw3" style="background:'+s.c+'"></i></span><span>'+esc(s.n)+'</span><span>'+esc(s.a)+'</span><span><i class="cb3'+(s.o?' on':'')+'" data-so="'+i+'">'+(s.o?I.check:'')+'</i></span><span class="tc">'+esc(s.t||'')+'</span><span class="tc pl">'+esc(s.p||'')+'</span></div>'; }).join('');
      var c = subj[st.sj] || subj[0];
      function ex(t,ico,open,inner){ return '<div class="exq'+(open?' open':'')+'"><div class="exh" data-ex>'+I[ico]+'<b>'+t+'</b><i class="lay">'+I.layers+'</i><span class="tg"><i></i><span>关</span></span><em>'+I.up+'</em></div>'+(open?'<div class="exb">'+inner+'</div>':'')+'</div>'; }
      var rem = '<div class="mini"><span class="on">准备上课</span><span>上课</span><span>显示</span></div><div class="cbx2 on dimc"><i>'+I.check+'</i>启用准备上课提醒。</div><label>准备上课提醒时间</label><div class="numq"><span>60</span><i>'+I.up+'</i></div><label>准备上课遮罩文字</label><input class="in2" placeholder="即将上课" disabled><label>准备上课提醒文字</label><input class="in2" placeholder="准备上课，请回到座位并保持安静，做好上课准备。" disabled>';
      var dsp = '<div class="cbx2 on dimc"><i>'+I.check+'</i>显示时间点附加信息</div><label>要显示的附加信息</label><div class="cbo"><span>时间点持续时间</span>'+I.chev+'</div><label>显示精确倒计时时长</label><div class="numq"><span>0</span><i>'+I.up+'</i></div><div class="cbx2 dimc"><i></i>使用模糊倒计时</div><div class="cbx2 dimc"><i></i>上课时仅显示当前课程</div>';
      return '<div class="e2tool"><span data-a="addsj">'+I.plus+'<em>添加</em></span><b></b><span data-a="dupsj">'+I.copy+'<em>复制</em></span><span data-a="delsj">'+I.trash+'<em>删除</em></span></div>'+
        '<div class="e2v sjv"><div class="sjl"><div class="sjr h"><span></span><span>图标</span><span>主题</span><span>科目名</span><span>简称</span><span>户外课程?</span><span>科任老师</span><span>地点</span></div>'+rows+'</div>'+
        '<div class="side2 sd4"><h5>编辑科目信息</h5><div class="r4"><div><label>图标</label><div class="cbo ic">'+I[SJI[st.sj%SJI.length]]+I.chev+'</div></div><div><label>科目名</label><input class="in2" data-sn value="'+esc(c.n)+'"></div><div><label>简称</label><input class="in2" data-sa maxlength="2" value="'+esc(c.a)+'"></div><div><label>主题色</label><div class="cbo clr"><i style="background:'+c.c+'"></i>'+I.chev+'</div></div></div>'+
        '<label>科任老师</label><input class="in2" data-st value="'+esc(c.t||'')+'"><label>地点</label><input class="in2" data-sp value="'+esc(c.p||'')+'">'+
        '<div class="cbx2'+(c.o?' on':'')+'" data-so="'+st.sj+'" style="margin:14px 0"><i>'+I.check+'</i>该科目是户外课程</div><hr><div class="sh">'+I.gear+'更多选项</div>'+ex('上课提醒设置','bolt',st.ex1!==false,rem)+ex('课程显示设置','book',st.ex2!==false,dsp)+'</div></div>';
    }
    function ymd(d){ return d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate()); }
    function calView(){
      var first = new Date(NOW.getFullYear(), NOW.getMonth()+st.cm, 1), off = (first.getDay()+6)%7, start = new Date(first.getFullYear(), first.getMonth(), 1-off), cells = '';
      for (var n=0;n<42;n++){
        var d = new Date(start.getFullYear(), start.getMonth(), start.getDate()+n), k = ymd(d), wd = d.getDay(), tp = st.temp[k] || [], isT = k===ymd(NOW);
        cells += '<div class="cc'+(isT?' today':'')+'"><span class="cl">'+(sched[wd]?'周'+days[wd]:'')+'</span><span class="cn"><i>'+d.getDate()+'</i></span>'+
          '<span class="ci'+(tp.length?' on':'')+'" data-ci="'+k+'" data-tip="预定临时课表">'+I.doc+'</span>'+(tp.length?'<span class="ct">'+tp.map(esc).join('、')+'</span>':'')+'</div>';
      }
      var tri = function(d,dir){ return '<span class="mv" data-mv="'+dir+'"><svg viewBox="0 0 10 10"><path d="'+d+'" fill="currentColor" stroke="none"/></svg></span>'; };
      return toolbar([['refresh','刷新','','sync']])+
        '<div class="e2v swv"><div class="swl"></div><div class="swsp"></div><div class="gmain cal"><div class="chd"><b>'+first.getFullYear()+'年'+(first.getMonth()+1)+'月</b><span class="sp"></span>'+tri('M1 7l4-4 4 4z',-1)+tri('M1 3l4 4 4-4z',1)+'</div>'+
        '<div class="wkh">'+['一','二','三','四','五','六','日'].map(function(x){return '<span>'+x+'</span>';}).join('')+'</div><div class="cgrid">'+cells+'</div>'+viewSw('cal', false)+'</div></div>'+
        (st.tpop ? tpopHtml() : '');
    }
    function tpopHtml(){
      var names = Object.keys(sched).map(function(i){ return '周'+days[i]; }), cur = st.temp[st.tpop.k] || [];
      return '<div class="tpop" style="left:'+st.tpop.x+'px;top:'+st.tpop.y+'px"><div class="th1"><b>选择要临时启用的课表</b><span data-tx>'+I.x+'</span></div>'+
        (names.length ? names.map(function(n){ var on = st.tpop.sel.indexOf(n)>=0; return '<div class="tr1'+(on?' on':'')+'" data-tpick="'+esc(n)+'"><i class="cb3'+(on?' on':'')+'">'+(on?I.check:'')+'</i>'+esc(n)+'</div>'; }).join('') : '<p class="hint2">还没有可选的课表。</p>')+
        '<div class="tact"><span data-tok>'+I.check+'确定</span><span data-tclr><svg viewBox="0 0 24 24"><path d="M9 6h11v12H9l-6-6z"/><path d="M12 10l4 4M16 10l-4 4"/></svg>清除</span></div></div>';
    }
    function swView(){
      if (st.sv === 'cal') return calView();
      return toolbar([['refresh','刷新','','sync'],'|',['modify','修改课程','','edit'],['swapc','交换课程','','swap']])+
        '<div class="e2v swv"><div class="swl"></div><div class="swsp"></div><div class="gmain">'+dateRow()+'<div class="gscroll">'+tableHtml(true)+'</div>'+viewSw('grid', false)+'</div></div>'+
        (st.swd ? '<div class="swov" data-swov><div class="sw2 w" data-app="swap" data-modal="1"></div></div>' : '');
    }
    function render(keep){
      var y = keep && body.querySelector('.cvs') ? body.querySelector('.cvs').scrollTop : 0;
      body.innerHTML = st.v==='grid' ? gridView() : st.v==='tl' ? tlView() : st.v==='sj' ? sjView() : swView();
      if (st.v==='sw' && st.swd) initSwap(body.querySelector('[data-app="swap"]'));
      var cur2 = root.querySelector('.e2act span:nth-child(2)'); if (cur2) { var cs = sched[TODAY] ? '周'+days[TODAY] : '（无）'; cur2.lastChild.textContent = cs; }
      var cv = body.querySelector('.cvs'); if (cv) cv.scrollTop = keep ? y : (7*60+20-T0)*PX;
    }
    root.querySelectorAll('.e2tabs > span').forEach(function(sp){ sp.addEventListener('click', function(){
      root.querySelectorAll('.e2tabs > span').forEach(function(x){x.classList.toggle('on',x===sp)}); st.v = sp.dataset.v; st.pop=false; render(); }); });

    var anchor = 0, atop = 140;
    function place(th){
      var f = body.querySelector('[data-fly]'); if(!f) return;
      if (th){ var nbEl = body.querySelector('.nb[data-new="'+pp.target+'"]'); var tb = (nbEl||body).getBoundingClientRect(), bb = body.getBoundingClientRect(); anchor = tb.left - bb.left - 6; atop = tb.bottom - bb.top + 4; }
      var bw = body.clientWidth, bh = body.clientHeight, pop = f.firstChild, w = pop.offsetWidth;
      pop.style.maxHeight = Math.max(160, bh - 12) + 'px';
      var ph = Math.min(pop.offsetHeight, bh - 12);
      f.style.left = Math.max(8, Math.min(anchor, bw - w - 8))+'px'; f.style.top = Math.max(6, Math.min(atop, bh - ph - 6))+'px';
    }
    function cur(){ return blocks[st.tl]; }
    body.addEventListener('click', function(e){
      var t = e.target, el;
      if ((el=t.closest('[data-a]'))){ var a = el.dataset.a, b = cur();
        if (a==='addk'||a==='addb'){ snap(); var s = b? b.e : 8*60, k = a==='addk'?'k':'b', d = k==='k'?40:10; if (s+d>T1) return; var nb={s:s,e:s+d,k:k}; blocks.splice(st.tl+1,0,nb);
          var sh = 0; for (var q=st.tl+2;q<blocks.length;q++){ var o=blocks[q]; if (o.s < blocks[q-1].e) { sh = blocks[q-1].e - o.s; o.s+=sh; o.e+=sh; } } st.tl++; render(true); }
        else if (a==='info' && st.v==='tl'){ st.tinfo=!st.tinfo; render(true); }
        else if (a==='tladd'){ if(!blocks.length){ snap(); blocks.push({s:480,e:520,k:'k'}); st.tl=0; } st.tinfo=false; render(); }
        else if (a==='swapc'){ st.swd=true; render(true); }
        else if (a==='sep'||a==='act'||a==='info'||a==='more'||a==='modify'){ }
        else if (a==='dup' && b){ snap(); var n = {s:b.e,e:b.e+(b.e-b.s),k:b.k}; if (n.e>T1) return; blocks.splice(st.tl+1,0,n); st.tl++; render(true); }
        else if (a==='del' && st.v==='tl' && b){ snap(); blocks.splice(st.tl,1); st.tl=Math.max(0,st.tl-1); render(true); }
        else if (a==='undo' && st.hist.length){ st.redo.push(JSON.stringify(blocks)); blocks = JSON.parse(st.hist.pop()); st.tl=Math.min(st.tl,blocks.length-1); render(true); }
        else if (a==='redo' && st.redo.length){ st.hist.push(JSON.stringify(blocks)); blocks = JSON.parse(st.redo.pop()); render(true); }
        else if (a==='refresh'){ render(true); }
        else if (a==='del' && st.v==='grid'){ var c=st.cell; if (c && sched[c[0]]){ sched[c[0]][c[1]] = null; render(); } }
        else if (a==='addsj'){ subj.push({n:'新科目',a:'新',c:'#8a8a8a',o:false}); st.sj=subj.length-1; render(); }
        else if (a==='dupsj'){ var q=subj[st.sj]; subj.splice(st.sj+1,0,{n:q.n+'（副本）',a:q.a,c:q.c,o:q.o,t:q.t,p:q.p}); st.sj++; render(true); }
        else if (a==='delsj' && subj.length>1){ subj.splice(st.sj,1); st.sj=0; render(); }
        return; }
      if ((el=t.closest('[data-sv]'))){ st.sv=el.dataset.sv; st.tpop=null; render(); return; }
      if ((el=t.closest('[data-mv]'))){ st.cm += +el.dataset.mv; st.tpop=null; render(); return; }
      if ((el=t.closest('[data-ci]'))){ var br=el.getBoundingClientRect(), bb2=body.getBoundingClientRect(), k=el.dataset.ci; var px=Math.max(8,Math.min(br.left-bb2.left-10, body.clientWidth-350)), py=Math.max(8,Math.min(br.bottom-bb2.top+8, body.clientHeight-230));
        st.tpop={k:k,x:px,y:py,sel:(st.temp[k]||[]).slice()}; render(true); return; }
      if (st.tpop){
        if ((el=t.closest('[data-tpick]'))){ var nm=el.dataset.tpick, ix=st.tpop.sel.indexOf(nm); if(ix>=0) st.tpop.sel.splice(ix,1); else st.tpop.sel.push(nm); render(true); return; }
        if (t.closest('[data-tok]')){ if(st.tpop.sel.length) st.temp[st.tpop.k]=st.tpop.sel; else delete st.temp[st.tpop.k]; st.tpop=null; render(true); return; }
        if (t.closest('[data-tclr]')){ delete st.temp[st.tpop.k]; st.tpop=null; render(true); return; }
        if (t.closest('[data-tx]') || !t.closest('.tpop')){ st.tpop=null; render(true); return; }
      }
      if (st.swd && t.matches('[data-swov]')){ st.swd=false; render(true); return; }
      if ((el=t.closest('.tb3')) && !t.closest('.hd')){ st.tinfo=false; st.tl=+el.dataset.i; render(true); return; }
      if ((el=t.closest('[data-ty]'))){ var b2=cur(); snap(); b2.k=el.dataset.ty; render(true); return; }
      if ((el=t.closest('[data-hide]'))){ var b3=cur(); b3.hide=!b3.hide; render(true); return; }
      if ((el=t.closest('td.c'))){ st.cell=[+el.dataset.d,+el.dataset.r]; render(); return; }
      if ((el=t.closest('[data-sub]'))){ var c=st.cell; if(!c||!sched[c[0]]) return; sched[c[0]][c[1]] = el.dataset.sub; var n=classes().length;
        if (st.auto) st.cell=[c[0], Math.min(n-1,c[1]+1)]; render(); return; }
      if ((el=t.closest('[data-z]'))){ var z=Math.round(PX/0.006)+(+el.dataset.z)*50; z=Math.max(100,Math.min(500,z)); PX=z*0.006; render(true); return; }
      if (t.closest('[data-auto]')){ st.auto=!st.auto; render(); return; }
      if ((el=t.closest('[data-new]'))){ pp.target=+el.dataset.new; pp.name='周'+days[pp.target]; pp.copy=false; pp.range=false; pp.days=days.map(function(x,i){return i===pp.target}); st.pop=true; render(); place(true); return; }
      if ((el=t.closest('[data-rule]'))){ pp.rule=+el.dataset.rule; render(); place(); return; }
      if ((el=t.closest('[data-pd]'))){ var i=+el.dataset.pd; pp.days[i]=!pp.days[i]; render(); place(); return; }
      if (t.closest('[data-pcopy]')){ pp.copy=!pp.copy; render(); place(); return; }
      if (t.closest('[data-prange]')){ pp.range=!pp.range; render(); place(); return; }
      if (st.pop && !t.closest('[data-fly]')){ st.pop=false; render(); return; }
      if (t.closest('[data-pok]')){ pp.days.forEach(function(on,i){ if(on && !sched[i]) sched[i]=classes().map(function(){return null}); }); st.pop=false; st.cell=[pp.target,0]; render(); return; }
      if ((el=t.closest('[data-so]'))){ var s=subj[+el.dataset.so]; s.o=!s.o; render(true); return; }
      if ((el=t.closest('[data-ex]'))){ var ee=el.parentNode; var k=ee.querySelector('b').textContent==='上课提醒设置'?'ex1':'ex2'; if(!t.closest('.tg')){ st[k]=!(st[k]!==false); render(true);} return; }
      if ((el=t.closest('.sjr[data-si]'))){ st.sj=+el.dataset.si; render(); return; }
      if ((el=t.closest('.tg'))){ el.classList.toggle('on'); el.lastChild.textContent = el.classList.contains('on')?'开':'关'; return; }
    });
    body.addEventListener('swclose', function(){ st.swd=false; render(true); });
    function clampBlock(){ blocks.sort(function(a,b){return a.s-b.s}); }
    body.addEventListener('input', function(e){
      var t=e.target, b=cur();
      if (t.matches('[data-tp]')){ var w=t.dataset.tp.charAt(0), tri=t.parentNode, hh=+tri.children[0].value||0, mm=+tri.children[1].value||0, v=hh*60+mm;
        if (w==='s'){ if(v<b.e-4 && v>=T0) b.s=v; } else if (v>b.s+4 && v<=T1) b.e=v; return; }
      if (t.matches('[data-sn]')) { var o=subj[st.sj].n; subj[st.sj].n=t.value; Object.keys(sched).forEach(function(k){ sched[k]=sched[k].map(function(x){return x===o?t.value:x}); }); var row=body.querySelector('.sjr.on'); if(row) row.children[3].textContent=t.value; return; }
      if (t.matches('[data-sa]')) { subj[st.sj].a=t.value; var r=body.querySelector('.sjr.on'); if(r) r.children[4].textContent=t.value; return; }
      if (t.matches('[data-st]')){ subj[st.sj].t=t.value; var r2=body.querySelector('.sjr.on'); if(r2) r2.children[6].textContent=t.value; return; }
      if (t.matches('[data-sp]')){ subj[st.sj].p=t.value; var r3=body.querySelector('.sjr.on'); if(r3) r3.children[7].textContent=t.value; return; }
      if (t.matches('[data-pn]')) pp.name=t.value;
      if (t.matches('[data-bn]')) b.name=t.value;
    });
    body.addEventListener('change', function(e){ var t=e.target; if (t.matches('[data-def]')) cur().def=t.value; if (t.matches('[data-tp]')) render(true); });
    function redrawBlocks(){ var y=body.querySelector('.cvs').scrollTop; var side=body.querySelector('[data-ts]'); var fs=document.activeElement; render(true); var again = fs && fs.matches && fs.matches('[data-ts],[data-te]') ? body.querySelector(fs.matches('[data-ts]')?'[data-ts]':'[data-te]') : null; if(again) again.focus(); }
    var drag=null;
    body.addEventListener('pointerdown', function(e){
      var h=e.target.closest('.hd'); if(!h) return; e.preventDefault(); h.setPointerCapture(e.pointerId);
      snap(); drag={edge:h.dataset.h, y:e.clientY, i:st.tl, s0:blocks[st.tl].s, e0:blocks[st.tl].e, el:h};
    });
    body.addEventListener('pointermove', function(e){
      if(!drag) return; var b=blocks[drag.i], dm=Math.round((e.clientY-drag.y)/PX/5)*5, MIN=5;
      var prev=blocks[drag.i-1], next=blocks[drag.i+1];
      if (drag.edge==='s'){ var v=drag.s0+dm, lo=T0, hi=b.e-MIN;
        if (prev && prev.e===drag.s0){ lo=prev.s+MIN; } else if (prev){ lo=prev.e; }
        v=Math.max(lo,Math.min(hi,v)); b.s=v; if (prev && prev.e===drag.s0) prev.e=v;
      } else { var v2=drag.e0+dm, lo2=b.s+MIN, hi2=T1;
        if (next && next.s===drag.e0){ hi2=next.e-MIN; } else if (next){ hi2=next.s; }
        v2=Math.max(lo2,Math.min(hi2,v2)); b.e=v2; if (next && next.s===drag.e0) next.s=v2; }
      var cv=body.querySelector('.cvin'); blocks.forEach(function(x,i){ var el=cv.querySelector('.tb3[data-i="'+i+'"]'); if(!el) return; el.style.top=(x.s-T0)*PX+'px'; el.style.height=(x.e-x.s)*PX+'px';
        var sp=el.children; if(x.k==='k'){ sp[0].lastChild.textContent=hm(x.s)+':00 - '+hm(x.e)+':00'; sp[1].lastChild.textContent=dur(x.e-x.s); } else sp[0].lastChild.textContent=hm(x.s)+':00 - '+hm(x.e)+':00'; var bar=cv.querySelector('.addbar'); if(bar) bar.style.top=((blocks[drag.i].e-T0)*PX+16)+'px'; });
      var tp=body.querySelectorAll('[data-tp]'); if(tp.length){ tp[0].value=Math.floor(b.s/60); tp[1].value=('0'+b.s%60).slice(-2); tp[3].value=Math.floor(b.e/60); tp[4].value=('0'+b.e%60).slice(-2); }
    });
    function end(){ if(drag){ drag=null; render(true); } }
    body.addEventListener('pointerup', end); body.addEventListener('pointercancel', end);
    root.__reset = function(){ sched={}; st.cell=[TODAY,0]; st.pop=false; st.sv='grid'; st.temp={}; st.tpop=null; st.swd=false; st.v='grid'; root.querySelectorAll('.e2tabs > span').forEach(function(x){x.classList.toggle('on',x.dataset.v==='grid')}); render(); };
    render();
  }
  $$('[data-app="editor"]').forEach(initEditor);
})();
(function(){
  
  document.querySelectorAll('.ctabs').forEach(function(bar){
    var host = document.getElementById(bar.dataset.for); if(!host) return;
    var desc = document.getElementById('cdesc');
    function mark(k){ bar.querySelectorAll('.ct').forEach(function(b){ var on=b.dataset.go===k; b.classList.toggle('on',on); if(on && desc) desc.textContent=b.dataset.d; }); }
    bar.addEventListener('click', function(e){ var b=e.target.closest('.ct'); if(!b) return; var k=b.dataset.go;
      var root=host.querySelector('.sapp'); root.querySelectorAll('.pgx').forEach(function(p){p.classList.toggle('on',p.dataset.p===k)});
      root.querySelectorAll('.nv .it[data-go]').forEach(function(n){n.classList.toggle('on',n.dataset.go===k)}); mark(k); });
    host.addEventListener('click', function(e){ var n=e.target.closest('.nv .it[data-go]'); if(n) mark(n.dataset.go); });
  });
})();

(function () {
  function closeAll(root) { root.querySelectorAll('.fly.open').forEach(function (f) { f.classList.remove('open'); }); }
  document.querySelectorAll('.sapp').forEach(function (root) {
    root.addEventListener('click', function (e) {
      var t = e.target, fk = t.closest('[data-fk]');
      if (fk) {
        var f = root.querySelector('[data-fly="' + fk.dataset.fk + '"]'); if (!f) return;
        var was = f.classList.contains('open'); closeAll(root); if (!was) f.classList.add('open'); return;
      }
      var mi = t.closest('.fly .mi');
      if (mi) {
        var fl = mi.closest('.fly'), k = fl.dataset.fly, name = mi.textContent.trim();
        if (k === 'trig') { root.querySelector('[data-fk="trig"] .v').textContent = name; closeAll(root); return; }
        if (k === 'act' && mi.querySelector('.chev') && /运行/.test(name)) {
          fl.querySelectorAll('.mi').forEach(function (x) { x.classList.toggle('mon', x === mi); });
          root.querySelector('[data-fly="act2"]').classList.add('open'); return;
        }
        var box = root.querySelector('[data-acts]'), add = box.querySelector('[data-fk="act"]'), row = document.createElement('div');
        row.className = 'act-row'; row.innerHTML = mi.querySelector('svg').outerHTML + '<span>' + name + '</span>';
        box.insertBefore(row, add); closeAll(root); return;
      }
      closeAll(root);
    });
  });
})();

(function () {
  document.querySelectorAll('.sapp').forEach(function (root) {
    root.addEventListener('click', function (e) {
      var pt = e.target.closest('.pl-pg .ptabs.sm [data-pt]');
      if (pt) { var pg0 = pt.closest('.pl-pg'); pg0.querySelectorAll('.ptabs.sm [data-pt]').forEach(function (x) { x.classList.toggle('on', x === pt); }); pg0.querySelectorAll('[data-pp]').forEach(function (n) { n.hidden = n.dataset.pp !== pt.dataset.pt; }); return; }
      var r = e.target.closest('.pl-pg .lst .row'); if (!r) return;
      var pg = r.closest('.pl-pg'), name = r.querySelector('.rt b').childNodes[0].textContent.trim(), desc = r.querySelector('.rt > span').textContent;
      pg.querySelectorAll('.lst .row').forEach(function (x) { x.classList.toggle('on', x === r); });
      pg.querySelector('.plr .ph h3').textContent = name;
      var md = pg.querySelector('.md'), full = /UIAccess/.test(name); md.querySelector('h1').textContent = name;
      Array.prototype.forEach.call(md.children, function (n) { if (n.tagName === 'H1') return; if (n.hasAttribute('data-first')) n.textContent = desc; else n.hidden = !full; });
      var t0 = pg.querySelector('.ptabs.sm [data-pt="0"]'); if (t0) t0.click();
    });
  });
})();
