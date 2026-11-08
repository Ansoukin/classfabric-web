(function () {
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
    var h = '<em class="bdg sm">' + ARCHN[p.arch] + '</em>';
    if (p.form === 'inst' || p.form === 'dir') h += p.rt === 'fd' ? '<em class="bdg sm amber">需 .NET 桌面运行时</em>' : '<em class="bdg sm green">自带运行时</em>';
    return h;
  }

  function card(p, rec) {
    return '<a class="ac' + (rec ? ' rec' : '') + '"' + (p.rt === 'fd' ? ' data-rt="fd"' : '') + ' href="' + p.a.browser_download_url + '" rel="noopener"><span class="ai"><svg viewBox="0 0 24 24"><path d="' + p.ic + '"/></svg></span><span class="at"><b>' + p.t + (rec ? '<u>推荐</u>' : '') + '</b><span class="chs">' + chips(p) + '</span>' + (p.d ? '<span class="ds">' + p.d + '</span>' : '') + '<code>' + p.a.name + '</code></span><span class="am"><em>' + fmt(p.a.size) + '</em><i class="dlb"><svg viewBox="0 0 24 24"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 20h14"/></svg></i></span></a>';
  }
  function bySc(a, b) { return a.sc - b.sc; }

  function shareLink(btn) {
    var u = location.origin + '/download.html';
    if (navigator.share) { navigator.share({ title: '下载 ClassFabric', text: '请在 Windows 电脑上打开此链接下载 ClassFabric', url: u }).catch(function () { }); return; }
    var done = function () { var o = btn.innerHTML; btn.textContent = '已复制链接，发到电脑上打开吧'; setTimeout(function () { btn.innerHTML = o; }, 2600); };
    if (navigator.clipboard) navigator.clipboard.writeText(u).then(done, function () { prompt('复制此链接：', u); });
    else prompt('复制此链接：', u);
  }

  function note(html, cls) {
    var n = $('#plat'); if (!n) return;
    if (!html) { n.hidden = true; return; }
    n.hidden = false; n.className = 'dlx-note' + (cls ? ' ' + cls : ''); n.innerHTML = html;
    var b = $('[data-share]', n); if (b) b.addEventListener('click', function () { shareLink(b); });
  }

  var IC_I = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/></svg>';
  var SHARE_BTN = '<button type="button" class="fb sm" data-share>把下载链接发到电脑</button>';

  function render() {
    var r = pick(), box = $('#assets'), dl = $('[data-dl]'), sub = $('[data-dlsub]');
    $$('[data-badge]').forEach(function (e) { e.hidden = chan !== 'pre'; });
    var tip = $('#chanTip'); if (tip) tip.textContent = chan === 'pre' ? '最新预览版' : '最新稳定版';
    fillHist();
    if (!r) {
      $$('[data-ver]').forEach(function (e) { e.textContent = chan === 'pre' ? '暂无预览版' : '—'; e.classList.remove('sk'); });
      $$('[data-date]').forEach(function (e) { e.textContent = '—'; });
      if (box) box.innerHTML = '<div class="none">' + (chan === 'pre' ? '目前没有发布预览版，请先使用稳定版。' : '暂无可下载的版本。') + '</div>';
      if (dl) dl.classList.add('dis');
      if (sub) sub.textContent = '';
      return;
    }
    $$('[data-ver]').forEach(function (e) { e.textContent = r.tag_name; e.classList.remove('sk'); });
    $$('[data-date]').forEach(function (e) { e.textContent = (r.published_at || '').slice(0, 10); e.classList.remove('sk'); });
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
    if (sub) {
      if (mobile) sub.textContent = '检测到 ' + OSN[P.os] + ' 设备，ClassFabric 目前仅支持 Windows 电脑';
    }

    if (P.os === 'android' || P.os === 'ios') note(IC_I + '<div><b>暂不支持 ' + OSN[P.os] + '</b><p>ClassFabric 是为 Windows 电脑上的班级大屏设计的，目前没有手机或平板版本，也暂无相关计划。请在要使用的 Windows 电脑上打开本页下载。</p>' + SHARE_BTN + '</div>', 'warn');
    else if (P.oldWin) note(IC_I + '<div><b>检测到较旧的 Windows</b><p>ClassFabric 需要 Windows 10 或更高版本。</p></div>', 'warn');
    else if (P.os === 'macos' || P.os === 'linux' || P.os === 'chromeos') note(IC_I + '<div><b>检测到 ' + OSN[P.os] + '</b><p>' + (native.length ? '已为你找到适用于 ' + OSN[P.os] + ' 的文件。' : '官方构建目前只提供 Windows 版本。代码中保留了相关支持，暂无测试环境，欢迎自行从源码构建或帮助测试。') + '</p></div>', '');
    else if (P.os === 'windows' && P.arch === 'arm64' && present.indexOf('arm64') < 0) note(IC_I + '<div><b>检测到 ARM64 设备</b><p>当前版本暂无 ARM64 构建，x64 版本可通过系统自带的转译运行。</p></div>', '');
    else note('');

    if (!box) return;
    var h = '';
    if (present.length > 1) h += '<div class="archbar seg4" role="tablist" aria-label="处理器架构">' + present.map(function (x) {
      return '<button type="button" role="tab" data-arch="' + x + '" class="' + (x === arch ? 'on' : '') + '">' + ARCHN[x] + (x === P.arch && P.os === 'windows' ? '<small>你的设备</small>' : '') + '</button>';
    }).join('') + '</div>';
    var list = win.filter(function (p) { return p.arch === arch; }).sort(bySc);
    h += '<div class="alist">' + (list.length ? list.map(function (p) { return card(p, p === best); }).join('') : '<div class="none">该版本暂无 Windows 文件，请前往 GitHub 查看。</div>') + '</div>';
    if (oth.length) h += '<details class="aoth"><summary>其他平台与文件<em class="cnt">' + oth.length + ' 个文件</em></summary><div class="alist">' + oth.sort(bySc).map(function (p) { return card(p, false); }).join('') + '</div></details>';
    box.innerHTML = h;
    $$('[data-arch]', box).forEach(function (b) { b.addEventListener('click', function () { arch = b.dataset.arch; render(); }); });
  }

  function fillHist() {
    var box = $('#hist'); if (!box || !rels) return;
    var list = rels.filter(function (r) { return !r.draft; }).slice(0, 12);
    box.innerHTML = list.length ? list.map(function (r, i) {
      var n = (r.assets || []).filter(function (a) { return parse(a); }).length;
      return '<li><a href="' + r.html_url + '" rel="noopener"><b>' + (r.name || r.tag_name) + '</b>' + (r.prerelease ? '<em class="bdg">预览版</em>' : '') + (i === 0 ? '<em class="bdg cur">最新</em>' : '') + '<span class="hd">' + (r.published_at || '').slice(0, 10) + '</span><span class="hn">' + n + ' 个文件</span><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></a></li>';
    }).join('') : '<li class="none">暂无历史版本。</li>';
  }

  $$('[data-chan]').forEach(function (b) {
    b.addEventListener('click', function () {
      chan = b.dataset.chan; $$('[data-chan]').forEach(function (x) { x.classList.toggle('on', x === b); }); render();
    });
  });

  function go(r) { rels = r; render(); }
  function load() {
    var cache = null; try { cache = JSON.parse(localStorage.getItem('cf_rels') || 'null'); } catch (e) { }
    if (cache && Date.now() - cache.t < 36e5) { go(cache.r); return; }
    fetch('https://api.github.com/repos/' + REPO + '/releases?per_page=20').then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .then(function (r) { go(r); try { localStorage.setItem('cf_rels', JSON.stringify({ t: Date.now(), r: r })); } catch (e) { } })
      .catch(function () {
        $$('[data-ver]').forEach(function (e) { e.textContent = '见 GitHub'; e.classList.remove('sk'); });
        var box = $('#assets'); if (box) box.innerHTML = '<div class="none">暂时无法读取版本信息，请前往 <a href="https://github.com/' + REPO + '/releases" rel="noopener">GitHub Releases</a> 下载。</div>';
        var hs = $('#hist'); if (hs) hs.innerHTML = '<li class="none">暂时无法读取。</li>';
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

  var NET = 'https://dotnet.microsoft.com/zh-cn/download/dotnet/10.0', WINGET = 'winget install Microsoft.DotNet.DesktopRuntime.10', dlg = null;
  function openNet(href, name) {
    if (!dlg) {
      dlg = document.createElement('dialog'); dlg.className = 'cfm'; dlg.setAttribute('aria-labelledby', 'cfmT');
      dlg.innerHTML = '<div class="cfm-b"><span class="cfm-i"><svg viewBox="0 0 24 24"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/></svg></span>'
        + '<h3 id="cfmT">这个版本需要 .NET 10 桌面运行时</h3>'
        + '<p>你选择的文件依赖本机已安装的 .NET 桌面运行时，没有它程序无法启动。请先安装 .NET 10 桌面运行时（Desktop Runtime），再运行 ClassFabric。</p>'
        + '<div class="cfm-c"><code></code><button type="button" data-copy>复制</button></div>'
        + '<div class="cfm-f"><a class="fb acc lg" href="' + NET + '" target="_blank" rel="noopener">前往 .NET 10 下载页</a>'
        + '<div class="cfm-x"><a class="fb" data-go href="#">我已安装，继续下载</a><button type="button" class="fb" data-close>取消</button></div></div>'
        + '<p style="margin-top:var(--s-3);font-size:var(--fs-1)">不想另装运行时？选择带「自带运行时」标记的安装程序即可。</p></div>';
      document.body.appendChild(dlg);
      $('code', dlg).textContent = WINGET;
      $('[data-close]', dlg).addEventListener('click', function () { dlg.close(); });
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
      $('[data-go]', dlg).addEventListener('click', function () { setTimeout(function () { dlg.close(); }, 200); });
      $('[data-copy]', dlg).addEventListener('click', function (e) {
        var b = e.currentTarget, done = function () { b.textContent = '已复制'; setTimeout(function () { b.textContent = '复制'; }, 1800); };
        if (navigator.clipboard) navigator.clipboard.writeText(WINGET).then(done, function () { }); else done();
      });
    }
    $('[data-go]', dlg).href = href;
    if (dlg.showModal) dlg.showModal(); else window.open(NET, '_blank');
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-rt="fd"]');
    if (!a || a.classList.contains('share') || e.defaultPrevented || e.button) return;
    e.preventDefault(); openNet(a.href, a.textContent);
  });
})();
