/* 关于页：目录条随滚动高亮当前段，并让指示条滑动到对应项（SelectorBar，指示条逻辑见 site.js 的 cfBar）。 */
(function () {
  var nav = document.getElementById('abNav'); if (!nav) return;
  var links = Array.prototype.slice.call(nav.querySelectorAll('a'));
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var place = window.cfBar && window.cfBar(nav, 'ab-ind');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bar = nav.parentNode, cur = -2, raf = 0;

  function spy() {
    raf = 0;
    bar.classList.toggle('stuck', bar.getBoundingClientRect().top <= 59);
    var line = 58 + nav.offsetHeight + 48, k = -1, i;
    for (i = 0; i < secs.length; i++) if (secs[i] && secs[i].getBoundingClientRect().top <= line) k = i;
    if (innerHeight + window.pageYOffset >= document.documentElement.scrollHeight - 4) k = secs.length - 1;
    if (k === cur) return; cur = k;
    links.forEach(function (a, n) { if (n === k) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    if (k < 0) { nav.removeAttribute('data-has'); return; }
    nav.setAttribute('data-has', '');
    if (place) place();
    var a = links[k];
    if (nav.scrollWidth > nav.clientWidth) nav.scrollTo({ left: a.offsetLeft - (nav.clientWidth - a.offsetWidth) / 2, behavior: reduce ? 'auto' : 'smooth' });
  }
  addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(spy); }, { passive: true });
  addEventListener('resize', spy);
  spy();
})();
