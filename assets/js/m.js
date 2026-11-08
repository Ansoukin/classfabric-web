(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var tabs = $$('#remTabs [data-g]'), figs = $$('.mrem .mrf');
  function show(i) {
    tabs.forEach(function (b) { b.classList.toggle('on', +b.dataset.g === i); });
    figs.forEach(function (f) { f.classList.toggle('on', +f.dataset.g === i); });
  }
  tabs.forEach(function (b) { b.addEventListener('click', function () { show(+b.dataset.g); }); });
  show(0);

  var lb = null;
  function close() {
    if (!lb) return;
    var l = lb; lb = null;
    l.classList.remove('on'); document.documentElement.classList.remove('lbo');
    setTimeout(function () { if (l.parentNode) l.parentNode.removeChild(l); }, 280);
  }
  function open(fig) {
    var img = $('img', fig); if (!img || lb) return;
    lb = document.createElement('div');
    lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', img.alt);
    lb.innerHTML = '<button type="button" class="lbx" aria-label="关闭"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button><div class="lbs"><img alt=""></div><p class="lbh">拖动查看细节　·　点按空白处关闭</p>';
    var im = $('img', lb); im.src = img.currentSrc || img.src; im.alt = img.alt; im.style.width = (+fig.dataset.zw || 720) + 'px';
    document.body.appendChild(lb); document.documentElement.classList.add('lbo');
    var sc = $('.lbs', lb);
    requestAnimationFrame(function () { lb.classList.add('on'); sc.scrollLeft = Math.max(0, (sc.scrollWidth - sc.clientWidth) / 2); });
    lb.addEventListener('click', function (e) { if (!e.target.closest('.lbs img')) close(); });
  }
  document.addEventListener('click', function (e) {
    var f = e.target.closest && e.target.closest('.shotf[data-zoom]');
    if (f) open(f);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
    else if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('.shotf[data-zoom]')) { e.preventDefault(); open(e.target); }
  });
  /* 横向滑动的卡片组：在下方给出位置圆点，让用户知道还有几张 */
  Array.prototype.forEach.call(document.querySelectorAll('.subs,.steps3,.themes3'), function (sc) {
    var n = sc.children.length;
    if (n < 2 || sc.scrollWidth <= sc.clientWidth + 4) return;
    var d = document.createElement('div'), t = 0, i;
    d.className = 'dots'; d.setAttribute('aria-hidden', 'true');
    for (i = 0; i < n; i++) d.appendChild(document.createElement('i'));
    sc.parentNode.insertBefore(d, sc.nextSibling);
    function sync() {
      t = 0;
      var max = sc.scrollWidth - sc.clientWidth, k = max > 0 ? Math.round(sc.scrollLeft / max * (n - 1)) : 0;
      Array.prototype.forEach.call(d.children, function (c, j) { c.classList.toggle('on', j === k); });
    }
    sc.addEventListener('scroll', function () { if (!t) t = requestAnimationFrame(sync); }, { passive: true });
    sync();
  });
})();
