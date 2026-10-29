# -*- coding: utf-8 -*-
# Generates the static pages. Output goes to /home/claude/cf-web
import os, re
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ansoukin.top'
GH = 'https://github.com/Ansoukin/ClassFabric'
REL = GH + '/releases/latest'

def svg(inner, vb='0 0 24 24', extra='fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'):
    return '<svg viewBox="%s" %s aria-hidden="true">%s</svg>' % (vb, extra, inner)

IC = {
 'sun': svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
 'info': svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><circle cx="12" cy="7.8" r=".7" fill="currentColor"/>'),
 'clock': svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 'atom': svg('<circle cx="12" cy="12" r="1.6" fill="currentColor"/><ellipse cx="12" cy="12" rx="10" ry="4.2"/><ellipse cx="12" cy="12" rx="10" ry="4.2" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.2" transform="rotate(120 12 12)"/>', extra='fill="none" stroke="currentColor" stroke-width="1.8"'),
 'gh': svg('<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>', vb='0 0 16 16', extra='fill="currentColor"'),
 'dl': svg('<path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 20h14"/>'),
 'theme': svg('<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17a8.5 8.5 0 000-17z" fill="currentColor"/>'),
 'globe': svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.7 4 5.7 4 9s-1.4 6.3-4 9c-2.6-2.7-4-5.7-4-9s1.4-6.3 4-9z"/>', extra='fill="none" stroke="currentColor" stroke-width="1.8"'),
 'menu': svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
 'win': svg('<path d="M3 5.5l7.6-1.1v7H3zM11.6 4.3L21 3v8.4h-9.4zM3 12.6h7.6v7l-7.6-1.1zM11.6 12.6H21V21l-9.4-1.3z"/>', extra='fill="currentColor"'),
}

def head(title, desc, path, extra=''):
    url = SITE + path
    return '''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(t)s</title>
<meta name="description" content="%(d)s">
<link rel="canonical" href="%(u)s">
<meta name="theme-color" content="#f5f2eb" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#151412" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icon-192.png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ClassFabric">
<meta property="og:title" content="%(t)s">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="%(u)s">
<meta property="og:image" content="%(s)s/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/site.css">
%(x)s</head>
''' % dict(t=title, d=desc, u=url, s=SITE, x=extra)

def nav(cur):
    def a(href, label, key):
        return '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if cur == key else '', label)
    return '''<body>
<header class="nav">
 <div class="wrap">
  <a class="brand" href="/"><img src="/assets/img/icon-64.png" width="26" height="26" alt="">ClassFabric</a>
  <nav class="links" id="links" aria-label="主导航">
   %s%s%s<a href="%s" rel="noopener">GitHub 仓库</a>
  </nav>
  <div class="tools">
   <div class="langbox">
    <button class="ibtn" id="lang" aria-label="语言 / Language" aria-haspopup="true">@@globe@@</button>
    <div class="langmenu ignore" role="menu">
     <button data-lang="zh" aria-checked="true">简体中文</button>
     <button data-lang="tw" aria-checked="false">繁體中文</button>
     <button data-lang="en" aria-checked="false">English</button>
    </div>
   </div>
   <button class="ibtn" id="theme" aria-label="切换明暗主题">@@theme@@</button>
   <a class="btn primary sm" href="/download.html" data-nav-dl>@@dl@@立即下载</a>
   <button class="ibtn menu-btn" id="menu" aria-label="菜单" aria-expanded="false">@@menu@@</button>
  </div>
 </div>
</header>
''' % (a('/', '首页', 'home'), a('/download.html', '下载', 'dl'), a('/about.html', '关于', 'about'), GH)

FOOT = '''<footer class="foot">
 <div class="wrap">
  <div class="cols">
   <div>
    <a class="brand" href="/"><img src="/assets/img/icon-64.png" width="26" height="26" alt="">ClassFabric</a>
    <p class="about">ClassIsland 的个人修改版。紧跟上游，再多一点来自社区和我们自己的改进。</p>
   </div>
   <div><h5>产品</h5><ul><li><a href="/download.html">下载</a></li><li><a href="%(gh)s/releases" rel="noopener">更新日志</a></li><li><a href="/about.html#planned">计划中的功能</a></li></ul></div>
   <div><h5>项目</h5><ul><li><a href="%(gh)s" rel="noopener">GitHub 仓库</a></li><li><a href="%(gh)s/issues" rel="noopener">反馈问题</a></li><li><a href="/about.html#join">参与贡献</a></li></ul></div>
   <div><h5>了解更多</h5><ul><li><a href="/about.html">关于 ClassFabric</a></li><li><a href="/about.html#faq">常见问题</a></li><li><a href="https://classisland.tech" rel="noopener">ClassIsland 官网</a></li></ul></div>
  </div>
  <div class="legal">© 2026 ClassFabric。基于 HelloWRC 的 ClassIsland（© 2023–2026 HelloWRC）二次开发，以 GPL-3.0 协议开源。<br>ClassFabric 是个人修改版，不是 ClassIsland 官方项目；ClassIsland 的名称与原有功能归其原作者所有。</div>
 </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
''' % dict(gh=GH)

def idle(kind, p0, p1, ms):
    wx = '<span class="wx">@@sun@@9℃</span><span class="dt">周四 10/29</span>'
    past = ''.join('<span class="s p">%s</span>' % c for c in '语数英')
    if kind == 'break':
        cur = '<span class="cur">@@clock@@<span>课间休息</span><small>10:00-10:30</small></span>'
        fut = ''.join('<span class="s">%s</span>' % c for c in '物化生政历地自自')
    else:
        past = ''.join('<span class="s p">%s</span>' % c for c in '语数英')
        cur = '<span class="cur">@@atom@@<span>物理</span><span class="pill">-39m</span></span>'
        fut = ''.join('<span class="s">%s</span>' % c for c in '化生政历地自自')
    return '<div class="isl" data-ms="%d" style="--dur:%.1fs;--p0:%s;--p1:%s">%s%s%s<span class="sep"></span>%s</div>' % (ms, ms/1000, p0, p1, wx, past, cur, fut)

def mask(label, icon, ms=2300):
    return '<div class="isl mask" data-ms="%d">@@info@@<span>%s</span>@@%s@@</div>' % (ms, label, icon)

def bar_text(txt, ms=3400):
    return '<div class="isl bar" data-ms="%d" style="--dur:%.1fs">%s</div>' % (ms, ms/1000, txt)

def bar_two(left, ms=2800):
    return ('<div class="isl bar two" data-ms="%d" style="--dur:%.1fs"><span>%s</span>'
            '<span class="nx">下节课是: <em>物理</em><small>10:30-11:10</small></span></div>') % (ms, ms/1000, left)

def static(h, w):
    return h.replace('class="isl bar', 'class="isl static bar').replace('style="--dur', 'style="--w:%s;--dur' % w)

HERO_STATES = ''.join([
    idle('break', '56%', '78%', 4400),
    bar_two('距上课还剩 <b>16</b> 秒', 2800),
    mask('即将上课', 'atom', 2300),
    bar_text('准备上课，请回到座位并保持安静，做好上课准备。', 3400),
    mask('上课', 'atom', 2300),
    idle('class', '2%', '14%', 4600),
])

SPEC = ''.join([
    static(bar_two('本节课间休息长 <b>10</b> 分钟'), '38%'),
    mask('课间休息', 'clock'),
    static(bar_two('距上课还剩 <b>16</b> 秒'), '72%'),
    mask('即将上课', 'atom'),
    static(bar_text('准备上课，请回到座位并保持安静，做好上课准备。'), '55%'),
    mask('上课', 'atom'),
])

def win(src, alt, w, h, cls='main', style=''):
    return '<figure class="win %s"%s><img src="/assets/img/%s.webp" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></figure>' % (cls, (' style="%s"' % style) if style else '', src, w, h, alt)

def feat(idx, rev, title, p, pts, stage_cls, stage_html):
    lis = ''.join('<li><b>%s</b><span>%s</span></li>' % (k, v) for k, v in pts)
    return '''<div class="wrap"><div class="feat%s" id="f%d">
  <div class="copy rv"><h3>%s</h3><p>%s</p><ul class="pts">%s</ul></div>
  <div class="stage %s rv d1">%s</div>
 </div></div>
''' % (' rev' if rev else '', idx, title, p, lis, stage_cls, stage_html)

def ld():
    return '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"ClassFabric","alternateName":"ClassFabric 班级大屏课表","applicationCategory":"EducationApplication","operatingSystem":"Windows 10, Windows 11","description":"ClassIsland 的个人修改版：班级大屏课表，紧跟上游更新，原有课表、自动化、插件和主题可直接沿用。","url":"%s/","license":"https://www.gnu.org/licenses/gpl-3.0.html","isBasedOn":"https://classisland.tech","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}</script>
''' % SITE

# ---------------- index ----------------
def index():
    h = head('ClassFabric — ClassIsland 个人修改版，班级大屏课表',
             'ClassFabric 是 ClassIsland 的个人修改版：班级大屏课表，紧跟上游更新，再加入来自社区和我们自己的改进。原来的课表、自动化、插件和主题，装上就能接着用。',
             '/', ld())
    h += nav('home')
    h += '''<main>
<section class="hero"><div class="wrap">
 <span class="eyebrow rv"><i></i>ClassFabric · 班级大屏课表</span>
 <h1 class="rv">ClassIsland，<br>再多一点。</h1>
 <p class="lead rv d1">ClassFabric 是 ClassIsland 的个人修改版：紧跟上游更新，再加入来自社区和我们自己的改进。原来的课表、插件和主题，装上就能接着用。</p>
 <div class="cta rv d2">
  <a class="btn primary" href="%(rel)s" data-dl data-releaselink rel="noopener">@@dl@@下载 Windows 版</a>
  <a class="btn ghost" href="#changes">和 ClassIsland 有什么不同</a>
 </div>
 <p class="fine rv d2">Windows 10 / 11 · 免费开源（GPL-3.0）· 最新版本 <span data-ver>见 GitHub</span></p>
 <div class="hero-stage rv d2" role="img" aria-label="桌面上方的 ClassFabric 主界面，显示天气、日期和当天课程，并演示上课提醒">
  <div class="isl-wrap ignore"><div class="isl-stack" data-demo>%(hero)s</div></div>
 </div>
</div></section>

<section class="strip"><div class="wrap">
 <div class="rv"><h2>原来的配置，<br>直接沿用。</h2><p>课表、自动化、插件和主题，都不用重新做。装上 ClassFabric，接着用就行。</p></div>
 <div class="carry rv d1">
  <div><strong>课表</strong><span>多周轮换、调课照旧</span></div>
  <div><strong>自动化</strong><span>触发器与行动照旧</span></div>
  <div><strong>插件</strong><span>市场里的插件照常装</span></div>
  <div><strong>主题</strong><span>已有主题照常用</span></div>
 </div>
</div></section>
''' % dict(rel=REL, hero=HERO_STATES)

    h += feat(1, False, '上课下课，<br>大家都看得见', '上课前、上课时、下课时，主界面上方都会弹出醒目的提醒；放学和恶劣天气也会提醒。提示语可以自己改，还能语音播报。',
              [('准备上课', '上课前提醒大家回到座位；户外课会提前更久，并换成户外课专用的提示。'),
               ('提示语', '“即将上课”“上课”和准备上课的提示文字，都可以按班级习惯修改。'),
               ('更多提醒', '放学提醒、天气预警，以及由自动化发出的行动提醒。')],
              'a', '<div class="spec ignore">%s</div>' % SPEC)
    h += feat(2, True, '主界面，<br>按你的想法拼', '课表、日期、时钟、天气、倒计时……都是可以拖进主界面的组件。进入编辑模式，直接在主界面上调整；外观则用主题一键切换。',
              [('组件', '文本、课表、日期、时钟、天气简报、倒计时，以及轮播、滚动、分组和堆叠容器。'),
               ('编辑模式', '不用在设置里来回切换，直接在主界面上拖动。'),
               ('主题', '内置经典、Fluent、Rectangles 三套外观，缩放、圆角和字体也能调。')],
              'b', win('edit-library-crop', 'ClassFabric 的编辑主界面模式，底部弹出组件库', 1140, 522, 'main', 'width:96%;margin-top:-6%') +
                   '<figure class="win float" style="left:4%;bottom:5%;width:80%"><img src="/assets/img/themes-crop.webp" width="984" height="176" alt="内置的经典、Fluent 与 Rectangles 三套主题预览" loading="lazy" decoding="async"></figure>')
    h += feat(3, False, '课表、时间表、调课，<br>一个窗口搞定', '在档案编辑里管理课表、时间表和科目。每周轮换、某一天启用、循环启用都能设置；临时调课，选两节课交换一下就行。',
              [('课表', '按每周、某一天或循环启用，到日期自动切换。'),
               ('时间表', '上课、课间、分割线和行动，在时间轴上拖动编辑。'),
               ('调课', '选择两节课交换，可以只换这一次，也可以永久交换。')],
              'c', win('schedule-grid', '档案编辑窗口里的周课表与科目', 1102, 601, 'main', 'width:88%;margin:-10% 0 0 -6%') +
                   '<figure class="win float" style="right:3%;bottom:5%;width:84%"><img src="/assets/img/swap-3.webp" width="824" height="209" alt="换课窗口：数学与语文交换" loading="lazy" decoding="async"></figure>')
    h += feat(4, True, '该做的事，<br>让它自己做', '“当什么发生，并且满足什么条件，就做什么。”上课时、课间、放学、到了指定时间……都可以作为触发；行动可以是发提醒、切换设置、运行程序或打开网址。',
              [('触发', '上课、课间休息、放学、cron、特定时间点前、收到信号、托盘菜单等。'),
               ('行动', '广播信号、等待、修改应用设置、运行程序或命令、显示提醒。'),
               ('扩展', '装上 SystemTools 等社区插件，还能用到更多触发器和行动。')],
              'd', win('auto-actions-crop', '自动化页面里添加行动的菜单', 822, 610, 'main', 'width:84%'))
    h += feat(5, False, '插件，<br>想要的都能装', '插件市场就在设置里，浏览、搜索、一键安装。随机抽选、像素流动、语音包适配、UIAccess 提权……社区已经做了不少。ClassFabric 还把插件详情页的预览做得更完整，装之前先看清楚。',
              [('市场', '应用内浏览与搜索，显示下载量和星标。'),
               ('兼容', 'ClassIsland 的插件可以直接使用。')],
              'e', win('plugins-crop', '应用设置中的插件市场，右侧是 UIAccess 提权插件的详情', 957, 511, 'main', 'width:100%'))
    h += feat(6, True, '出了问题，<br>也能自己救回来', '右键托盘图标，编辑档案、换课、加载临时课表都在里面。万一软件异常，内置的恢复模式可以用安全模式启动、查看日志、恢复备份，必要时再重置配置。',
              [('托盘', '右键菜单直达常用操作。'),
               ('恢复', '安全模式、诊断模式、恢复备份、清除临时文件和分级重置。')],
              'f', '<div style="position:relative;z-index:1;display:flex;align-items:flex-end;justify-content:center;gap:5%;width:100%;height:100%">'
                   '<figure class="win" style="width:41%"><img src="/assets/img/recovery.webp" width="423" height="818" alt="ClassFabric 的恢复模式窗口" loading="lazy" decoding="async"></figure>'
                   '<figure class="win" style="width:27%;margin-bottom:6%"><img src="/assets/img/tray.webp" width="187" height="390" alt="托盘右键菜单" loading="lazy" decoding="async"></figure></div>')

    h += '''<section class="sect" id="changes"><div class="wrap">
 <div class="sect-head rv"><h2>我们在上游之上，<br>做了什么</h2><p>这里只写 ClassFabric 自己做的改动。ClassIsland 原有的功能，请看<a href="https://classisland.tech" rel="noopener">它的官网</a>。</p></div>
 <div class="cards">
  <div class="card rv"><h3>紧跟上游</h3><p>ClassIsland 发布的新功能和修复，我们会尽快同步进来，不用等。</p></div>
  <div class="card rv d1"><h3>更多天气源</h3><p>除了 ClassIsland 内置的小米天气，还可以选择 OpenWeather 和和风天气。</p></div>
  <div class="card rv d1"><h3>多语言<span class="st">实验中</span></h3><p>界面文字正在改成可翻译，已有简体中文、繁体中文和 English，通过 Crowdin 协作。还有不少地方没适配，欢迎帮忙。</p></div>
  <div class="card rv d2"><h3>更好的插件预览</h3><p>插件市场的详情页能预览更多内容，装之前看得更清楚。</p></div>
 </div>
</div></section>

<section class="sect tint" id="relation"><div class="wrap rel">
 <div class="txt rv">
  <div class="sect-head" style="margin-bottom:22px"><h2>和 ClassIsland<br>是什么关系</h2></div>
  <p>ClassFabric 是在 ClassIsland 基础上做的个人修改版，不是它的替代品，也不是竞品。我们一直在同步上游的更新，同时加入来自社区和我们自己的改动。</p>
  <p>从 ClassIsland 切换过来很简单：不用重新配置，下载安装之后，原来的课表、自动化、插件和主题接着就能用。</p>
  <a class="tl" href="/about.html">了解更多 →</a>
 </div>
 <div class="fit rv d1">
  <div><h4>适合你，如果……</h4><p>你想比上游更早用到新功能；或者希望装完就能直接用上上游、社区和我们做的各种新功能。</p></div>
  <div class="no"><h4>可能不适合，如果……</h4><p>你想要一个长期不变的稳定环境，或者场合对稳定性要求极高。因为我们会积极跟进上游的改动。</p></div>
 </div>
</div></section>

<section class="sect" id="join"><div class="wrap rel">
 <div class="sect-head rv" style="margin:0"><h2>一起把它<br>做得更好</h2></div>
 <div class="txt rv d1">
  <p>欢迎在 GitHub 上提 Issue 或 PR。有价值的改动，我们也会考虑定期提交回上游，帮 ClassIsland 生态一起变好。</p>
  <p>名字里的 Fabric，取自 Minecraft 的模组加载器 Fabric，意思是把社区和个人的功能连起来；就像 ClassIsland 的 Island，来自 iOS 的灵动岛。</p>
  <div class="cta" style="margin-top:22px"><a class="btn ghost" href="%(gh)s" rel="noopener">@@gh@@GitHub 仓库</a><a class="btn ghost" href="%(gh)s/issues" rel="noopener">反馈问题</a></div>
 </div>
</div></section>

<section class="final"><div class="wrap">
 <h2 class="rv">立即试用 ClassFabric。</h2>
 <div class="cta rv d1"><a class="btn primary" href="/download.html">@@dl@@下载 Windows 版</a><a class="btn ghost" href="%(gh)s" rel="noopener">@@gh@@在 GitHub 查看</a></div>
</div></section>
</main>
''' % dict(gh=GH)
    return h + FOOT

# ---------------- download ----------------
def download():
    h = head('下载 ClassFabric — Windows 版', '下载 ClassFabric，ClassIsland 的个人修改版班级大屏课表。支持 Windows 10 及更高版本，免费开源。', '/download.html')
    h += nav('dl')
    h += '''<main><div class="wrap">
 <div class="dl-head rv"><h1>下载 ClassFabric</h1><p>目前提供 Windows 版本。</p></div>
 <div class="dl-grid">
  <div class="dl-card main rv">
   <div class="dl-os">@@win@@<h2>Windows</h2></div>
   <p class="dl-sub">Windows 10 及更高版本</p>
   <div class="ver"><span>最新版本 <code data-ver>读取中…</code></span><span>发布于 <span data-date>—</span></span></div>
   <div class="cta"><a class="btn primary" href="%(rel)s" data-dl data-releaselink rel="noopener">@@dl@@下载最新版</a><a class="btn ghost" href="%(gh)s/releases" rel="noopener">全部版本</a></div>
   <div class="assets" id="assets"><div class="none">正在读取版本信息…</div></div>
   <ol class="steps">
    <li><span><b>下载</b>　选择上面的文件，保存到本地。</span></li>
    <li><span><b>运行</b>　按文件类型安装或解压后启动，主界面会出现在屏幕上方。</span></li>
    <li><span><b>接着用</b>　如果之前用过 ClassIsland，原来的课表、自动化、插件和主题可以直接沿用。</span></li>
   </ol>
  </div>
  <div class="dl-side">
   <div class="dl-card rv d1"><h3>Linux 与 macOS</h3><p>代码里保留了相关支持，但我们没有测试环境，暂时不提供官方构建。想用的话可以从源码自行构建，也欢迎帮忙测试。</p></div>
   <div class="dl-card rv d2"><h3>更新与反馈</h3><p>新版本都发布在 GitHub Releases。遇到问题或有想法，欢迎提 Issue。</p><div class="cta" style="margin-top:18px"><a class="btn ghost sm" href="%(gh)s/issues" rel="noopener">@@gh@@反馈问题</a><a class="btn ghost sm" href="/about.html">了解 ClassFabric</a></div></div>
  </div>
 </div>
 <div style="height:clamp(60px,9vw,120px)"></div>
</div></main>
''' % dict(rel=REL, gh=GH)
    return h + FOOT

# ---------------- about ----------------
def about():
    h = head('关于 ClassFabric — 与 ClassIsland 的关系、计划与常见问题',
             'ClassFabric 是 ClassIsland 的个人修改版。了解它和上游的关系、从 ClassIsland 切换要做什么、已完成与计划中的功能，以及常见问题。', '/about.html')
    h += nav('about')
    h += '''<main>
<div class="wrap">
 <div class="ab-head rv"><h1>关于 ClassFabric</h1><p>它是什么，和 ClassIsland 是什么关系，现在做了什么，接下来想做什么。</p></div>
 <div class="ab">
  <nav class="toc" aria-label="本页目录"><a href="#what">是什么</a><a href="#relation">和 ClassIsland 的关系</a><a href="#switch">如何切换</a><a href="#fit">适合谁</a><a href="#done">已经做了</a><a href="#planned">计划中</a><a href="#name">名字由来</a><a href="#join">参与贡献</a><a href="#faq">常见问题</a></nav>
  <div class="prose">
   <section id="what"><h2>ClassFabric 是什么</h2>
    <p>ClassFabric 是基于 HelloWRC 的 ClassIsland 二次开发的<strong>个人修改版</strong>。我们一边积极同步上游的最新特性，一边加入来自个人和社区的修改，比如多语言、云功能、更好的自动化、更好的性能和更多功能。</p>
    <p>其中有些已经做好，有些还在规划中，具体见下面的“已经做了”和“计划中”。</p></section>
   <section id="relation"><h2>和 ClassIsland 的关系</h2>
    <p>ClassFabric 不是 ClassIsland 的完美替代品，也不是它的竞品。它是在 ClassIsland 基础上的二次开发，就像不少下游项目和原版之间的关系：在原项目的基础上继续做自己的事，同时尊重和感谢上游。</p>
    <p>ClassIsland 的作者是 HelloWRC。ClassFabric 沿用上游的开源协议（GPL-3.0），软件的“关于”页里也保留了上游的版权声明。</p></section>
   <section id="switch"><h2>从 ClassIsland 切换，要做什么</h2>
    <p>不需要复杂的前期工作。ClassFabric 的底层代码与上游保持一致，你只需要下载安装，原来的课表、自动化、插件和主题就能接着用。</p>
    <div class="callout">我们正在把底层代码尽量还原到与上游一致，同时让界面里显示的名字仍然是 ClassFabric，目的就是让切换对你“无感”。</div></section>
   <section id="fit"><h2>适合谁，不适合谁</h2>
    <p><strong>适合：</strong>想在 ClassIsland 生态里保持现有内容，又想及时体验上游新功能的人；也适合想“开箱即用”，装完就能直接用上上游、社区和我们做的各种新功能的人。</p>
    <p><strong>不太适合：</strong>希望环境长期一成不变的人，或者对稳定性有极高要求的场合。因为 ClassFabric 会积极同步上游的改动，版本变化会比较勤。</p></section>
   <section id="done"><h2>已经做了什么</h2>
    <ul>
     <li><strong>紧跟上游</strong>：同步 ClassIsland 的新功能和修复。</li>
     <li><strong>更多天气源</strong>：除小米天气外，增加 OpenWeather 和和风天气。</li>
     <li><strong>多语言（实验中）</strong>：ClassIsland 的界面文字原本是写死的，我们已经把大部分改成可翻译的形式，目前支持简体中文、繁体中文和 English，约完成 40%%。还有不少写死的文字和界面适配没做完，欢迎在 Crowdin 上帮忙翻译。</li>
     <li><strong>更好的插件预览</strong>：插件市场的详情页可以预览更多内容。</li>
    </ul>
    <p>想看具体改了什么，可以在 <a href="%(gh)s/commits/main" rel="noopener">GitHub 提交记录</a>里查看。</p></section>
   <section id="planned"><h2>计划中</h2>
    <p>下面这些还在规划阶段，<strong>并不代表已经可用</strong>。</p>
    <div class="plan">
     <div><h4>云功能 · 远程提醒</h4><p>从远端向大屏发送提醒。</p></div>
     <div><h4>云功能 · 集中管理</h4><p>统一管理多台设备。上游暂时没有做，社区项目 <a href="https://github.com/1sIancl/ClassislandControlHub" rel="noopener">ClassislandControlHub</a> 正在积极开发。</p></div>
     <div><h4>云功能 · 云端备份</h4><p>通过 SFTP、WebDAV、OpenList 等方式备份档案和配置。</p></div>
     <div><h4>更好的自动化</h4><p>主要借助社区知名插件 SystemTools 来实现。</p></div>
     <div><h4>更好的性能表现</h4><p>持续优化。</p></div>
    </div></section>
   <section id="name"><h2>名字由来</h2>
    <p>ClassIsland 的 Island，来自 iOS 的“灵动岛”。ClassFabric 的 Fabric，则来自 Minecraft 社区知名的模组加载器 Fabric，寓意把社区和个人的功能连接起来。</p></section>
   <section id="join"><h2>参与贡献</h2>
    <p>欢迎任何有价值的贡献：在 GitHub 提 Issue 或 PR 就可以。我们也会考虑定期把有意义的改动提交给上游，一起建设 ClassIsland 生态。</p>
    <div class="cta"><a class="btn ghost" href="%(gh)s" rel="noopener">@@gh@@GitHub 仓库</a><a class="btn ghost" href="%(gh)s/issues" rel="noopener">反馈问题</a></div></section>
   <section id="faq" class="faq"><h2>常见问题</h2>
    <details><summary>支持 Linux 和 macOS 吗？</summary><p>目前只提供 Windows 版本。代码里保留了相关支持，但我们没有测试环境，也没有足够精力维护，所以暂不提供官方构建。</p></details>
    <details><summary>有交流群吗？</summary><p>暂时没有。ClassIsland 现有的 QQ 频道和群属于上游项目，ClassFabric 的问题请直接在 GitHub 上提 Issue。</p></details>
    <details><summary>软件出问题了怎么办？</summary><p>先试试内置的恢复模式：可以用安全模式启动、查看日志、恢复备份，必要时再重置配置。仍然解决不了，请到 GitHub 提 Issue，并附上诊断信息。</p></details>
    <details><summary>它会取代 ClassIsland 吗？</summary><p>不会。ClassFabric 建立在 ClassIsland 之上，没有上游就没有它。你可以把它当作“更早体验新功能、再多一点功能”的选择。</p></details>
    <details><summary>开源协议是什么？</summary><p>GPL-3.0，与上游一致。ClassIsland 的版权归 HelloWRC，ClassFabric 的改动版权归各自贡献者。</p></details>
   </section>
  </div>
 </div>
</div></main>
''' % dict(gh=GH)
    return h + FOOT

def finish(html):
    for k, v in IC.items():
        html = html.replace('@@%s@@' % k, v)
    assert '@@' not in html, re.findall(r'@@\w+@@', html)
    return html

for name, fn in (('index.html', index), ('download.html', download), ('about.html', about)):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(finish(fn()))
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>%s%s</loc></url>\n' % (SITE, p) for p in ('/', '/download.html', '/about.html')) + '</urlset>\n')
print('ok')
