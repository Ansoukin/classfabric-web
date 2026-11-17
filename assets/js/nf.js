(function () {
  var d = document;
  function $(s) { return d.querySelector(s); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* 请求的地址 */
  var path = $('#nfp');
  if (path) path.textContent = (location.pathname + location.search).slice(0, 96);

  /* 404 诗：每次打开随机一首，不连续重复。颜文字与诗一一对应。 */
  var POEMS = [
    ['¯\\_(ツ)_/¯', '路牌', ['路牌还立在原处，', '路却被谁悄悄收走了。', '你来得没有错，', '只是这里，今天什么也没有。']],
    ['(´･ω･`)', '回声', ['我朝这个地址喊了一声，', '没有人应，只有回声说：', '「找不到。」', '它说得那样轻，像怕吵醒什么。']],
    ['(・_・;)', '空房间', ['门是开着的，', '灯也曾亮过。', '主人搬走时忘了留话，', '这一页，去了别处。']],
    ['(°ー°〃)', '四零四', ['四，像一扇半掩的门；', '零，是门后那片空；', '四，又是一扇门。', '你推开的，全是风。']],
    ['( ˘ω˘ )', '蒲公英', ['有些链接像蒲公英，', '被一阵风吹散了。', '你捡起其中一朵，', '它说：我也不知道落在了哪里。']],
    ['(；′⌒`)', '迷路', ['地图上没有这个点，', '指南针转了半圈又停下。', '迷路并不可耻，', '来时的路，还在身后。']],
    ['(´･_･`)', '缓存', ['也许它存在过，', '在某个下午，某次点击里。', '现在只剩你记得的这个地址，', '和一个很礼貌的 404。']]
  ];
  var last = parseInt(get('cf_nfp'), 10), n = Math.floor(Math.random() * POEMS.length);
  if (n === last) n = (n + 1 + Math.floor(Math.random() * (POEMS.length - 1))) % POEMS.length;
  set('cf_nfp', String(n));
  var P = POEMS[n], k = $('#nfk'), fig = $('#nfpoem');
  if (k) k.textContent = P[0];
  if (fig) {
    var pt = fig.querySelector('.nf-pt'), pl = fig.querySelector('.nf-pl');
    pt.textContent = '《' + P[1] + '》';
    pl.textContent = '';
    P[2].forEach(function (t) { var s = d.createElement('span'); s.textContent = t; pl.appendChild(s); });
  }

  /* 壁纸：Bing 每日壁纸（经 bing.biturl.top 取得当天地址与版权信息）；任何一步失败都退回站内壁纸池 */
  var bg = $('.nf-bg'), im = bg && bg.querySelector('i'), done = false;
  function show(url) {
    if (done || !im) return; done = true;
    im.style.backgroundImage = url ? 'url("' + url + '")' : 'var(--wp, url(/assets/img/wp/lake.webp))';
    bg.classList.add('on');
  }
  function local() { show(null); }
  function bing(u) { return typeof u === 'string' && /^https:\/\/([a-z0-9-]+\.)?bing\.com\//i.test(u); }
  function credit(c, l) {
    var box = $('#nfc'), a = $('#nfcl'), t = $('#nfct');
    if (!box || !c) return;
    if (bing(l)) { a.href = l; a.textContent = c; } else { t.textContent = c; }
    box.hidden = false;
  }
  function load(u, c, l) {
    var img = new Image(), t = setTimeout(local, 6000);
    img.onload = function () { clearTimeout(t); if (!done) { credit(c, l); show(u); } };
    img.onerror = function () { clearTimeout(t); local(); };
    img.src = u;
  }
  function today() { var x = new Date(); return x.getFullYear() + '-' + (x.getMonth() + 1) + '-' + x.getDate(); }
  function res() { var w = innerWidth * (devicePixelRatio || 1); return w <= 1400 ? '1366' : w <= 2200 ? '1920' : 'UHD'; }
  try {
    var c = JSON.parse(get('cf_bing') || 'null');
    if (c && c.d === today() && c.r === res() && bing(c.u)) { load(c.u, c.c, c.l); return; }
  } catch (e) {}
  if (!window.fetch) { local(); return; }
  var ac = window.AbortController ? new AbortController() : null, to = setTimeout(function () { if (ac) ac.abort(); local(); }, 3000);
  fetch('https://bing.biturl.top/?resolution=' + res() + '&format=json&index=0&mkt=zh-CN', ac ? { signal: ac.signal } : undefined)
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (j) {
      clearTimeout(to);
      if (!j || !bing(j.url)) throw 0;
      var cp = typeof j.copyright === 'string' ? j.copyright.slice(0, 160) : '';
      set('cf_bing', JSON.stringify({ d: today(), r: res(), u: j.url, c: cp, l: bing(j.copyright_link) ? j.copyright_link : '' }));
      load(j.url, cp, j.copyright_link);
    })
    .catch(function () { clearTimeout(to); local(); });
})();
