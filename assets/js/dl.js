(function () {
  var cfBar = function () { return window.cfBar.apply(null, arguments); };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var REPO = 'Ansoukin/ClassFabric';
  if (!window.fetch || !($('[data-ver]') || $('#assets'))) return;

  var ua = navigator.userAgent || '';
  var P = { os: 'other', arch: 'x64', oldWin: false };
  if (/Android/i.test(ua)) P.os = 'android';
  else if (/iPhone|iPad|iPod/i.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1)) P.os = 'ios';
  else if (/Windows/i.test(ua)) P.os = 'windows';
  else if (/CrOS/.test(ua)) P.os = 'chromeos';
  else if (/Mac OS X|Macintosh/.test(ua)) P.os = 'macos';
  else if (/Linux|X11/.test(ua)) P.os = 'linux';
  if (/arm64|aarch64/i.test(ua)) P.arch = 'arm64';
  P.oldWin = /Windows NT [1-6]\./.test(ua) && !/Windows NT 10/.test(ua);
  var mobile = P.os === 'android' || P.os === 'ios';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  var OSN = { windows: 'Windows', android: 'Android', ios: 'iPhone / iPad', macos: 'macOS', linux: 'Linux', chromeos: 'ChromeOS', other: '当前系统' };
  var ARCHN = { x64: 'x64', x86: 'x86（32 位）', arm64: 'ARM64', arm: 'ARM（32 位）' };
  var ARCHS = ['x64', 'arm64', 'x86', 'arm'];
  var rels = null, chan = 'stable', arch = P.arch;

  function fmt(n) { return n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.round(n / 1024) + ' KB'; }
  function pick() { if (!rels) return null; for (var i = 0; i < rels.length; i++) { var r = rels[i]; if (!r.draft && (chan === 'pre' ? r.prerelease : !r.prerelease)) return r; } return null; }

  var ICON = {
    exe: 'M12 3v10m0 0l-4-4m4 4l4-4M5 17v2a2 2 0 002 2h10a2 2 0 002-2v-2',
    dir: 'M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z',
    one: 'M5 4h9l5 5v11H5zM14 4v5h5',
    pkg: 'M12 3l8 4.5v9L12 21l-8-4.5v-9zM4 7.5l8 4.5 8-4.5M12 12v9'
  };

  function parse(a) {
    var n = a.name, l = n.toLowerCase();
    if (/\.(sha\d*|sig|asc|txt|json|md|ya?ml|blockmap|pdb|sum)$/.test(l) || /^source|^checksums?/.test(l)) return null;
    var os = /windows|(^|[_.-])win(32|64)?([_.-]|$)|\.msi$/.test(l) ? 'windows'
      : /linux|appimage|\.deb$|\.rpm$/.test(l) ? 'linux'
      : /macos|osx|darwin|\.dmg$|\.pkg$/.test(l) ? 'macos'
      : /android|\.apk$/.test(l) ? 'android'
      : /\.(exe|zip)$/.test(l) ? 'windows' : 'other';
    var ar = /x86[_-]64|amd64|x64/.test(l) ? 'x64'
      : /arm64|aarch64/.test(l) ? 'arm64'
      : /(^|[^a-z0-9])(x86|i[3-6]86|win32)([^a-z0-9]|$)/.test(l) ? 'x86'
      : /(^|[^a-z0-9])arm(v7)?([^a-z0-9]|$)/.test(l) ? 'arm' : 'x64';
    var rt = /self-?contained/.test(l) ? 'sc' : /(^|[^a-z])(full|frameworkdependent|fd)([^a-z]|$)/.test(l) ? 'fd' : '';
    var form = /installer|setup|\.msi$/.test(l) ? 'inst' : /single-?file|portable/.test(l) ? 'one' : /\.(zip|7z|tar\.gz|tgz)$/.test(l) ? 'dir' : 'pkg';
    var t, d, sc, ic;
    if (form === 'inst') { t = '安装程序'; d = '按向导安装，适合大多数用户。' + (rt === 'fd' ? '需本机已有 .NET 桌面运行时。' : '已内置运行时，无需另装。'); sc = rt === 'fd' ? 1 : 0; ic = ICON.exe; }
    else if (form === 'one') { t = '单文件版'; d = '单个可执行文件，无需解压。'; sc = 4; ic = ICON.one; }
    else if (form === 'dir') {
      ic = ICON.dir;
      if (rt === 'sc') { t = '免安装 · 自带运行时'; d = '解压即用，无需另装运行时，体积较大。'; sc = 2; }
      else if (rt === 'fd') { t = '免安装 · 依赖运行时'; d = '解压即用，需本机已有 .NET 桌面运行时，体积较小。'; sc = 3; }
      else { t = '免安装版'; d = '解压即用。'; sc = 3; }
    } else { t = (l.split('.').pop() || 'file').toUpperCase() + ' 包'; d = ''; sc = 5; ic = ICON.pkg; }
    return { a: a, os: os, arch: ar, t: t, d: d, sc: sc, ic: ic, rt: rt, form: form };
  }

  function chips(p) {
    var h = ARCHN[p.arch];
    if (p.form === 'inst' || p.form === 'dir') h += ' · ' + (p.rt === 'fd' ? '<span class="dl-rt need">需 .NET 桌面运行时</span>' : '<span class="dl-rt ok">自带运行时</span>');
    return h;
  }

  function card(p, rec, i) {
    return '<a class="dl-row dl-file dl-in" style="--i:' + (i || 0) + '"' + (p.rt === 'fd' ? ' data-rt="fd"' : '') + ' href="' + p.a.browser_download_url + '" rel="noopener"><span class="dl-tx"><b>' + p.t + (rec ? '<em class="dl-rec">推荐</em>' : '') + '</b>' + (p.d ? '<span class="dl-ds">' + p.d + '</span>' : '') + '<span class="dl-fl"><span>' + chips(p) + '</span><code>' + p.a.name + '</code></span></span><span class="dl-sz">' + fmt(p.a.size) + '</span><span class="dl-go">下载</span></a>';
  }
  function bySc(a, b) { return a.sc - b.sc; }

  function shareLink(btn) {
    var u = location.origin + '/download.html';
    if (navigator.share) { navigator.share({ title: '下载 ClassFabric', text: '请在 Windows 电脑上打开此链接下载 ClassFabric', url: u }).catch(function () { }); return; }
    var done = function () { var o = btn.innerHTML; btn.textContent = '已复制链接，发到电脑上打开吧'; setTimeout(function () { btn.innerHTML = o; }, 2600); };
    if (navigator.clipboard) navigator.clipboard.writeText(u).then(done, function () { prompt('复制此链接：', u); });
    else prompt('复制此链接：', u);
  }

  function note(html) {
    var n = $('#plat'); if (!n) return;
    if (!html) { n.hidden = true; return; }
    n.hidden = false; n.innerHTML = html;
  }

  var IC_I = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/></svg>';

  function render() {
    var r = pick(), box = $('#assets'), dl = $('[data-dl]');
    $$('[data-badge]').forEach(function (e) { e.hidden = chan !== 'pre'; });
    var tip = $('#chanTip'); if (tip) tip.textContent = chan === 'pre' ? '最新预览版' : '最新稳定版';
    var cd = $('#chanDesc'); if (cd) cd.textContent = chan === 'pre' ? '预览版包含尚未稳定的新功能，遇到问题欢迎反馈。' : '不确定选哪个？下载第一项即可。';
    var ch = $('#chan'); if (ch && rels) ch.hidden = !rels.some(function (x) { return !x.draft && x.prerelease; });
    fillHist();
    if (!r) {
      $$('[data-ver]').forEach(function (e) { e.textContent = chan === 'pre' ? '暂无预览版' : '—'; e.classList.remove('dl-sk'); });
      $$('[data-date]').forEach(function (e) { e.textContent = '—'; });
      if (box) box.innerHTML = '<div class="dl-none">' + (chan === 'pre' ? '目前没有发布预览版，请先使用稳定版。' : '暂无可下载的版本。') + '</div>';
      if (dl) dl.classList.add('dis');
      $$('[data-dlsize]').forEach(function (e) { e.textContent = ''; });
      return;
    }
    $$('[data-ver]').forEach(function (e) { e.textContent = r.tag_name; e.classList.remove('dl-sk'); });
    $$('[data-date]').forEach(function (e) { e.textContent = (r.published_at || '').slice(0, 10); e.classList.remove('dl-sk'); });
    $$('[data-releaselink]').forEach(function (e) { e.href = r.html_url; });

    var items = (r.assets || []).map(parse).filter(Boolean);
    var win = items.filter(function (p) { return p.os === 'windows'; });
    var native = items.filter(function (p) { return p.os === P.os && P.os !== 'windows'; });
    var oth = items.filter(function (p) { return p.os !== 'windows'; });
    var present = ARCHS.filter(function (x) { return win.some(function (p) { return p.arch === x; }); });
    $$('[data-archs]').forEach(function (e) { e.textContent = present.length ? present.map(function (x) { return x === 'x64' ? 'x64' : x === 'arm64' ? 'ARM64' : x; }).join(' / ') : 'x64'; });
    if (present.indexOf(arch) < 0) arch = present[0] || 'x64';

    var best = win.filter(function (p) { return p.arch === arch; }).sort(bySc)[0] || win.slice().sort(bySc)[0];
    if (P.os !== 'windows' && P.os !== 'android' && P.os !== 'ios' && native.length) best = native.slice().sort(bySc)[0];

    if (dl) {
      dl.classList.remove('dis');
      if (mobile) {
        dl.removeAttribute('href'); dl.classList.add('share');
        dl.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 15V4m0 0L8 8m4-4l4 4M5 13v6a2 2 0 002 2h10a2 2 0 002-2v-6"/></svg>把下载链接发到电脑';
        if (!dl.__s) { dl.__s = 1; dl.addEventListener('click', function (e) { e.preventDefault(); shareLink(dl); }); }
      } else { dl.href = best ? best.a.browser_download_url : r.html_url; if (best && best.rt === 'fd') dl.setAttribute('data-rt', 'fd'); else dl.removeAttribute('data-rt'); }
    }
    $$('[data-dlsize]').forEach(function (e) { e.textContent = best && !mobile ? fmt(best.a.size) : ''; });

    if (P.os === 'android' || P.os === 'ios') note(IC_I + '<div><b>暂不支持 ' + OSN[P.os] + '</b><p>ClassFabric 是为 Windows 电脑上的班级大屏设计的，目前没有手机或平板版本，也暂无相关计划。请在要使用的 Windows 电脑上打开本页下载。</p>' + '</div>', 'warn');
    else if (P.oldWin) note(IC_I + '<div><b>检测到较旧的 Windows</b><p>ClassFabric 需要 Windows 10 或更高版本。</p></div>', 'warn');
    else if (P.os === 'macos' || P.os === 'linux' || P.os === 'chromeos') note(IC_I + '<div><b>检测到 ' + OSN[P.os] + '</b><p>' + (native.length ? '已为你找到适用于 ' + OSN[P.os] + ' 的文件。' : '官方构建目前只提供 Windows 版本。代码中保留了相关支持，暂无测试环境，欢迎自行从源码构建或帮助测试。') + '</p></div>', '');
    else if (P.os === 'windows' && P.arch === 'arm64' && present.indexOf('arm64') < 0) note(IC_I + '<div><b>检测到 ARM64 设备</b><p>当前版本暂无 ARM64 构建，x64 版本可通过系统自带的转译运行。</p></div>', '');
    else note('');

    if (!box) return;
    var h = '';
    if (present.length > 1) h += '<div class="dl-sel" role="tablist" aria-label="处理器架构">' + present.map(function (x) {
      return '<button type="button" role="tab" data-arch="' + x + '" class="' + (x === arch ? 'on' : '') + '" aria-selected="' + (x === arch) + '">' + ARCHN[x] + (x === P.arch && P.os === 'windows' ? '<small>你的设备</small>' : '') + '</button>';
    }).join('') + '</div>';
    var list = win.filter(function (p) { return p.arch === arch; }).sort(bySc);
    h += '<div class="dl-list">' + (list.length ? list.map(function (p, i) { return card(p, p === best, i); }).join('') : '<div class="dl-none">该版本暂无 Windows 文件，请前往 GitHub 查看。</div>') + '</div>';
    if (oth.length) h += '<details class="dl-oth"><summary>其他平台与文件<em>' + oth.length + ' 个文件</em></summary><div class="dl-list">' + oth.sort(bySc).map(function (p, i) { return card(p, false, i); }).join('') + '</div></details>';
    var hadFocus = box.contains(document.activeElement) && document.activeElement.hasAttribute('data-arch');
    box.innerHTML = h;
    $$('[data-arch]', box).forEach(function (b) { b.addEventListener('click', function () { arch = b.dataset.arch; render(); }); });
    var ab = $('.dl-sel', box); if (ab) { cfBar(ab, 'dl-ind'); if (hadFocus) { var cur = $('[aria-selected="true"]', ab); if (cur) cur.focus(); } }
  }

  function fillHist() {
    var box = $('#hist'); if (!box || !rels) return;
    var list = rels.filter(function (r) { return !r.draft; }).slice(0, 6);
    var chev = '<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>';
    box.innerHTML = list.length ? list.map(function (r, i) {
      return '<li class="dl-in" style="--i:' + i + '"><a class="dl-row" href="' + r.html_url + '" rel="noopener"><b>' + (r.name || r.tag_name) + '</b>' + (r.prerelease ? '<span class="dl-pre">预览版</span>' : '') + '<span class="dl-hd">' + (r.published_at || '').slice(0, 10) + '</span>' + chev + '</a></li>';
    }).join('') + '<li class="dl-in" style="--i:' + list.length + '"><a class="dl-row dl-more" href="https://github.com/' + REPO + '/releases" rel="noopener">在 GitHub 查看全部版本' + chev + '</a></li>' : '<li class="dl-none">暂无历史版本。</li>';
  }

  $$('[data-chan]').forEach(function (b) {
    b.addEventListener('click', function () {
      chan = b.dataset.chan; $$('[data-chan]').forEach(function (x) { var on = x.dataset.chan === chan; x.classList.toggle('on', on); x.setAttribute('aria-selected', on); }); render();
    });
  });

  cfBar($('#chan'), 'dl-ind');

  function go(r) { rels = r; render(); }
  function load() {
    var cache = null; try { cache = JSON.parse(localStorage.getItem('cf_rels') || 'null'); } catch (e) { }
    if (cache && Date.now() - cache.t < 36e5) { go(cache.r); return; }
    fetch('https://api.github.com/repos/' + REPO + '/releases?per_page=20').then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .then(function (r) { go(r); try { localStorage.setItem('cf_rels', JSON.stringify({ t: Date.now(), r: r })); } catch (e) { } })
      .catch(function () {
        $$('[data-ver]').forEach(function (e) { e.textContent = '见 GitHub'; e.classList.remove('dl-sk'); });
        var box = $('#assets'); if (box) box.innerHTML = '<div class="dl-none">暂时无法读取版本信息，请前往 <a href="https://github.com/' + REPO + '/releases" rel="noopener">GitHub Releases</a> 下载。</div>';
        var hs = $('#hist'); if (hs) hs.innerHTML = '<li class="dl-none">暂时无法读取。</li>';
      });
  }

  var uad = navigator.userAgentData;
  if (uad && uad.getHighEntropyValues && P.os === 'windows') {
    uad.getHighEntropyValues(['architecture', 'bitness']).then(function (v) {
      if (v.architecture === 'arm') P.arch = 'arm64';
      else if (v.architecture === 'x86') P.arch = v.bitness === '32' ? 'x86' : 'x64';
      arch = P.arch; if (rels) render();
    }).catch(function () { });
  }
  load();

  /* 点击下载：按钮图标变 ✓、底部进度线扫过；舞台里的灵动岛切到「下载已开始」，随后恢复循环 */
  function started() {
    var b = $('[data-dl]'), t = b && $('span', b);
    if (!t || mobile || b.classList.contains('done')) return;
    var desk = $('.dl-desk'); if (desk) desk.classList.add('launch');
    var o = t.textContent, sv = $('svg', b), osv = sv && sv.innerHTML, st = $('.isl-stack[data-demo]'), ok = $('.dl-ok .isl');
    b.classList.add('done'); t.textContent = '下载已开始'; if (sv) sv.innerHTML = '<path d="M5 12.5l4.5 4.5L19 7"/>';
    if (st && st._c && ok) { st._c.stop(); $$('.isl', st).forEach(function (n) { n.classList.remove('on'); }); ok.classList.add('on'); }
    setTimeout(function () {
      if (desk) desk.classList.remove('launch');
      b.classList.remove('done'); t.textContent = o; if (sv) sv.innerHTML = osv;
      if (st && st._c && ok) { ok.classList.remove('on'); st._c.start(); }
    }, 3150);
  }

  /* 舞台前景是按 1000px 虚拟桌面绘制的，按舞台宽度整体缩放 */
  var stg = $('.dl-stage');
  if (stg) {
    var fitK = function () { stg.style.setProperty('--k', (stg.clientWidth / 1000).toFixed(4)); };
    fitK(); if (window.ResizeObserver) new ResizeObserver(fitK).observe(stg); else addEventListener('resize', fitK);
  }

  /* 舞台三层随指针轻微偏移（仅 hover 设备、减少动态时关闭） */
  var stage = $('.dl-stage');
  if (stage && !reduce && window.matchMedia && matchMedia('(hover: hover)').matches) {
    var raf = 0;
    document.addEventListener('pointermove', function (e) {
      if (raf || innerWidth < 900) return;
      var cx = e.clientX, cy = e.clientY;
      raf = requestAnimationFrame(function () {
        raf = 0; var r = stage.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
        stage.style.setProperty('--mx', ((cx / innerWidth - .5) * 2).toFixed(3)); stage.style.setProperty('--my', ((cy / innerHeight - .5) * 2).toFixed(3));
      });
    }, { passive: true });
  }

  var files = $('#files'), ft = $('.dl-fold-t');
  if (mobile && files && ft) {
    files.classList.add('fold');
    ft.addEventListener('click', function () { var o = files.classList.toggle('open'); ft.setAttribute('aria-expanded', o); ft.textContent = o ? '收起文件' : '查看全部文件'; });
  }

  var NET = 'https://dotnet.microsoft.com/zh-cn/download/dotnet/10.0', WINGET = 'winget install Microsoft.DotNet.DesktopRuntime.10', dlg = null;
  function openNet(href, name) {
    if (!dlg) {
      dlg = document.createElement('dialog'); dlg.className = 'cfm'; dlg.setAttribute('aria-labelledby', 'cfmT'); dlg.setAttribute('aria-describedby', 'cfmD');
      dlg.innerHTML = '<div class="cfm-b"><h3 id="cfmT">需要先安装 .NET 10 桌面运行时</h3>'
        + '<p id="cfmD">你选择的这个文件依赖本机已安装的 .NET 桌面运行时（Desktop Runtime），没有它程序无法启动。</p>'
        + '<p class="cfm-l">已有 winget？在终端运行：</p><div class="cfm-c"><code></code><button type="button" data-copy>复制</button></div>'
        + '<p class="cfm-h">不想另装？选择带「自带运行时」标记的安装程序即可。</p></div>'
        + '<div class="cfm-f"><a class="cfm-btn pri" href="' + NET + '" target="_blank" rel="noopener" autofocus>前往 .NET 下载页</a><a class="cfm-btn" data-go href="#">我已安装，继续下载</a><button type="button" class="cfm-btn" data-close>取消</button></div>';
      document.body.appendChild(dlg);
      $('code', dlg).textContent = WINGET;
      $('[data-close]', dlg).addEventListener('click', function () { dlg.close(); });
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
      $('[data-go]', dlg).addEventListener('click', function () { setTimeout(function () { dlg.close(); }, 200); started(); });
      $('[data-copy]', dlg).addEventListener('click', function (e) {
        var b = e.currentTarget, done = function () { b.textContent = '已复制'; setTimeout(function () { b.textContent = '复制'; }, 1800); };
        if (navigator.clipboard) navigator.clipboard.writeText(WINGET).then(done, function () { }); else done();
      });
    }
    $('[data-go]', dlg).href = href;
    if (dlg.showModal) dlg.showModal(); else window.open(NET, '_blank');
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button || !e.target.closest) return;
    var a = e.target.closest('a[data-rt="fd"]');
    if (a && !a.classList.contains('share')) { e.preventDefault(); openNet(a.href, a.textContent); return; }
    var d = e.target.closest('[data-dl], #assets a.dl-row');
    if (d && !d.classList.contains('share') && !d.classList.contains('dis')) started();
  });
})();
