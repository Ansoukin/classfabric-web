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
    chev: '<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>',
    cal: '<svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>',
    sync: '<svg viewBox="0 0 24 24"><path d="M20 11a8 8 0 0 0-14-4M4 4v4h4M4 13a8 8 0 0 0 14 4M20 20v-4h-4"/></svg>',
    info: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/></svg>',
    stack: '<svg viewBox="0 0 24 24"><path d="M12 4l9 5-9 5-9-5zM3 14l9 5 9-5"/></svg>',
    trash: '<svg viewBox="0 0 24 24"><path d="M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13"/></svg>',
    plus: '<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',
    undo: '<svg viewBox="0 0 24 24"><path d="M9 7L4 12l5 5M4 12h10a6 6 0 0 1 0 12"/></svg>',
    clock: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    shield: '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>'
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

  /* ============ 档案编辑（可交互 · 可拖拽时间轴） ============ */
  function initEditor(root){
    var body = root.querySelector('.e2body');
    var PX = 1.7, T0 = 7*60+30, T1 = 14*60+30;
    var subj = [['语文','语','#e5576b'],['数学','数','#5a78d8'],['英语','英','#7e62d3'],['物理','物','#3a9ae2'],['化学','化','#2fb2a1'],['生物','生','#4faf53'],['政治','政','#df4f6d'],['历史','历','#c58b3d'],['地理','地','#8bb347'],['信息技术','信','#2f9cc9'],['体育','体','#f0872e'],['自习','自','#6c7d9d']];
    subj = subj.map(function(x,i){return {n:x[0],a:x[1],c:x[2],o:x[0]==='体育'}});
    var blocks = [], t = 8*60;
    for (var i=0;i<6;i++){ blocks.push({s:t,e:t+40,k:'k'}); t+=40; if(i<5){ blocks.push({s:t,e:t+10,k:'b'}); t+=10; } }
    var days = ['日','一','二','三','四','五','六'], dates = ['10/25','10/26','10/27','10/28','10/29','10/30','10/31'], TODAY = 6;
    var sched = {}; sched[TODAY] = ['语文','数学','英语','物理','化学','生物'];
    sched[1] = ['数学','语文','英语','历史','政治','地理'];
    var st = {v:'grid', cell:[TODAY,1], auto:true, tl:3, sj:0, hist:[], redo:[], pop:false};
    function hm(m){ return ('0'+Math.floor(m/60)).slice(-2)+':'+('0'+m%60).slice(-2); }
    function pm(v){ var a=v.split(':'); return (+a[0])*60+(+a[1]); }
    function classes(){ return blocks.filter(function(b){return b.k==='k'}); }
    function snap(){ st.hist.push(JSON.stringify(blocks)); if(st.hist.length>60) st.hist.shift(); st.redo=[]; }
    function ic(n){ return I[n] || ''; }
    function esc(x){ return String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }

    function toolbar(items){ return '<div class="e2tool">'+items.map(function(x){ return x==='|' ? '<b></b>' : '<span class="'+(x[2]||'')+'" data-a="'+x[0]+'">'+(I[x[3]]||'')+'<em>'+x[1]+'</em></span>'; }).join('')+'</div>'; }

    function gridView(){
      var cl = classes(), th='<th class="t0">时间</th>';
      days.forEach(function(d,i){
        th += '<th class="'+(i===TODAY?'today':'')+'">周'+d+'<small>'+dates[i]+'</small>'+(sched[i]?'':'<span class="nb" data-new="'+i+'">+ 新课表</span>')+'</th>'; });
      var rows='';
      cl.forEach(function(b,r){
        var tr='<td class="t">'+hm(b.s)+'-'+hm(b.e)+'</td>';
        days.forEach(function(d,i){
          var v = sched[i] && sched[i][r];
          tr += sched[i] ? '<td class="c'+(st.cell[0]===i&&st.cell[1]===r?' sel':'')+(v?'':' no')+'" data-d="'+i+'" data-r="'+r+'">'+(v||'（无）')+'</td>' : '<td></td>';
        });
        rows += '<tr>'+tr+'</tr>';
      });
      var chips = subj.map(function(s){ return '<span data-sub="'+esc(s.n)+'" title="'+esc(s.n)+'">'+esc(s.a)+'</span>'; }).join('');
      return toolbar([['refresh','刷新','','sync'],'|',['day','周六','dim','doc'],['info','详细信息','','info'],['layer','创建临时层','','stack'],['del','删除','','trash']]) +
        '<div class="e2v grid"><div class="gmain"><div class="gh2"><span class="dp">2026/10/31'+I.cal+'</span><span class="ar">←</span><span class="ar">→</span><span class="wk">第 9 周</span></div>'+
        '<div class="gscroll"><table class="tt2"><thead><tr>'+th+'</tr></thead><tbody>'+rows+'</tbody></table></div></div>'+
        '<div class="side2"><div class="tb2"><span class="on">编辑科目</span><span>编辑课程</span></div><div class="chips3">'+chips+'</div>'+
        '<div class="cbx2'+(st.auto?' on':'')+'" data-auto>'+'<i>'+I.check+'</i>选完科目自动移动到下一个课程</div></div></div>'+
        (st.pop ? popup() : '');
    }
    var pp = {name:'新课表', rule:0, days:[false,false,false,false,false,false,false], target:null};
    function popup(){
      return '<div class="mask2"><div class="pop2"><h4>新课表</h4><label>时间表</label><div class="sel2"><span>新时间表</span>'+I.chev+'</div>'+
        '<label>名称</label><input class="in2" data-pn value="'+esc(pp.name)+'"><label>触发规则</label><div class="seg2">'+['每周','某天','循环'].map(function(x,i){return '<span class="'+(pp.rule===i?'on':'')+'" data-rule="'+i+'">'+x+'</span>';}).join('')+'</div>'+
        '<label>当今天是</label><div class="pills">'+days.map(function(d,i){return '<span class="'+(pp.days[i]?'on':'')+'" data-pd="'+i+'">'+d+'</span>';}).join('')+'</div>'+
        '<div class="pbar"><span class="b2" data-pcancel>取消</span><span class="b2 acc" data-pok>创建</span></div></div></div>';
    }
    function tlView(){
      var H = (T1-T0)*PX, lines='';
      for (var m=T0;m<=T1;m+=30) lines += '<div class="hl" style="top:'+(m-T0)*PX+'px"><span>'+hm(m)+'</span></div>';
      var bl = blocks.map(function(b,i){
        var sel = i===st.tl, h=(b.e-b.s)*PX;
        return '<div class="tb3 '+b.k+(sel?' sel':'')+'" data-i="'+i+'" style="top:'+(b.s-T0)*PX+'px;height:'+h+'px">'+
          (b.k==='k' ? '<span>'+hm(b.s)+':00 - '+hm(b.e)+':00</span><span class="du">'+('0'+Math.floor((b.e-b.s)/60)).slice(-2)+':'+('0'+(b.e-b.s)%60).slice(-2)+':00</span>' : '<span>'+I.clock+hm(b.s)+':00 - '+hm(b.e)+':00</span>')+
          (sel?'<i class="hd t" data-h="s"></i><i class="hd b" data-h="e"></i>':'')+'</div>'; }).join('');
      var b = blocks[st.tl] || blocks[0];
      return toolbar([['addk','上课','','plus'],['addb','课间','','plus'],['sep','分割线','dim',''],'|',['dup','创建副本','','doc'],['undo','撤销','','undo'],['redo','重做','',''],['del','删除','','trash'],'|',['refresh','刷新','','sync'],['info','时间表信息','','info']]) +
        '<div class="e2v tlv"><div class="llist"><div class="li2 on">新时间表</div></div><div class="cvs"><div class="cvin" style="height:'+(H+20)+'px">'+lines+bl+'</div>'+
        '<div class="addbar"><span>添加</span><span class="b2" data-a="addk">上课</span><span class="b2" data-a="addb">课间</span></div></div>'+
        '<div class="side2"><h5>编辑时间点</h5><label>开始时间</label><input type="time" class="in2" data-ts value="'+hm(b.s)+'"><label>结束时间</label><input type="time" class="in2" data-te value="'+hm(b.e)+'">'+
        '<label>类型</label><div class="seg2"><span class="'+(b.k==='k'?'on':'')+'" data-ty="k">上课</span><span class="'+(b.k==='b'?'on':'')+'" data-ty="b">课间休息</span></div>'+
        '<div class="cbx2'+(b.hide?' on':'')+'" data-hide><i>'+I.check+'</i>默认隐藏</div>'+
        (b.k==='k' ? '<label>默认课程</label><select class="in2" data-def><option value="">（无）</option>'+subj.map(function(s){return '<option'+(b.def===s.n?' selected':'')+'>'+esc(s.n)+'</option>';}).join('')+'</select>' : '<label>课间名称</label><input class="in2" data-bn value="'+esc(b.name||'课间休息')+'">')+
        '<label>更多选项</label><div class="mo">上课提醒设置<span class="tg"><i></i><span>关</span></span></div><div class="mo">课程显示设置<span class="tg"><i></i><span>关</span></span></div></div></div>';
    }
    function sjView(){
      var rows = subj.map(function(s,i){ return '<div class="sr'+(i===st.sj?' on':'')+'" data-si="'+i+'"><span>'+I.doc+'</span><span class="sw3" style="background:'+s.c+'"></span><span>'+esc(s.n)+'</span><span>'+esc(s.a)+'</span><span><i class="cb3'+(s.o?' on':'')+'" data-so="'+i+'">'+(s.o?I.check:'')+'</i></span></div>'; }).join('');
      var c = subj[st.sj] || subj[0];
      return toolbar([['addsj','新建科目','','plus'],['delsj','删除','','trash']]) +
        '<div class="e2v"><div class="sjl"><div class="sr h"><span></span><span>主题</span><span>科目名</span><span>简称</span><span>户外课程?</span></div>'+rows+'</div>'+
        '<div class="side2"><h5>编辑科目信息</h5><label>科目名</label><input class="in2" data-sn value="'+esc(c.n)+'"><label>简称</label><input class="in2" data-sa maxlength="2" value="'+esc(c.a)+'"><label>科任老师</label><input class="in2" placeholder="可选"></div></div>';
    }
    function swView(){ return '<div class="e2v swv"><div class="swwrap"><div class="sw2 w" data-app="swap"></div></div></div>'; }
    function render(keep){
      var y = keep && body.querySelector('.cvs') ? body.querySelector('.cvs').scrollTop : 0;
      body.innerHTML = st.v==='grid' ? gridView() : st.v==='tl' ? tlView() : st.v==='sj' ? sjView() : swView();
      if (st.v==='sw') initSwap(body.querySelector('[data-app="swap"]'));
      var cv = body.querySelector('.cvs'); if (cv) cv.scrollTop = y;
    }
    root.querySelectorAll('.e2tabs > span').forEach(function(sp){ sp.addEventListener('click', function(){
      root.querySelectorAll('.e2tabs > span').forEach(function(x){x.classList.toggle('on',x===sp)}); st.v = sp.dataset.v; st.pop=false; render(); }); });

    function cur(){ return blocks[st.tl]; }
    body.addEventListener('click', function(e){
      var t = e.target, el;
      if ((el=t.closest('[data-a]'))){ var a = el.dataset.a, b = cur();
        if (a==='addk'||a==='addb'){ snap(); var last = blocks[blocks.length-1], s = last? last.e : 8*60, k = a==='addk'?'k':'b', d = k==='k'?40:10; if (s+d>T1) return; blocks.push({s:s,e:s+d,k:k}); st.tl = blocks.length-1; render(true); }
        else if (a==='dup' && b){ snap(); var n = {s:b.e,e:b.e+(b.e-b.s),k:b.k}; if (n.e>T1) return; blocks.splice(st.tl+1,0,n); st.tl++; render(true); }
        else if (a==='del' && st.v==='tl' && b){ snap(); blocks.splice(st.tl,1); st.tl=Math.max(0,st.tl-1); render(true); }
        else if (a==='undo' && st.hist.length){ st.redo.push(JSON.stringify(blocks)); blocks = JSON.parse(st.hist.pop()); st.tl=Math.min(st.tl,blocks.length-1); render(true); }
        else if (a==='redo' && st.redo.length){ st.hist.push(JSON.stringify(blocks)); blocks = JSON.parse(st.redo.pop()); render(true); }
        else if (a==='refresh'){ render(true); }
        else if (a==='del' && st.v==='grid'){ var c=st.cell; if (sched[c[0]]){ sched[c[0]][c[1]] = null; render(); } }
        else if (a==='addsj'){ subj.push({n:'新科目',a:'新',c:'#8a8a8a',o:false}); st.sj=subj.length-1; render(); }
        else if (a==='delsj' && subj.length>1){ subj.splice(st.sj,1); st.sj=0; render(); }
        return; }
      if ((el=t.closest('.tb3')) && !t.closest('.hd')){ st.tl=+el.dataset.i; render(true); return; }
      if ((el=t.closest('[data-ty]'))){ var b2=cur(); snap(); b2.k=el.dataset.ty; render(true); return; }
      if ((el=t.closest('[data-hide]'))){ var b3=cur(); b3.hide=!b3.hide; render(true); return; }
      if ((el=t.closest('td.c'))){ st.cell=[+el.dataset.d,+el.dataset.r]; render(); return; }
      if ((el=t.closest('[data-sub]'))){ var c=st.cell; if(!sched[c[0]]) return; sched[c[0]][c[1]] = el.dataset.sub; var n=classes().length;
        if (st.auto) st.cell=[c[0], Math.min(n-1,c[1]+1)]; render(); return; }
      if (t.closest('[data-auto]')){ st.auto=!st.auto; render(); return; }
      if ((el=t.closest('[data-new]'))){ pp.target=+el.dataset.new; pp.name='新课表'; pp.days=days.map(function(x,i){return i===pp.target}); st.pop=true; render(); return; }
      if ((el=t.closest('[data-rule]'))){ pp.rule=+el.dataset.rule; render(); return; }
      if ((el=t.closest('[data-pd]'))){ var i=+el.dataset.pd; pp.days[i]=!pp.days[i]; render(); return; }
      if (t.closest('[data-pcancel]')){ st.pop=false; render(); return; }
      if (t.closest('[data-pok]')){ pp.days.forEach(function(on,i){ if(on && !sched[i]) sched[i]=classes().map(function(){return null}); }); st.pop=false; st.cell=[pp.target,0]; render(); return; }
      if ((el=t.closest('[data-so]'))){ var s=subj[+el.dataset.so]; s.o=!s.o; render(); return; }
      if ((el=t.closest('.sr[data-si]'))){ st.sj=+el.dataset.si; render(); return; }
      if ((el=t.closest('.tg'))){ el.classList.toggle('on'); el.lastChild.textContent = el.classList.contains('on')?'开':'关'; return; }
    });
    function clampBlock(){ blocks.sort(function(a,b){return a.s-b.s}); }
    body.addEventListener('input', function(e){
      var t=e.target, b=cur();
      if (t.matches('[data-ts],[data-te]') && t.value){ var v=pm(t.value); if (t.matches('[data-ts]')) { if(v<b.e-4 && v>=T0) b.s=v; } else if (v>b.s+4 && v<=T1) b.e=v;
        var cv=body.querySelector('.cvin'); if(cv) { redrawBlocks(); } return; }
      if (t.matches('[data-sn]')) { var o=subj[st.sj].n; subj[st.sj].n=t.value; Object.keys(sched).forEach(function(k){ sched[k]=sched[k].map(function(x){return x===o?t.value:x}); }); var row=body.querySelector('.sr.on'); if(row) row.children[2].textContent=t.value; return; }
      if (t.matches('[data-sa]')) { subj[st.sj].a=t.value; var r=body.querySelector('.sr.on'); if(r) r.children[3].textContent=t.value; return; }
      if (t.matches('[data-pn]')) pp.name=t.value;
      if (t.matches('[data-bn]')) b.name=t.value;
    });
    body.addEventListener('change', function(e){ var t=e.target; if (t.matches('[data-def]')) cur().def=t.value; });
    function redrawBlocks(){ var y=body.querySelector('.cvs').scrollTop; var side=body.querySelector('[data-ts]'); var fs=document.activeElement; render(true); var again = fs && fs.matches && fs.matches('[data-ts],[data-te]') ? body.querySelector(fs.matches('[data-ts]')?'[data-ts]':'[data-te]') : null; if(again) again.focus(); }
    // 拖拽手柄：改变上沿/下沿，相邻块共享边界时同步移动
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
        var sp=el.children; if(x.k==='k'){ sp[0].textContent=hm(x.s)+':00 - '+hm(x.e)+':00'; sp[1].textContent=('0'+Math.floor((x.e-x.s)/60)).slice(-2)+':'+('0'+(x.e-x.s)%60).slice(-2)+':00'; } else sp[0].innerHTML=I.clock+hm(x.s)+':00 - '+hm(x.e)+':00'; });
      var ts=body.querySelector('[data-ts]'), te=body.querySelector('[data-te]'); if(ts){ts.value=hm(b.s);te.value=hm(b.e);}
    });
    function end(){ if(drag){ drag=null; render(true); } }
    body.addEventListener('pointerup', end); body.addEventListener('pointercancel', end);
    render();
  }
  $$('[data-app="editor"]').forEach(initEditor);
})();
