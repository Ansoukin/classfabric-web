(function () {
  var d = document;
  function $(s) { return d.querySelector(s); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* 404 诗：每次打开随机一首，「换一首」不会重复当前这首。颜文字与诗一一对应。 */
  var POEMS = [
    ['¯\\_(ツ)_/¯', ['路牌还立在原处，', '路却被谁悄悄收走了。', '你来得没有错，', '只是这里，今天什么也没有。']],
    ['(´･ω･`)', ['我朝这个地址喊了一声，', '没有人应，只有回声说：', '「找不到。」', '它说得那样轻，像怕吵醒什么。']],
    ['(・_・;)', ['门是开着的，', '灯也曾亮过。', '主人搬走时忘了留话，', '这一页，去了别处。']],
    ['(°ー°〃)', ['四，像一扇半掩的门；', '零，是门后那片空；', '四，又是一扇门。', '你推开的，全是风。']],
    ['( ˘ω˘ )', ['有些链接像蒲公英，', '被一阵风吹散了。', '你捡起其中一朵，', '它说：我也不知道落在了哪里。']],
    ['(；′⌒`)', ['地图上没有这个点，', '指南针转了半圈又停下。', '迷路并不可耻，', '来时的路，还在身后。']],
    ['(´･_･`)', ['也许它存在过，', '在某个下午，某次点击里。', '现在只剩你记得的这个地址，', '和一个很礼貌的 404。']]
  ];
  var dlg = $('.nf-dlg'), k = $('#nfk'), pl = $('#nfpl'), sw = $('#nfsw'), cur = parseInt(get('cf_nfp'), 10);
  function other() { var n = Math.floor(Math.random() * POEMS.length); return n === cur ? (n + 1 + Math.floor(Math.random() * (POEMS.length - 1))) % POEMS.length : n; }
  function render(n) {
    cur = n; set('cf_nfp', String(n));
    k.textContent = POEMS[n][0]; pl.textContent = '';
    POEMS[n][1].forEach(function (t) { var s = d.createElement('span'); s.textContent = t; pl.appendChild(s); });
  }
  if (dlg && k && pl) {
    render(other());
    if (sw) {
      sw.hidden = false;
      sw.addEventListener('click', function () {
        dlg.classList.add('sw');
        setTimeout(function () { render(other()); dlg.classList.remove('sw'); }, 140);
      });
    }
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
