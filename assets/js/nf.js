(function () {
  var d = document;
  function $(s) { return d.querySelector(s); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* 404 诗：每次打开随机一首（逐字打出来），「换一首」不会重复当前这首。颜文字与诗一一对应。 */
  var POEMS = [
    ['(´･ω･`)', ['邮差照着旧地址，敲了三年的门。', '门后换了人，换了漆，换了门牌。', '他每次都问：「请问，是不是——」', '住户每次都说：「不是，进来喝口水。」', '信还在他包里。', '地址早就不存在了，', '水，倒一直是热的。'], 'Sonnet 5.5'],
    ['( ˘ω˘ )', ['老街拆了，路灯没人拆，', '还亮着，照着一块空地。', '夜里有人路过，抬头看灯，', '又低头看看空地，轻声说：', '「原来你一直在这儿等。」', '没有人答话。', '灯，又亮了一点。'], 'Sonnet 5.5'],
    ['(・_・?)', ['图书馆的第 404 号书架', '一直是空的。', '管理员说是特意留的：', '总得有一格，', '让人伸手去拿的时候，', '摸到的是整齐的空气，', '并且知道，这不是你的错。'], 'Sonnet 5.5'],
    ['¯\\_(ツ)_/¯', ['地图上这一格是白的。', '不是没人测量，', '是测量的人写了一行小字：', '「这里的东西走开了。', '如果你正好在这里，', '请原地坐一会儿，', '也许它只是出去买东西了。」'], 'Sonnet 5.5'],
    ['(´･_･`)', ['我捡到一把钥匙，', '刻着一个早就不存在的门牌号。', '我把它挂在窗台上。', '风一来，它就叮当响一下，', '像在回答：', '「我在，我在，', '只是锁不在了。」'], 'Sonnet 5.5'],
    ['(°ー°〃)', ['有人问我：「怎么走到这一页？」', '我说：「往前，右转，再右转，', '会遇到一堵很诚实的墙。」', '他道了谢，真的去了。', '回来时手里捧着一个小小的零：', '「墙上只有这个，送你。」'], 'Sonnet 5.5'],
    ['(T_T)', ['纸条上的网址，', '是别人写给你的。', '字迹被雨洇开了一点，', '你照着它走过来，', '路却已经换了方向。'], 'Haiku 5.5'],
    ['(^_^;)', ['地图折了一个角，', '想着下次还要来。', '后来那条路', '变成了一堵墙，', '墙上画着一扇门。', '我站在门前，没有推。'], 'Haiku 5.5'],
    ['(_ _)', ['你写来的信，', '地址写对了。', '收信的人', '已经搬去了别的城。', '邮局没有退回它，', '只在信封上盖了一个章：', '「查无此址」。'], 'Haiku 5.5'],
    ['(・ω・)', ['这一页写到一半，', '作者去喝了杯咖啡。', '咖啡凉了，页面没有写完。', '你来的时候，', '只看见一行标题，', '和一句：「待补充。」'], 'Haiku 5.5'],
    ['(._.)', ['雪下了一夜，', '盖平了所有的路。', '只剩一串脚印，', '从门口走到门前，', '停住了。', '门没有锁，', '脚印也没有回去。'], 'Haiku 5.5']
  ];
  var box = $('.nf-in'), k = $('#nfk'), pl = $('#nfpl'), sw = $('#nfsw'), cur = parseInt(get('cf_nfp'), 10), timer = 0;
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function other() { var n = Math.floor(Math.random() * POEMS.length); return n === cur ? (n + 1 + Math.floor(Math.random() * (POEMS.length - 1))) % POEMS.length : n; }
  /* 每个字先占好位置（透明），再逐个显示，打字时版面不会跳动；标点处停顿，行尾多停一下 */
  function render(n) {
    clearTimeout(timer); cur = n; set('cf_nfp', String(n));
    var lines = POEMS[n][1], chars = [], ends = {};
    k.textContent = POEMS[n][0]; pl.textContent = ''; box.classList.remove('done'); if ($('.nf-by')) $('.nf-by').textContent = '—— ' + POEMS[n][2];
    pl.setAttribute('aria-label', lines.join(''));
    lines.forEach(function (t) {
      var l = d.createElement('span'); l.className = 'l'; l.setAttribute('aria-hidden', 'true');
      t.split('').forEach(function (ch) { var c = d.createElement('span'); c.className = 'c'; c.textContent = ch; l.appendChild(c); chars.push(c); });
      ends[chars.length - 1] = 1; pl.appendChild(l);
    });
    function finish() { box.classList.add('done'); }
    if (calm) { chars.forEach(function (c) { c.className = 'c on'; }); finish(); return; }
    var i = 0;
    (function step() {
      if (i) chars[i - 1].className = 'c on';
      if (i >= chars.length) { finish(); return; }
      var c = chars[i], ch = c.textContent;
      c.className = 'c on cur';
      var wait = /[，、]/.test(ch) ? 170 : /[。！？；：」]/.test(ch) ? 280 : 55;
      if (ends[i]) wait += 260;
      i++; timer = setTimeout(step, wait);
    })();
  }
  if (box && k && pl) {
    render(other());
    if (sw) { sw.hidden = false; sw.addEventListener('click', function () { render(other()); }); }
  }

  /* 壁纸：Bing 每日壁纸（api.bimg.cc/today，直接返回图片）；任何一步失败都退回站内壁纸池 */
  var bg = $('.nf-bg'), im = bg && bg.querySelector('i'), done = false;
  function show(url) {
    if (done || !im) return; done = true;
    im.style.backgroundImage = url ? 'url("' + url + '")' : 'var(--wp, url(/assets/img/wp/lake.webp))';
    bg.classList.add('on');
  }
  function local() { show(null); }
  function size() {
    var w = innerWidth * (devicePixelRatio || 1);
    if (innerWidth <= 820 && innerHeight > innerWidth * 1.1) return 'w=1080&h=1920';
    return w <= 1400 ? 'w=1366&h=768' : 'w=1920&h=1080';
  }
  var u = 'https://api.bimg.cc/today?' + size() + '&mkt=zh-CN', img = new Image(), t = setTimeout(local, 6000);
  img.onload = function () { clearTimeout(t); show(u); };
  img.onerror = function () { clearTimeout(t); local(); };
  img.src = u;
})();
