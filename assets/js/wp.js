/* 壁纸随机：每次加载先随机选「跟随本地时间」或「纯随机」两种方式之一，再选一张（不与上一次相同）。
   时间段由壁纸画面判定：d 白天（蓝天、日光充足）/ t 晨昏（太阳贴近地平线、暖色天空）/ n 夜晚（暗色、无日光）。
   L 为画面中岛所在位置偏亮的壁纸（实测亮度 >130），主界面复刻切浅色皮肤，其余深色。
   本地时间：07–17 点白天，05–07 与 17–19 点晨昏，其余夜晚。由 <head> 内联执行，写入 --wp（1280 宽）与 --wpl（2400 宽，首页用）。 */
(function () {
  var W = { lake: 'd', pine: 'dt', dune: 'd', dawn: 't', ember: 'tn', bloom: 'n' };
  var L = { lake: 1, pine: 1, dawn: 1, dune: 1 };
  var d = document.documentElement, h = new Date().getHours();
  var ph = h >= 7 && h < 17 ? 'd' : (h >= 5 && h < 7) || (h >= 17 && h < 19) ? 't' : 'n';
  var last = ''; try { last = localStorage.getItem('cf_wp') || ''; } catch (e) { }
  var mode = Math.random() < .5 ? 'time' : 'random';
  var pool = Object.keys(W).filter(function (x) { return mode === 'random' || W[x].indexOf(ph) > -1; });
  var q = pool.filter(function (x) { return x !== last; }); if (!q.length) q = pool;
  var k = q[Math.floor(Math.random() * q.length)];
  try { localStorage.setItem('cf_wp', k); } catch (e) { }
  var big = '/assets/img/wp/' + k + (window.cfWpS ? '' : '-l') + '.webp';
  d.style.setProperty('--wp', 'url(/assets/img/wp/' + k + '.webp)');
  d.style.setProperty('--wpl', 'url(' + big + ')');
  d.dataset.wp = k; d.dataset.wpi = L[k] ? 'light' : 'dark'; d.dataset.wpm = mode; d.dataset.wpt = ph;
  window.cfWp = { key: k, mode: mode, phase: ph };
  if (window.cfWpPre) { var l = document.createElement('link'); l.rel = 'preload'; l.as = 'image'; l.href = big; l.setAttribute('fetchpriority', 'high'); document.head.appendChild(l); }
})();
