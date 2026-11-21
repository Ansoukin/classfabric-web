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
    ['(._.)', ['雪下了一夜，', '盖平了所有的路。', '只剩一串脚印，', '从门口走到门前，', '停住了。', '门没有锁，', '脚印也没有回去。'], 'Haiku 5.5'],
    ['(・∀・)', ['一只气球松开了手，', '一路向上，没有回头。', '云问它：「路过，还是应聘？」', '它想了想，说：「应聘。」', '现在它在天上上班，', '每天负责把天空吹蓝一点。', '你要找的这一页，', '也许被挖去了同一家公司。'], 'Sonnet 5.5'],
    ['(｡•ᴗ•｡)', ['沙发缝里组了个乐队：', '硬币打鼓，圆珠笔弹吉他，', '遥控器当主唱，', '只会一首歌，叫《下一首》。', '他们巡演了三个月，', '观众是一粒花生。', '你要找的那一页，', '大概是被拉去当了贝斯手。'], 'Sonnet 5.5'],
    ['( ´▽` )', ['四和四中间夹着一个零。', '有人说那是个洞。', '零说：「不，我是被抱着的。」', '左边的四点点头，', '右边的四也点点头。', '它们谁也不知道该抱什么，', '就抱着这一个空，', '抱得很认真。'], 'Sonnet 5.5'],
    ['(•ᴗ•)', ['导航仪说：「前方一百米，请掉头。」', '我没有掉头。', '它又说：「已为您重新规划路线。」', '我还是没有。', '它沉默了一会儿，说：', '「那我们就一起迷路吧。」', '这一页，', '就是那个拐角。'], 'Sonnet 5.5'],
    ['(°▽°)', ['橡皮最爱干净。', '它擦掉错别字，擦掉算错的数，', '擦掉一只画坏的猫，', '擦着擦着，整页都成了白。', '它很得意，', '没发现自己只剩一粒渣。', '你来的这一页，', '是它最勤奋的作品。'], 'Sonnet 5.5'],
    ['(・ω・´)', ['楼梯少了一级台阶，', '你的脚照旧抬了起来。', '它踩到一小团整齐的空，', '悬了一秒，才明白。', '脚没有错，它只是太信任', '这栋楼昨天的样子。', '新的那一级搬去了别处，', '你再迈一步，它就在。'], 'Sonnet 5.5'],
    ['(｡･ω･｡)', ['我是书签，夹在第四百零四页，', '一夹就是很多年，一动没动。', '后来书被重新装订，页码洗了牌，', '我还站在原来的位置。', '你顺着我走来，我没有骗你，', '只是那一页，被挪去了别处。', '书还在，故事也还在，', '我替你记着，最初是从哪里翻开的。'], 'Sonnet 5.5'],
    ['(ᵔᴥᵔ)', ['你朝山谷喊了一个名字。', '山谷想了想，没有找到。', '它不愿意让你白喊，', '就把你的声音原样送了回来，', '又在最后多添了一声：', '「没有，没有，没有——」', '听上去像在唱歌。', '你笑了，它也松了口气。'], 'Sonnet 5.5'],
    ['(＾▽＾)', ['有人在没有鱼的河边坐了一下午。', '旁边的老人说：「这条河去年就改道了。」', '他问：「那您怎么还坐在这儿？」', '老人说：「习惯。再说，', '总得有人告诉来的人一声。」', '他于是也坐了一会儿，', '没有钓到鱼，', '钓到了一个很长的傍晚。'], 'Sonnet 5.5'],
    ['( ˙▽˙ )', ['镇上最后一家钥匙铺关了门。', '第二天，仍有人来配钥匙。', '他们推门，门是锁着的，', '就站在门口，互相问：', '「你也是来配钥匙的吗？」', '一群没有钥匙的人，聊了一下午。', '天黑时，一把钥匙也没配出来，', '三对邻居认识了彼此。'], 'Fable 5.2'],
    ['(´-ω-`)', ['渡口的船夫搬去了城里。', '渡口还在，河也还在。', '每天仍有人走到岸边，', '朝对岸挥手，', '对岸也有人朝这边挥手。', '谁也过不去，', '谁也没觉得白来。'], 'Fable 5.2'],
    ['(・ー・)', ['【机场广播】各位旅客请注意：', '前往「您要找的那一页」的航班', '已于今日取消。', '原因：目的地暂时不存在。', '地勤人员已在首页柜台备好热茶，', '欢迎前往。', '本次不收退票费。'], 'Opus 5.5'],
    ['(｀・ω・´)', ['【今日天气预报】', '您要找的页面：全天无云，无风，无页面。', '能见度极佳，一眼就能看出它不在这里。', '明日可能有新页面出现，概率：未知。', '出门请带好耐心，', '不必带伞。'], 'Opus 5.5'],
    ['( ´∀｀)', ['旧路口的那棵树', '替走远的路牌', '站了一整个秋天。'], 'Haiku 5.5'],
    ['(・_・)', ['网址有点旧，', '风把它吹去了别处，', '花还开在原地。'], 'Haiku 5.5'],
    ['(´ー｀)', ['你来找一页，', '只遇见一条小溪，', '水替它答了话。'], 'Haiku 5.5']
  ];
  var box = $('.nf-in'), k = $('#nfk'), pl = $('#nfpl'), sw = $('#nfsw'), cur = parseInt(get('cf_nfp'), 10), timer = 0;
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function other() { var n = Math.floor(Math.random() * POEMS.length); return n === cur ? (n + 1 + Math.floor(Math.random() * (POEMS.length - 1))) % POEMS.length : n; }
  /* 每个字先占好位置（透明），再逐个显示，打字时版面不会跳动；标点处停顿，行尾多停一下 */
  function render(n) {
    clearTimeout(timer); cur = n; set('cf_nfp', String(n));
    var lines = POEMS[n][1], chars = [], ends = {};
    k.textContent = POEMS[n][0]; pl.textContent = '';
    /* 署名：先无过渡地隐去，再换字；等诗打完（.done）才淡入，换一首时不会抢在打字机之前出现 */
    box.classList.add('rst'); box.classList.remove('done');
    if ($('.nf-by')) $('.nf-by').textContent = '—— ' + POEMS[n][2];
    void box.offsetWidth; box.classList.remove('rst');
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
  /* 署名：接口 /all?limit=1 返回当天条目的 title / copyright(含摄影师或机构) / copyrightlink；字段名不确定，所以递归找第一个带这些字段的对象。只用 textContent，链接只接受 bing.com 的 https 地址；任何失败都不显示 */
  function pick(o, n) {
    if (!o || typeof o !== 'object' || (n || 0) > 4) return null;
    if (typeof o.copyright === 'string' || typeof o.title === 'string') return o;
    var v = Array.isArray(o) ? o : Object.keys(o).map(function (k) { return o[k]; });
    for (var i = 0; i < v.length; i++) { var r = pick(v[i], (n || 0) + 1); if (r) return r; }
    return null;
  }
  function credit() {
    var cr = $('#nfcr'); if (!cr || !window.fetch) return;
    fetch('https://api.bimg.cc/all?limit=1&mkt=zh-CN&' + size(), { mode: 'cors' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      var o = pick(j); if (!o) return;
      var c = String(o.copyright || '').trim(), ti = String(o.title || '').trim(), text = c;
      if (ti && c.indexOf(ti) < 0) text = c ? ti + ' · ' + c : ti;
      if (!text) return;
      cr.textContent = 'Bing 每日壁纸 · ';
      var link = String(o.copyrightlink || o.copyright_link || '');
      if (/^https:\/\/([a-z0-9-]+\.)?bing\.com\//i.test(link)) { var a = d.createElement('a'); a.href = link; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = text; cr.appendChild(a); }
      else cr.appendChild(d.createTextNode(text));
      cr.hidden = false;
    }).catch(function () {});
  }
  var u = 'https://api.bimg.cc/today?' + size() + '&mkt=zh-CN', img = new Image(), t = setTimeout(local, 6000);
  img.onload = function () { clearTimeout(t); show(u); credit(); };
  img.onerror = function () { clearTimeout(t); local(); };
  img.src = u;
})();
