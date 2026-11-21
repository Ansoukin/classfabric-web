# -*- coding: utf-8 -*-
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ui2
import ui3 as U3
import ui4 as U4
from ui import *

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://cf.ansoukin.top'
GH = 'https://github.com/Ansoukin/ClassFabric'
REL = GH + '/releases/latest'

GHSVG = '<svg class="ghi" viewBox="0 0 16 16" fill="currentColor" stroke="none"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'

def svg_(n, extra=''):
    return ic(n, extra)

def idle(kind, p0, p1, ms, g=None):
    wx = '<span class="wx">%s9℃</span><span class="idt">周四 10/29</span>' % ic('sun')
    past = ''.join('<span class="s p">%s</span>' % c for c in '语数英')
    if kind == 'break':
        cur = '<span class="cur">%s<span>课间休息</span><small>10:00-10:30</small></span>' % ic('clock')
        fut = ''.join('<span class="s">%s</span>' % c for c in '物化生政历地自自')
    else:
        cur = '<span class="cur">%s<span>物理</span><span class="pill">-39m</span></span>' % ic('atom')
        fut = ''.join('<span class="s">%s</span>' % c for c in '化生政历地自自')
    r0 = float(str(p0).rstrip('%')) / float(str(p1).rstrip('%'))
    return '<div class="isl"%s data-ms="%d" style="--dur:%.1fs;--p0:%s;--p1:%s;--r0:%.4f">%s%s%s<span class="sep"></span>%s</div>' % (
        (' data-g="%d"' % g) if g is not None else '', ms, ms / 1000, p0, p1, r0, wx, past, cur, fut)

def mask(label, icon, ms=2300, g=None):
    return '<div class="isl mask"%s data-ms="%d">%s<span>%s</span>%s</div>' % ((' data-g="%d"' % g) if g is not None else '', ms, ic('info'), label, ic(icon))

def bar_text(txt, ms=3400, g=None):
    return '<div class="isl bar"%s data-ms="%d" style="--dur:%.1fs">%s</div>' % ((' data-g="%d"' % g) if g is not None else '', ms, ms / 1000, txt)

def bar_two(left, ms=2800, g=None):
    return ('<div class="isl bar two"%s data-ms="%d" style="--dur:%.1fs"><span>%s</span><span class="nx">下节课是: <em>物理</em><small>10:30-11:10</small></span></div>' % (
        (' data-g="%d"' % g) if g is not None else '', ms, ms / 1000, left))

HERO_STATES = idle('break', '56%', '78%', 4600) + bar_two('距上课还剩 <b>16</b> 秒', 2800) + mask('即将上课', 'atom') + bar_text('准备上课，请回到座位并保持安静，做好上课准备。', 3400) + mask('上课', 'atom') + idle('class', '2%', '14%', 4600)

REM_STATES = (bar_text('准备上课，请回到座位并保持安静，做好上课准备。', 3200, 0) + bar_two('距上课还剩 <b>16</b> 秒', 2800, 0) + mask('即将上课', 'atom', 2400, 0) +
              mask('上课', 'atom', 2400, 1) + idle('class', '2%', '14%', 3400, 1) +
              mask('课间休息', 'clock', 2400, 2) + bar_two('本节课间休息长 <b>10</b> 分钟', 2800, 2) + idle('break', '56%', '78%', 3400, 2))

def fit(inner, dw, style='', dwm=None, cls='', extra=''):
    return '<div class="fitbox %s" data-dw="%d"%s style="%s"%s><div class="fit" style="width:%dpx">%s</div></div>' % (
        cls, dw, (' data-dwm="%d"' % dwm) if dwm else '', style, extra, dw, inner)

def vtask(running=False):
    def W(n, w):
        return '<img src="/assets/img/win/%s.png" alt="" width="%d" height="%d" style="width:%dpx;height:auto" draggable="false" loading="lazy" decoding="async">' % (n, w, w, w)
    tb = ''.join('<span class="tb%s">%s</span>' % (' on0' if n == 'start' else '', W(n, w)) for n, w in
                 [('start', 24), ('search', 22), ('taskview', 24), ('widgets', 24), ('chat', 24), ('explorer', 24), ('edge', 24), ('store', 23)])
    cf = '<img src="/assets/img/icon-64.png" alt="" width="24" height="24" style="width:24px;height:auto" draggable="false" loading="lazy" decoding="async">'
    return ('<div class="vtask"><div class="vtb">' + tb + '<span class="tb cfapp' + (' on' if running else ' run') + '">' + cf + '</span></div>'
            '<div class="vtray"><span class="tg2 hide">' + W('chev', 12) + '</span><span class="tg2 ime">英</span>'
            '<span class="tg2 ctray" id="%s" title="ClassFabric"><img src="/assets/img/icon-64.png" alt=""></span>'
            '<span class="sys">' + W('sys', 40) + '</span><span class="clk" data-clock>10:12<br>2026/11/2</span><span class="tg2 ntf">' + W('moon', 13) + '</span></div></div>')

def vdesk(inner, cls, w=1280, h=720, mw=680, mh=780, extra='', tray_id='vTray'):
    return ('<div class="vdk %s" data-vd data-w="%d" data-h="%d" data-mw="%d" data-mh="%d"%s><div class="vdks">%s%s</div></div>' % (cls, w, h, mw, mh, extra, inner, vtask(False).replace('%s', tray_id, 1)))

def static_isl(h, w='50%'):
    return h.replace('class="isl bar', 'class="isl static bar').replace('<div class="isl"', '<div class="isl static"').replace('<div class="isl mask', '<div class="isl static mask')

def _fin(h, m, path='/'):
    if m:
        from mobile import JS_REDIR_M
        h = h.replace('width=device-width,initial-scale=1', 'width=device-width,initial-scale=1,viewport-fit=cover', 1)
        h = h.replace('<meta name="viewport"', JS_REDIR_M + '<meta name="viewport"', 1)
        h = h.replace('<link rel="stylesheet" href="/assets/css/base.css">\n', '<link rel="stylesheet" href="/assets/css/base.css">\n<link rel="stylesheet" href="/assets/css/m.css">\n', 1)   # m.css 必须在 base.css 之后，才能覆盖共用部件
    elif path == '/':
        h = h.replace('<meta name="viewport"', JS_REDIR_D + '<meta name="viewport"', 1)
    return h

def jsonld(path, title, desc):
    import json
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "ClassFabric", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/icon-192.png", "width": 192, "height": 192}, "sameAs": [GH]}
    web = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "ClassFabric", "alternateName": ["ClassFabric 官网", "ClassIsland 个人修改版"], "inLanguage": "zh-CN", "publisher": {"@id": SITE + "/#org"}}
    app = {"@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "ClassFabric", "alternateName": "ClassIsland 个人修改版", "applicationCategory": "EducationalApplication", "operatingSystem": "Windows 10, Windows 11",
           "description": "ClassIsland 的个人修改版班级大屏课表，紧跟上游更新，原有课表、插件与主题可直接沿用。", "url": SITE + "/", "downloadUrl": SITE + "/download.html", "installUrl": SITE + "/download.html",
           "license": "https://www.gnu.org/licenses/gpl-3.0.html", "isBasedOn": {"@type": "SoftwareApplication", "name": "ClassIsland", "url": "https://classisland.tech"}, "image": SITE + "/assets/img/og.jpg",
           "featureList": ["课表编辑与调课", "自动化行为", "插件生态", "主题与主界面自定义", "更多天气源", "多语言（实验中）"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CNY"}, "publisher": {"@id": SITE + "/#org"}}
    names = [('/', '首页', 'ClassFabric 首页：紧跟上游的 ClassIsland 班级大屏课表'), ('/download.html', '下载', '下载 ClassFabric Windows 版'), ('/about.html', '关于', '了解 ClassFabric 与 ClassIsland 的关系、已完成与计划中的功能')]
    nav = [{"@type": "SiteNavigationElement", "@id": SITE + "/#nav-%d" % i, "name": n, "description": d, "url": SITE + p} for i, (p, n, d) in enumerate(names)]
    kind = {'/': 'WebPage', '/download.html': 'WebPage', '/about.html': 'AboutPage'}.get(path, 'WebPage')
    page = {"@type": kind, "@id": SITE + path + "#page", "url": SITE + path, "name": title, "description": desc, "inLanguage": "zh-CN", "isPartOf": {"@id": SITE + "/#website"}, "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/assets/img/og.jpg", "width": 1200, "height": 630}, "about": {"@id": SITE + "/#app"}}
    g = [org, web, app] + nav + [page] if path == '/' else [page]
    if path != '/':
        g.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "首页", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": dict((p, n) for p, n, d in names)[path], "item": SITE + path}]})
        page["breadcrumb"] = {"@id": SITE + path + "#crumb"}; g[-1]["@id"] = SITE + path + "#crumb"
    if path == '/about.html':
        g.append({"@type": "FAQPage", "@id": SITE + path + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    if path == '/download.html':
        g.append({"@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "ClassFabric", "operatingSystem": "Windows 10, Windows 11", "applicationCategory": "EducationalApplication", "downloadUrl": SITE + "/download.html", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CNY"}})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, separators=(',', ':')) + '</script>\n'

JS_REDIR_D = ('<script>(function(){try{var u=navigator.userAgent,s=location.search,k="cf_view";if(/[?&]view=pc\\b/.test(s))localStorage.setItem(k,"pc");else if(/[?&]view=m\\b/.test(s))localStorage.setItem(k,"m");'
              'var v=localStorage.getItem(k),ph=/iPhone|iPod|Android.+Mobile|Windows Phone|IEMobile|BlackBerry|Opera Mini|Mobile.+Firefox/i.test(u);'
              'if(v==="m"||(ph&&v!=="pc")){var p=location.pathname;location.replace((p==="/"||p==="/index.html"?"/m/":"/m"+p)+location.hash)}}catch(e){}})()</script>\n')

def wp_early(flags):
    js = open(os.path.join(OUT, 'assets/js/wp.js'), encoding='utf-8').read()
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.S)
    return '<script>' + flags + re.sub(r'\s*\n\s*', ' ', js).strip() + '</script>\n'

def head(title, desc, path, extra='', alt=None, m=False):
    url = SITE + path
    alt_tag = ('<link rel="alternate" media="only screen and (max-width: 640px)" href="%s%s">\n' % (SITE, alt)) if alt else ''
    out = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n<link rel="canonical" href="%s">\n'
            '<link rel="alternate" hreflang="zh-CN" href="%s">\n<link rel="alternate" hreflang="x-default" href="%s">\n%s<meta name="application-name" content="ClassFabric">\n<meta name="theme-color" content="#f4f6fb" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#141312" media="(prefers-color-scheme: dark)">\n'
            '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icon-192.png">\n<link rel="apple-touch-icon" href="/assets/img/icon-180.png">\n'
            '<meta property="og:type" content="website">\n<meta property="og:locale" content="zh_CN">\n<meta property="og:site_name" content="ClassFabric">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n<meta property="og:image" content="%s/assets/img/og.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="ClassFabric 班级大屏课表">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n<meta name="twitter:image" content="%s/assets/img/og.jpg">\n'
            '<meta name="color-scheme" content="dark light">\n<script>document.documentElement.classList.add("js");try{var t=localStorage.getItem("cf_theme");if(t!=="light"&&t!=="dark")t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.dataset.theme=t}catch(e){}</script>\n<link rel="stylesheet" href="/assets/css/site.css">\n<link rel="stylesheet" href="/assets/css/tokens.css">\n<link rel="stylesheet" href="/assets/css/materials.css">\n<link rel="stylesheet" href="/assets/css/nav.css">\n<link rel="stylesheet" href="/assets/css/base.css">\n%s%s</head>\n') % (
        title, desc, url, url, url, alt_tag, title, desc, url, SITE, title, desc, SITE, (jsonld(path, title, desc) if path != '/404.html' else ''), extra)
    wpf = 'window.cfWpPre=2;' if path == '/download.html' else (('window.cfWpS=1;window.cfWpPre=1;' if m else 'window.cfWpPre=1;') if path == '/' else None)
    if wpf is not None:
        css = '<link rel="stylesheet" href="/assets/css/site.css">'
        out = out.replace(css, wp_early(wpf) + css, 1)
    spec = {'/': ['/download.html', '/about.html'], '/download.html': ['/', '/about.html'], '/about.html': ['/', '/download.html']}.get(path)
    if spec and not m:
        out = out.replace('</head>', '<script type="speculationrules">' + __import__('json').dumps({"prefetch": [{"source": "list", "urls": spec}]}, separators=(',', ':')) + '</script>\n</head>', 1)
    return _fin(out, m, path)

def navbar(cur, secs=None):
    def a(href, label, key):
        return '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if cur == key else '', label)
    moon = '<svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 019.5 4 8.5 8.5 0 1020 14.5z"/></svg>'
    sun = '<svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
    return ('<body>\n<a class="skip" href="#main">跳到正文</a>\n<header class="nav" id="nav"><div class="wrap"><a class="brand" href="/"><img src="/assets/img/icon-64.png" width="26" height="26" alt="">ClassFabric</a>'
            '<nav class="links" id="links" aria-label="主导航">' + a('/', '首页', 'home') + a('/download.html', '下载', 'dl') + a('/about.html', '关于', 'about') + '<a class="ghl" href="' + GH + '" rel="noopener">' + GHSVG + 'GitHub 仓库</a>'
            '<a class="btn blue nav-cta" href="/download.html">' + ic('dl') + '立即下载</a></nav>'
            + ('<nav class="slinks" aria-label="页面章节">' + ''.join('<a href="#%s">%s</a>' % (i, l) for i, l in secs) + '</nav>' if secs else '')
            + '<div class="tools"><button type="button" class="ibtn" id="theme" aria-label="切换主题">' + moon + sun + '</button>'
            '<a class="btn blue sm" href="/download.html">' + ic('dl') + '立即下载</a>'
            '<button type="button" class="ibtn menu-btn" id="menu" aria-label="打开菜单" aria-expanded="false" aria-controls="links"><svg class="i-open" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="i-close" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div></div></header>\n')

import hashlib, datetime

SITE_VER = '1.0.9'
RELEASE_DATE = '2026-11-21'

def build_id():
    h = hashlib.sha1()
    for f in ('assets/css/site.css', 'assets/css/tokens.css', 'assets/css/materials.css', 'assets/css/nav.css', 'assets/css/base.css', 'assets/css/m.css', 'assets/js/site.js', 'assets/js/apps.js', 'assets/js/widgets.js', 'assets/js/dl.js', 'assets/js/fx.js', 'assets/js/m.js', 'assets/js/home.js', 'assets/css/home2.css', 'assets/css/bento.css', 'assets/css/display.css', 'assets/js/bento.js', 'assets/css/tokens.css', 'assets/css/modal.css', 'assets/css/dl.css', 'assets/css/about.css', 'assets/js/about.js', 'assets/js/wp.js', 'assets/css/nf.css', 'assets/js/nf.js'):
        h.update(open(os.path.join(OUT, f), 'rb').read())
    return RELEASE_DATE.replace('-', ''), h.hexdigest()[:7], RELEASE_DATE

BD, BH, BT = build_id()

def levels(h):
    """标题层级不跳级（WCAG 1.3.1 / 2.4.6）：版面用的 h4 直接跟在 h2 后面时，给它补 aria-level（父级 +1），样式不受影响。
    软件界面复刻里的标题已是 role=presentation，不参与。"""
    st = []   # (原始层级, 有效层级)
    def f(m):
        n = int(m.group(1)); attrs = m.group(2)
        if 'role=' in attrs or 'aria-level' in attrs: return m.group(0)
        while st and st[-1][0] >= n: st.pop()
        eff = min(n, (st[-1][1] if st else 0) + 1)
        st.append((n, eff))
        return m.group(0) if eff == n else '<h%d%s role="heading" aria-level="%d">' % (n, attrs, eff)
    return re.sub(r'<h([1-6])((?:\s[^>]*)?)>', f, h)

def vers(h):
    """给 CSS/JS 引用加 ?v=内容哈希：文件一变 URL 就变，Cloudflare 与浏览器缓存不会再返回旧版本"""
    return re.sub(r'((?:href|src)="/assets/(?:css|js)/[\w.-]+\.(?:css|js))"', r'\1?v=' + BH + '"', h)
BUILD = ('<div class="bld" title="V%s 发布于 %s"><span class="dot"></span><span>站点版本 v%s</span><i></i><span>Build %s</span><i></i><code>%s</code></div>' % (SITE_VER, BT, SITE_VER, BD, BH))

FOOT = ('<footer class="foot"><div class="wrap"><div class="cols"><div><a class="brand" href="/"><img src="/assets/img/icon-64.png" width="26" height="26" alt="">ClassFabric</a>'
        '<p class="about">ClassIsland 的个人修改版班级大屏课表。紧跟上游，并加入来自社区与我们的改进。</p></div>'
        '<div><h2 class="fh">产品</h2><ul><li><a href="/download.html">下载</a></li><li><a href="' + GH + '/releases" rel="noopener">版本发布</a></li><li><a href="/about.html#planned">计划中的功能</a></li></ul></div>'
        '<div><h2 class="fh">项目</h2><ul><li><a href="' + GH + '" rel="noopener">GitHub 仓库</a></li><li><a href="' + GH + '/issues" rel="noopener">反馈问题</a></li><li><a href="/about.html#join">参与贡献</a></li></ul></div>'
        '<div><h2 class="fh">了解更多</h2><ul><li><a href="/about.html">关于 ClassFabric</a></li><li><a href="/about.html#faq">常见问题</a></li><li><a href="https://classisland.tech" rel="noopener">ClassIsland 官网</a></li></ul></div></div>'
        '<div class="legal">© 2026 ClassFabric　基于 HelloWRC 的 ClassIsland（© 2023–2026 HelloWRC）二次开发，以 GPL-3.0 协议开源。<br>ClassFabric 是个人修改版，并非 ClassIsland 官方项目；ClassIsland 的名称与原有功能归其原作者所有。</div>' + BUILD + '</div><div class="foot-mark" aria-hidden="true">ClassFabric</div></footer>\n'
        '<script src="/assets/js/site.js" defer></script>\n<script src="/assets/js/apps.js" defer></script>\n<script src="/assets/js/widgets.js" defer></script>\n<script src="/assets/js/dl.js" defer></script>\n<script src="/assets/js/fx.js" defer></script>\n</body>\n</html>\n')

FOOT_LITE = FOOT.replace('<script src="/assets/js/apps.js" defer></script>\n', '').replace('<script src="/assets/js/widgets.js" defer></script>\n', '')  # 下载/关于页没有演示控件，不加载其脚本
FOOT_M = (FOOT.replace('<script src="/assets/js/apps.js" defer></script>\n', '').replace('<script src="/assets/js/fx.js" defer></script>', '<script src="/assets/js/fx.js" defer></script>\n<script src="/assets/js/bento.js" defer></script>').replace('<script src="/assets/js/widgets.js" defer></script>\n', '<script src="/assets/js/m.js" defer></script>\n')
          .replace('<div class="bld"', '<p class="pcl"><a href="/?view=pc">查看电脑版网页</a></p><div class="bld"', 1))

def ld():
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"ClassFabric","applicationCategory":"EducationApplication","operatingSystem":"Windows 10, Windows 11",'
            '"description":"ClassIsland 的个人修改版班级大屏课表，紧跟上游更新，原有课表、插件与主题可直接沿用。","url":"%s/","license":"https://www.gnu.org/licenses/gpl-3.0.html","isBasedOn":"https://classisland.tech","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}</script>\n') % SITE

PLUGINS = [
    ('ExtraIsland', 'LiPolymer/ExtraIsland', 'LiPolymer/ExtraIsland@master/ExtraIsland/icon.png', '为 ClassIsland 提供多种扩展功能！'),
    ('地震预警', 'denglihong2007/EarthquakeWarningForClassIsLand', 'denglihong2007/EarthquakeWarningForClassIsLand@master/EarthquakeWarning/icon.png', '防范于未然，争取宝贵的避险时间'),
    ('SystemTools', 'Programmer-MrWang/SystemTools', 'Programmer-MrWang/SystemTools@main/icon.png', '提供多彩而丰富的更多 行动/触发器/实用工具'),
    ('MediaIsland', 'bywhite0/MediaIsland', 'bywhite0/MediaIsland@master/MediaIsland/icon.png', '在 ClassIsland 显示 SMTC 媒体信息。'),
    ('DutyIsland', 'lrsgzs/DutyIsland', 'lrsgzs/DutyIsland@master/DutyIsland/icon.png', '给 ClassIsland 加上值日表。'),
    ('MonitorIsland', 'LiuYan-xwx/MonitorIsland', 'LiuYan-xwx/MonitorIsland@master/MonitorIsland/icon.png', '在主界面实时监控系统硬件资源使用状态'),
    ('以管理员身份自启动', 'ClassIsland/StartUpAsAdmin', 'ClassIsland/StartUpAsAdmin@master/icon.ico', '通过计划任务，让 ClassIsland 在开机时以管理员身份自启动。'),
    ('SuperAutoIsland', 'lrsgzs/SuperAutoIsland', 'lrsgzs/SuperAutoIsland@master/SuperAutoIsland/icon.png', '自动化进化'),
    ('UIAccess 提权', 'HelloWRC/GrantUiAccess', 'HelloWRC/GrantUiAccess@master/GrantUiAccess/icon.png', '为 ClassIsland 提升 UIAccess 令牌，使其可以置顶到全屏 UWP 应用和系统界面上。'),
]

def panel_wall(inner, wx='50%', wy='50%', ws='170%', cls='pad'):
    return '<div class="panel %s" style="--wx:%s;--wy:%s;--ws:%s"><div class="wp"></div><div style="position:relative">%s</div></div>' % (cls, wx, wy, ws, inner)

def home(mob=False):
    import mobile as M
    M.init(globals())
    h = head('ClassFabric — 紧跟上游的 ClassIsland 班级大屏课表',
             'ClassFabric 是基于 ClassIsland 的个人修改版班级大屏课表：积极同步上游特性，原有课表、自动化、插件与主题无缝沿用，并加入更多天气源、多语言等改进。', '/', '<link rel="preconnect" href="https://api.github.com" crossorigin>\n<link rel="stylesheet" href="/assets/css/bento.css">\n<link rel="stylesheet" href="/assets/css/display.css">\n' if mob else '<link rel="stylesheet" href="/assets/css/home2.css">\n<link rel="stylesheet" href="/assets/css/bento.css">\n<link rel="stylesheet" href="/assets/css/display.css">\n<link rel="preconnect" href="https://api.github.com" crossorigin>\n<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">\n', None if mob else '/m/', m=mob)
    h += navbar('home', [('features','功能'),('custom','定制'),('grow','增强'),('start','开始使用'),('faqs','常见问题')])
    h += '<main id="main" tabindex="-1">\n'
    U3.init(globals())
    h += U3.hero(mob)

    if mob:
        h += ('<section class="axstrip"><div class="wrap"><div class="axgrid four">' + ''.join('<div class="axc rv d%d"><div><b>%s</b></div></div>' % (k, t) for k, t in enumerate(['紧跟上游', '无缝沿用', '社区增强', '开源免费'])) + '</div></div></section>\n')
    h += '<section class="mani"><div class="wrap"><p class="mtxt" id="mtxt">' + ''.join('<span class="mw">%s</span>' % c for c in "积极同步上游。无缝沿用配置。再多一点点，属于我们自己的增强。") + '</p></div></section>\n'
    def bigmq(a, b):
        r1 = ''.join('<span>%s</span><i>·</i>' % t for t in a) * 3
        r2 = ''.join('<span>%s</span><i>·</i>' % t for t in b) * 3
        return '<div class="bigmq" aria-hidden="true"><div class="r1"><div class="t">' + r1 + '</div></div><div class="r2"><div class="t">' + r2 + '</div></div></div>\n'
    def fc(icn, t, d='', trail='', bd=None):
        return '<div class="fcard">%s<div class="tx"><b>%s%s</b>%s</div>%s</div>' % (ic(icn), t, (U3.bdg(bd[0], bd[1], None, 'sm')) if bd else '', ('<span>%s</span>' % d) if d else '', trail)
    ok = '<span class="ok">' + ic('check') + '已同步</span>'
    used = '<span class="ok">' + ic('check') + '已沿用</span>'
    on = '<span class="tg on"><i></i></span>'
    c_sync = fc('sync', '新功能', '', ok) + fc('bolt', '问题修复', '', ok) + fc('info', '上游版本', '', ok)
    c_mig = fc('cal', '课表与档案', '', used) + fc('bolt', '自动化', '', used) + fc('plug', '插件', '', used) + fc('brush', '主题', '', used)
    c_enh = fc('cloud', '更多天气源', '小米天气 · OpenWeather · 和风天气', on) + fc('text', '多语言', '实验中', on) + fc('plug', '更好的插件预览', '', on) + fc('sync', '持续同步上游', '', on)
    if mob:
        h += ('<section class="sec" id="features"><div class="wrap"><h2 class="claim rv">一款<span class="g">紧跟上游</span>的大屏课表软件</h2><div class="grid3">'
              '<div class="copy rv"><h3>积极同步上游特性</h3><p>ClassIsland 的新功能与修复，会尽快同步到 ClassFabric。</p><div class="fstack">' + c_sync + '</div></div>'
              '<div class="copy rv d1"><h3>无感切换，沿用现有配置</h3><p>底层代码与上游保持一致。原有的课表、自动化、插件与主题，安装后即可继续使用。</p><div class="fstack">' + c_mig + '</div></div>'
              '<div class="copy rv d2"><h3>来自社区与我们的增强</h3><p>在上游之上加入更多天气源、多语言支持（实验中）与更好的插件预览，并将持续扩充。</p><div class="fstack">' + c_enh + '</div></div>'
              '</div></div></section>\n')

    else:
        U4.init(dict(globals(), **locals()))
        h += U4.sync(c_sync, c_mig, c_enh, panel_wall)

    def sidle(past, cur, fut):
        return '<div class="isl static on"><span class="pa">%s</span>%s<span class="sep"></span><span class="fu">%s</span></div>' % (''.join('<span class="s p">%s</span>' % c for c in past), cur, ''.join('<span class="s">%s</span>' % c for c in fut))
    def sbar2(l, ms=''):
        return '<div class="isl static on bar two"><span>%s</span><span class="nx">下节课是: <em>物理</em><small>10:30-11:10</small></span></div>' % l
    def smask(t, icn):
        return '<div class="isl static on mask">%s<span>%s</span>%s</div>' % (ic('info'), t, ic(icn))
    ST = [sbar2('距上课还剩 <b data-cd2="48">48</b> 秒'),
          '<div class="isl static on bar">准备上课，请回到座位并保持安静，做好上课准备。</div>',
          smask('上课', 'atom'),
          sidle('语数英', '<span class="cur">' + ic('clock') + '<span>课间休息</span><small>10:20-10:30</small></span>', '物化生历政地'),
          smask('即将上课', 'atom'),
          sidle('语数', '<span class="cur">' + ic('text') + '<span>英语</span><span class="pill" data-cd2="31" data-fmt="-{n}s">-31s</span></span>', '物化生历政地'),
          smask('课间休息', 'clock'),
          sbar2('本节课间休息长 <b>10</b> 分钟')]
    wrapi = lambda x: '<div class="mq-i"><div class="isl-stack">' + x + '</div></div>'
    row1 = ''.join(wrapi(x) for x in (ST[0], ST[1], ST[2], ST[3]))
    row2 = ''.join(wrapi(x) for x in (ST[4], ST[5], ST[6], ST[7]))
    if mob:
        h += ('<section class="sec show"><div class="wrap"><h2 class="claim rv">上课与下课，<span class="g">一目了然</span></h2></div>'
              '<div class="marq rv" aria-label="灵动岛的各种状态"><div class="row"><div class="trk">' + row1 * 2 + '</div></div><div class="row rev"><div class="trk">' + row2 * 2 + '</div></div></div>'
              + ('' if mob else '<div class="wrap"><figure class="vid rv" id="vid"><video muted loop playsinline preload="none" data-src="https://www.classisland.tech/assets/notification-demo.web-Os7FSQPD.mp4" aria-label="提醒演示视频"></video></figure></div>') + '</section>\n')
    else:
        h += U4.show(ST)

    if mob:
        h += '<section class="sec light"><div class="wrap"><h2 class="claim rv">一款<span class="g">功能强</span>的大屏课表软件</h2>'
        row2 = '<div style="display:flex;gap:10px;justify-content:center;margin-top:14px;font-size:17px;font-family:var(--font)">' + ''.join('<div class="isl static" style="padding:0 1em">%s</div>' % t for t in ['12:30:44', ic('sun') + '&nbsp;9℃', ic('timer') + '&nbsp;元旦 62 天']) + '</div>'
        main_vis = panel_wall(fit('<div style="width:1000px;padding:14px 0 18px"><div style="display:flex;justify-content:center;font-size:19px"><div class="isl-stack">' + static_isl(idle('break', '56%', '78%', 3000)).replace('<div class="isl static"', '<div class="isl static on"') + '</div></div>' + row2.replace('17px', '19px') + '</div>', 1000, 'position:relative;width:100%', 520), '50%', '2%', '190%', 'pad')
        if mob: main_vis = M.main_panel()
        h += ('<div class="blk scene-over rv"><div class="copy"><h3>直观的信息显示</h3><p>自动直观地显示今日的课程安排与当前进行的课程，并支持通过「组件」自定义主界面上显示的内容。</p></div>' + main_vis + '</div>')
        tabs = ('<div class="subs" id="remTabs">'
                '<button class="sub-i on" data-g="0" style="text-align:left;cursor:pointer;color:inherit">' + ic('bell') + '<div><h4>准备上课</h4><p>在上课前一段时间发出提醒，提示做好上课准备。室内课程默认提前 60 秒，室外课程默认提前 600 秒。</p></div></button>'
                '<button class="sub-i" data-g="1" style="text-align:left;cursor:pointer;color:inherit">' + ic('school') + '<div><h4>上课</h4><p>在上课时发出提醒，提示已经上课，并在主界面标出当前课程与剩余时间。</p></div></button>'
                '<button class="sub-i" data-g="2" style="text-align:left;cursor:pointer;color:inherit">' + ic('clock') + '<div><h4>课间休息</h4><p>在下课时发出提醒，并显示本节课间的时长与下一节课。</p></div></button></div>')
        rem_vis = ('<div class="panel" style="--wx:60%;--wy:34%;--ws:200%"><div class="wp"></div><div style="position:relative;padding:20px 0 0">'
                   + fit('<div style="display:flex;justify-content:center;width:100%"><div class="isl-stack" data-demo="rem" id="remIsl" style="font-size:20px">' + REM_STATES + '</div></div>', 1000, 'position:relative;width:100%', 720)
                   + '<div style="padding:18px 4% 0;position:relative;margin-bottom:-24px"><div class="app" data-app="settings" data-start="remind" data-h="600"></div></div></div></div>')
        if mob: rem_vis = M.rem_panel()
        h += ('<div class="blk full ctr rv"><div class="copy"><h3>醒目的提醒系统</h3><p>在上课、下课等重要时间点发出醒目的提醒，提示语可以自行修改，并支持语音播报；放学提醒、天气预警和自动化行动同样可以通过它显示。</p>' + tabs + '</div>' + rem_vis + '</div>')
        subs = ('<div class="subs"><div class="sub-i">' + ic('cal') + '<div><h4>灵活的课表启用规则</h4><p>可为课表设置每周、某一天或循环启用的规则，支持多周轮换，到日期自动切换。</p></div></div>'
                '<div class="sub-i">' + ic('clock') + '<div><h4>时间与科目的自由定制</h4><p>不同课表可使用不同的时间表，并支持自定义科目，设置科目图标与主题色。</p></div></div>'
                '<div class="sub-i">' + ic('edit') + '<div><h4>简洁直观的编辑工具</h4><p>课表、时间表、科目分页编辑，时间表以时间轴方式直接拖动调整。</p></div></div></div>')
        ed_vis = '<div class="edpanel">' + vdesk('<div class="vwin">' + ui2.editor_app(seed='real') + '</div>', 'vdk-bare', 1280, 720, 680, 780).replace('<div class="vtask">', '<div class="vtask" hidden>', 1) + '</div>'
        if mob: ed_vis = M.editor_section()
        h += ('<div class="blk full rv"><div class="copy"><h3>强大的课表系统</h3><p>便捷地导入、编辑和调换课表。点击窗口上方的标签页，试试看。</p>' + subs + '</div>' + ed_vis + '</div>')
        swap_vis = '<div class="edpanel">' + vdesk('<div class="vwin" data-vwin="swap"><div class="sw2 w" data-app="swap" data-modal="1"></div></div><div class="vtray-menu" data-vmenu>' + tray_menu() + '</div>', 'vdk-swap', 800, 500, 720, 520, ' data-vtray="swap"', 'swTray') + '<p class="vcap">点击右下角的托盘图标，选择「换课…」，即可从托盘打开独立的换课窗口。</p></div>'
        if mob: swap_vis = M.swap_section()
        h += ('<div class="blk rev zoomed rv"><div class="copy" style="order:2"><h3>为高效而生的换课</h3><p>换课窗口专为快速调课而设计：从托盘一键打开，选中要调换的课程，再选替换科目，几秒钟完成。</p>'
              '<div class="subs"><div class="sub-i">' + ic('swap') + '<div><h4>当日与跨天都能换</h4><p>可以只换这一次，也可以勾选「永久换课」。</p></div></div>'
              '<div class="sub-i">' + ic('cal') + '<div><h4>临时启用课表</h4><p>在当日或未来某一天临时启用另一个课表，应对调休。</p></div></div></div></div>' + swap_vis + '</div>')
        auto_vis = panel_wall('<div style="padding:3.5% 3%"><div class="app" data-app="settings" data-start="auto" data-h="640"></div></div>', '84%', '60%', '230%', '')
        if mob: auto_vis = M.auto_shot()
        h += '<div class="flow rv"><span>当 <b class="f1" data-tw>时间到了</b></span><i>→</i><span>若 <b class="f2">满足规则</b></span><i>→</i><span>就 <b class="f3">自动执行</b></span></div>\n'
        h += ('<div class="blk full rv"><div class="copy"><h3>智能的自动行为</h3><p>让 ClassFabric 在特定的时间节点执行特定的操作，比如切换组件配置、运行程序、显示提醒。简单来说，就是「当 XX 发生」，并且「满足 XX 规则」时「做什么」。</p>'
              '</div>' + auto_vis + '</div>')
        h += '</div></section>\n'

        h += bigmq(['组件','主题','插件','自动化','外观'], ['拖动','搭配','安装','触发','个性化'])
        h += '<section class="sec" id="custom"><div class="wrap"><h2 class="claim rv">一款<span class="g">可定制</span>的大屏课表软件</h2>'
        wid_vis = panel_wall('<div style="padding:3.5% 3%"><div class="app" data-app="settings" data-start="widgets" data-h="600"></div></div>', '8%', '44%', '230%', '')
        if mob: wid_vis = M.wid_shot()
        h += ('<div class="blk full crop rv"><div class="copy"><h3>使用组件搭配你的主界面</h3><p>通过「组件」自由定制主界面上显示的内容，并支持轮播、滚动、分组与堆叠容器。除了课表，还可以显示日期、时钟、天气与倒计时。</p>'
              '<p>进入「编辑模式」，可以直接在主界面上拖动调整组件。</p></div>' + wid_vis + '</div>')
        thm_vis = panel_wall('<div style="padding:5% 4% 3%"><div class="app" data-app="settings" data-start="appearance" data-h="620"></div></div>', '50%', '90%', '230%', '')
        h += U3.themes(mob, '' if mob else thm_vis)
        plg_vis = panel_wall('<div style="padding:3.5% 3%"><div class="app" data-app="settings" data-start="plugins" data-h="640"></div></div>', '20%', '20%', '230%', '')
        if mob: plg_vis = M.plg_shot()
        h += '<div class="pmq rv" aria-label="社区插件"><div class="t">' + (''.join('<a class="pc" href="https://github.com/%s" target="_blank" rel="noopener"><img src="https://cdn.jsdelivr.net/gh/%s" alt="" loading="lazy" width="48" height="48"><div><b>%s</b><small>%s</small></div></a>' % (repo, icon, name, desc) for name, repo, icon, desc in PLUGINS) * 2) + '</div></div>\n'
        h += ('<div class="blk full crop rv"><div class="copy"><h3>丰富的插件生态</h3><p>支持通过安装插件扩展应用功能，在应用内的插件市场即可浏览、搜索与安装。ClassIsland 的插件可直接使用，ClassFabric 还让插件详情页能预览更多内容。</p></div>' + plg_vis + '</div>')
        h += '</div></section>\n'

        G = [('tl', '时间表', '以时间轴的方式直接拖动调整每一节课的时间。'), ('sj', '科目', '自定义科目的名称、图标与主题色。'), ('grid', '课表', '按周查看并填写课表，科目一键点选。'), ('sw', '调课', '周视图与日历视图，可预定临时启用的课表。')]
        gt = ''.join('<button role="tab" data-gt="%s"%s>%s</button>' % (g[0], ' class="on" aria-selected="true"' if i == 0 else '', g[1]) for i, g in enumerate(G))
        if not mob: h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">档案编辑，<span class="g">所见即所得</span></h2><div class="gal rv"><div class="gtabs" role="tablist">' + gt + '</div>'
              + vdesk('<div class="vwin">' + ui2.editor_app(seed='real') + '</div>', 'vdk-bare', 1280, 720, 680, 780, ' data-gallery="1"').replace('<div class="vtask">', '<div class="vtask" hidden>', 1) +
              '<p class="vcap" id="gcap">' + G[0][2] + '</p></div></div></section>\n')

    else:
        U4.init(dict(globals(), **locals()))
        h += U4.stage()
        h += U4.custom(bigmq, panel_wall)
    if mob: h += bigmq(['更多天气源','托盘菜单','恢复模式','持续同步'], ['OpenWeather','和风天气','SFTP 备份','云端同步'])
    if mob: U4.init(dict(globals(), **locals()))
    h += U4.grow()

    rec_txt = '内置恢复模式：可以安全模式或诊断模式继续使用，直接打开日志目录，恢复备份，必要时分级重置配置，减轻维护压力。'
    if mob:
        rec_vis = panel_wall('<div style="padding:22px 14px 0">' + fit(recovery(), 420, 'position:relative;width:100%;margin-bottom:-4px') + '</div>', '70%', '70%', '240%', '')
        h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">除了这些…</h2>'
              '<div class="blk rv"><div class="copy"><h3>出现问题，也能恢复</h3><p>' + rec_txt + '</p></div>' + rec_vis + '</div></div></section>\n')
    else:
        rec_vis = panel_wall('<div style="display:flex;justify-content:center;padding:5% 0 0">' + fit(recovery(), 420, 'position:relative;width:min(400px,38%);margin-bottom:-4px') + '</div>', '70%', '70%', '240%', '')
        h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">除了这些…</h2></div>' + U4.split('#可靠', '出现问题，也能恢复', rec_txt)
              + '<div class="n4-wide crop rv">' + rec_vis + '</div></section>\n')

    st = [('01', 'dl', '下载', '前往下载页，获取适用于 Windows 的最新版本。', '安装程序 · 免安装压缩包'), ('02', 'play', '运行', '按文件类型安装或解压后启动，主界面会出现在屏幕上方。', '右键托盘图标，打开设置'), ('03', 'check', '接着用', '如果之前使用过 ClassIsland，原有的课表、自动化、插件与主题可直接沿用。', '')]
    if True:
        h += ('<section class="sec" id="start"><div class="wrap"><h2 class="claim rv">三步，<span class="g">开始使用</span></h2><ol class="n5-st">' +
              ''.join('<li><span class="n5-sn">第 %d 步</span><h4>%s</h4><p>%s</p>%s</li>' % (k + 1, b, c, ('<span class="n5-sc">%s</span>' % d) if d else '') for k, (n, i, b, c, d) in enumerate(st)) + '</ol></div></section>\n')

    if True:
        h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">与 ClassIsland 的关系</h2><div class="n5-rel">'
              '<div class="n5-rl"><p>ClassFabric 是在 ClassIsland 基础上二次开发的个人修改版。我们在保持同步上游最新特性的同时，融入来自个人与社区的修改。</p>'
              '<p>名字里的 Fabric，取自 Minecraft 社区知名的模组加载器 Fabric，寓意将社区与个人的功能连接起来；正如 ClassIsland 的 Island，来自 iOS 的灵动岛。</p>'
              '<a class="n5-ln" href="/about.html">了解更多' + '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>' + '</a></div>'
              '<dl class="n5-fit"><div><dt>适合你，如果……</dt><dd>你想在 ClassIsland 生态上保持现有内容，又希望及时体验上游的新功能；或者想要开箱即用，装完就能用上上游、社区与我们开发的各类新功能。</dd></div>'
              '<div><dt>可能不适合，如果……</dt><dd>你希望环境长期保持不变，或所在场合对稳定性有极高要求。ClassFabric 会积极同步上游的更改。</dd></div></dl></div></div></section>\n')

    h += '<section class="sec" id="faqs"><div class="wrap"><h2 class="claim rv">常见问题</h2><div class="faq faqhome rv">' + faq_html() + '</div></div></section>\n'
    if mob:
        h += ('<section class="final3"><div class="wrap"><h2 class="rv">立即体验<br><span class="g">ClassFabric</span></h2><p class="rv d1">更多功能留给您自行探索！</p><div class="cta rv d2"><a class="btn blue" href="/download.html">' + ic('dl') + '立即下载</a><a class="btn glass" href="/about.html">了解更多</a></div></div></section>\n')
    else:
        h += U4.final('<a class="btn blue" href="/download.html">' + ic('dl') + '立即下载</a>', '<a class="btn glass" href="/about.html">了解更多</a>')
    h += '</main>\n'
    if mob:
        return h.replace('<div class="copy" style="order:2">', '<div class="copy">').replace('blk rev zoomed rv', 'blk full rv').replace('blk scene-over rv', 'blk full rv') + FOOT_M
    h += '<template id="tpl-settings">' + ui2.settings_app() + '</template>'
    h += '<template id="schedIc">' + ''.join('<i data-n="%s">%s</i>' % (n, ic(n)) for n in ('clock', 'text', 'atom')) + '</template>'
    return h + FOOT.replace('<script src="/assets/js/fx.js" defer></script>', '<script src="/assets/js/fx.js" defer></script>\n<script src="/assets/js/bento.js" defer></script>\n<script src="/assets/js/home.js" defer></script>')

def dl_menu():
    """下载页舞台里的托盘菜单：完整的真实托盘菜单（ui.tray_menu）；高亮行单独成层（落在「换课...」行），由动画淡入"""
    return tray_menu()[:-len('</div>')] + '<div class="mi mon dl-mh"></div></div>'

def download():
    U3.init(globals())
    h = head('下载 ClassFabric（Windows 版）— 免费 · 开源', '下载 ClassFabric：ClassIsland 的个人修改版班级大屏课表。提供安装程序与免安装版，支持 Windows 10 及更高版本，免费开源，自动选择适合你设备的版本。', '/download.html', '<link rel="preconnect" href="https://api.github.com" crossorigin>\n<link rel="stylesheet" href="/assets/css/tokens.css">\n<link rel="stylesheet" href="/assets/css/display.css">\n<link rel="stylesheet" href="/assets/css/dl.css">\n<link rel="stylesheet" href="/assets/css/modal.css">\n')
    h += navbar('dl')
    chan = ''.join('<button type="button" role="tab" class="%s" aria-selected="%s" aria-controls="assets" data-chan="%s">%s</button>' % ((('on', 'true') if k == 'stable' else ('', 'false')) + (k, t)) for k, t in (('stable', '稳定版'), ('pre', '预览版')))
    sec = lambda i, t, body: '<section class="dl-sec rv" id="%s"><div class="dl-sh"><div><h2>%s</h2></div></div>%s</section>' % (i, t, body)
    chev = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
    isl_states = HERO_STATES.replace('<div class="isl"', '<div class="isl on"', 1)
    h += ('<main id="main" tabindex="-1" class="dl-wrap"><div class="dl-w"><header class="dl-top" id="dltop"><div class="dl-copy"><h1 class="rv">下载 ClassFabric</h1><p class="dl-lead"><span>紧跟上游的 ClassIsland 个人修改版，</span><span>目前提供 Windows 版本。</span></p>'
          '<div class="dl-cta"><a class="btn blue" href="' + REL + '" data-dl rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><g class="dl-ar"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5"/></g><path d="M5 20h14"/></svg><span>下载安装包</span><small data-dlsize></small></a>'
          '<a class="dl-link" href="' + GH + '/releases" data-releaselink rel="noopener">更新日志</a></div>'
          '<p class="dl-line"><span id="chanTip">最新稳定版</span> <b data-ver class="dl-sk"></b>，<span data-date>—</span> 发布</p>'
          '<p class="dl-line">适用于 Windows 10 及更高版本（<span data-archs>x64</span>），免费开源，GPL-3.0。</p>'
          '<div class="dl-info" id="plat" hidden></div></div>'
          '<div class="dl-stage"><div class="dl-st-l dl-st-l1" aria-hidden="true"></div>'
          '<div class="dl-st-l dl-st-l2" aria-hidden="true"><div class="isl-stack" data-demo="dl">' + isl_states + '</div><div class="isl-stack dl-ok">' + mask('下载已开始', 'dl', 3200) + '</div></div>'
          '<div class="dl-st-l dl-st-l3" aria-hidden="true"><div class="dl-desk"><div class="dl-tm">' + dl_menu() + '</div><i class="dl-cur"><svg viewBox="0 0 24 24"><path d="M4 2.5v16.2l4.3-3.9 2.6 6 2.7-1.2-2.6-5.9h5.7z"/></svg></i>' + vtask(True).replace('%s', 'dlTray', 1) + '</div></div></div></header>'
          '<section class="dl-sec rv" id="files"><div class="dl-sh"><div><h2>选择版本</h2><p id="chanDesc">不确定选哪个？下载第一项即可。</p></div>'
          '<div class="dl-sel" id="chan" role="tablist" aria-label="版本通道" hidden>' + chan + '</div></div>'
          '<button type="button" class="dl-fold-t" aria-expanded="false" aria-controls="assets">查看全部文件</button>'
          '<div class="dl-body"><div id="assets" aria-live="polite"><div class="dl-list">' + U3.skel_rows(3) + '</div></div></div></section>'
          + sec('steps', '下载之后', '<div class="dl-prose"><p><b>安装或解压。</b>安装程序按向导完成；压缩包解压到任意目录即可，不必放在系统盘。</p><p><b>启动。</b>主界面会出现在屏幕上方，右键托盘图标即可编辑档案、换课或打开设置。</p></div>')
          + sec('history', '历史版本', '<ul class="dl-list dl-hl" id="hist">' + ''.join('<li class="dl-sk dl-hsk" aria-hidden="true"></li>' for _ in range(6)) + '</ul>')
          + sec('feedback', '说明与反馈', '<div class="dl-prose"><p>预览版包含尚未稳定的新功能，仅在 GitHub 发布了预览版时才可选择。遇到问题或有想法，欢迎在 GitHub 上反馈。</p></div>'
                '<div class="dl-links"><a class="dl-link" href="' + GH + '/issues" rel="noopener">反馈问题' + chev + '</a><a class="dl-link" href="/about.html">了解 ClassFabric' + chev + '</a></div>')
          + '</div></main>\n')
    return h + FOOT_LITE

FAQ = [
    ('原来的课表、插件和主题还能用吗？', '可以。ClassFabric 的底层代码与上游保持一致，安装后原有的课表、自动化、插件与主题可直接沿用。'),
    ('支持 Linux 和 macOS 吗？', '目前仅提供 Windows 版本。代码中保留了相关支持，但我们暂无测试环境与精力维护，因此暂不提供官方构建。'),
    ('有交流群吗？', '暂时没有。ClassIsland 现有的 QQ 频道与群属于上游项目，ClassFabric 的问题请直接在 GitHub 提交 Issue。'),
    ('软件出现问题怎么办？', '可以先尝试内置的恢复模式：以安全模式启动、查看日志、恢复备份，必要时重置配置。仍无法解决，请在 GitHub 提交 Issue 并附上诊断信息。'),
    ('和 ClassIsland 是什么关系？', 'ClassFabric 建立在 ClassIsland 之上，并持续同步上游，没有上游就没有它。可以把它看作一个「更早体验新功能，并带有额外改进」的选择。'),
    ('开源协议是什么？', 'GPL-3.0，与上游一致。ClassIsland 的版权归 HelloWRC，ClassFabric 的改动版权归各自贡献者。'),
]

def faq_html():
    # 原生 <details>（modern-web-guidance: accordion）：不套标题、不互斥，第一项默认展开
    chev = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
    out = '<div class="acc">'
    for i, (q, a) in enumerate(FAQ):
        out += '<details class="acc-i"%s><summary><span>%s</span>%s</summary><div class="acc-p"><p>%s</p></div></details>' % (' open' if i == 0 else '', q, chev, a)
    return out + '</div>'


def about():
    h = head('关于 ClassFabric — 与 ClassIsland 的关系、计划与常见问题', 'ClassFabric 是 ClassIsland 的个人修改版。了解它与上游的关系、从 ClassIsland 切换需要做什么、已完成与计划中的功能，以及常见问题。', '/about.html', '<link rel="stylesheet" href="/assets/css/tokens.css">\n<link rel="stylesheet" href="/assets/css/display.css">\n<link rel="stylesheet" href="/assets/css/about.css">\n')
    h += navbar('about')
    chev = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
    secs = [('relation', '关系'), ('switch', '切换'), ('fit', '适合谁'), ('progress', '进展'), ('name', '名字由来'), ('join', '参与'), ('faq', '常见问题')]
    nav = '<nav class="ab-nav ab-w" id="abNav" aria-label="本页目录">' + ''.join('<a href="#%s">%s</a>' % x for x in secs) + '</nav>'
    sec = lambda i, t, body: '<section class="ab-sec rv" id="%s"><h2>%s</h2><div class="ab-body">%s</div></section>' % (i, t, body)
    steps = ''.join('<li class="ab-in" style="--i:%d"><i>%s</i><div><b>%s</b><p>%s</p></div></li>' % ((n,) + x) for n, x in enumerate([('1', '下载并安装', '从下载页获取适用于 Windows 的版本，安装或解压即可。'), ('2', '启动', '主界面出现在屏幕上方，界面中显示的名称为 ClassFabric。'), ('3', '接着用', '原有的课表、自动化、插件与主题可直接沿用。')]))
    def rows(items, start=0):
        out = ''
        for n, (t, d, st, extra) in enumerate(items):
            out += '<li class="ab-in" style="--i:%d"><div><b>%s</b><p>%s</p>%s</div>%s</li>' % (start + n, t, d, extra, ('<span class="ab-st">%s</span>' % st) if st else '')
        return out
    done = rows([
        ('紧跟上游', '同步 ClassIsland 的新功能与修复。', '', ''),
        ('更多天气源', '除小米天气外，新增 OpenWeather 与和风天气。', '', ''),
        ('多语言', '界面文字由写死改为可翻译的形式，支持简体中文、繁體中文与 English，已完成约 40%，欢迎在 Crowdin 上参与翻译。', '实验中', '<div class="ab-pb"><i></i></div>'),
        ('更好的插件预览', '插件市场的详情页可以预览更多内容。', '', '')])
    road = rows([
        ('云功能 · 远程提醒', '从远端向大屏发送提醒。', '规划中', ''),
        ('云功能 · 集中管理', '统一管理多台设备。上游暂未提供，我们计划原生支持 <a href="https://miniclassisland.com/" rel="noopener">MINI ClassIsland</a> 及其它第三方集控；社区项目 <a href="https://github.com/1sIancl/ClassislandControlHub" rel="noopener">ClassislandControlHub</a> 也在积极开发。', '规划中', ''),
        ('云功能 · 云端备份', '通过 SFTP、WebDAV、OpenList 等方式备份档案与配置。', '规划中', ''),
        ('更好的自动化', '主要借助社区知名插件 SystemTools 实现。', '规划中', ''),
        ('更好的性能表现', '持续优化。', '规划中', '')], 4)
    go = ''.join('<li class="ab-in" style="--i:%d"><a class="ab-row" href="%s" rel="noopener">%s%s</a></li>' % (n, u, t, chev) for n, (u, t) in enumerate([(GH, 'GitHub 仓库'), (GH + '/issues', '反馈问题'), (GH + '/pulls', '提交 PR')]))
    h += ('<main id="main" tabindex="-1" class="ab-wrap"><div class="ab-w"><header class="ab-top" id="abtop"><div class="ab-copy"><h1 class="rv">关于 ClassFabric</h1>'
          '<p class="ab-lead"><span>ClassIsland 的个人修改版：</span><span>紧跟上游，</span><span>你的课表、</span><span>自动化、</span><span>插件与主题</span><span>直接沿用。</span></p>'
          '<a class="ab-link" href="#switch">了解如何切换' + chev + '</a>'
          '<p class="ab-line">基于 HelloWRC 的 ClassIsland 二次开发，沿用上游的 GPL-3.0 开源协议。</p></div></header></div>'
          '<div class="ab-bar">' + nav + '</div><div class="ab-w">'
          + sec('relation', '与 ClassIsland 的关系', '<p class="ab-q">ClassFabric 是基于 HelloWRC 的 ClassIsland 二次开发的<strong>个人修改版</strong>。</p>'
                '<p>在保持积极同步上游最新特性的同时，融入来自个人与社区的修改，例如多语言、云功能、更好的自动化、更好的性能表现与更多功能。其中一部分已经完成，另一部分仍处于规划阶段，详见下文「进展」。</p>'
                '<p>ClassIsland 的作者是 HelloWRC。ClassFabric 沿用上游的 GPL-3.0 开源协议，软件的「关于」页中也保留了上游的版权声明。</p>')
          + sec('switch', '从 ClassIsland 切换，需要做什么', '<p class="ab-q">不需要复杂的前期工作。</p><p>ClassFabric 的底层代码与上游保持一致，只需下载并安装，原有的课表、自动化、插件与主题即可接着使用。</p><ol class="ab-steps">' + steps + '</ol>'
                '<div class="ab-info">' + ic('info') + '<p>我们仍在继续让底层代码向上游靠拢，界面上则保留 ClassFabric 这个名字。这样你切换过来，看到的是熟悉的界面，原来的设置也照常能用，几乎感觉不到变化。</p></div>')
          + sec('fit', '适合谁，不适合谁', '<div class="ab-fit"><div class="yes"><h3>' + ic('check') + '适合</h3><ul><li>想在 ClassIsland 生态上保持现有内容，又希望及时体验上游新功能的人</li><li>希望开箱即用，装完就能体验上游、社区与我们开发的各类新功能的人</li></ul></div>'
                '<div class="no"><h3>' + ic('info') + '不太适合</h3><ul><li>希望环境长期保持不变的人</li><li>对稳定性有极高要求的场合</li></ul><p>ClassFabric 会积极同步上游的更改，版本变化相对频繁。</p></div></div>')
          + sec('progress', '进展', '<h3 class="ab-gh">已经做了</h3><ul class="ab-list">' + done + '</ul><p>想了解具体改动，可以查看 <a href="' + GH + '/commits/main" rel="noopener">GitHub 提交记录</a>。</p>'
                '<h3 class="ab-gh">计划中</h3><p>以下内容仍在规划阶段，<strong>尚未可用</strong>。</p><ul class="ab-list">' + road + '</ul>')
          + sec('name', '名字由来', '<div class="ab-name"><div class="ab-in" style="--i:0"><div class="ab-eq">Class<i>+</i>Island</div><p>Island，来自 iOS 的「灵动岛」。</p></div>'
                '<div class="ab-ar ab-in" style="--i:3" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>'
                '<div class="ab-in" style="--i:6"><div class="ab-eq">Class<i>+</i><span class="f">Fabric</span></div><p>Fabric，取自 Minecraft 社区知名的模组加载器，寓意将社区与个人的功能连接起来。</p></div></div>')
          + sec('join', '参与贡献', '<p>欢迎任何有价值的贡献：在 GitHub 提交 Issue 或 PR 即可。我们也会考虑定期将有意义的改动提交给上游，一起建设 ClassIsland 生态。</p><ul class="ab-list ab-go">' + go + '</ul>')
          + sec('faq', '常见问题', '<div class="faq">' + faq_html() + '</div>')
          + '</div></main>'
          '<section class="final3"><div class="wrap"><h2 class="rv">立即体验<br><span class="g">ClassFabric</span></h2><p class="rv d1">更多功能留给您自行探索！</p>'
          '<div class="cta rv d2"><a class="btn blue" href="/download.html">' + ic('dl') + '立即下载</a><a class="btn glass" href="/">返回首页</a></div></div></section>\n')
    return h + FOOT_LITE.replace('<script src="/assets/js/dl.js" defer></script>\n', '').replace('<script src="/assets/js/fx.js" defer></script>', '<script src="/assets/js/fx.js" defer></script>\n<script src="/assets/js/about.js" defer></script>')

def notfound():
    h = head('页面未找到（404）— ClassFabric', 'ClassFabric 官网：你访问的页面不存在，或者已经移走。', '/404.html', '<link rel="preconnect" href="https://api.bimg.cc">\n<link rel="stylesheet" href="/assets/css/nf.css">\n')
    for pat in (r'<link rel="canonical"[^>]*>\n?', r'<link rel="alternate"[^>]*>\n?', r'<meta property="og:url"[^>]*>\n?'):
        h = re.sub(pat, '', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    h = h.replace('content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"', 'content="noindex,follow"')
    h += navbar('')
    # 整屏 Bing 每日壁纸 + 超大的诗。没有脚本时显示第一首；有脚本时由 nf.js 随机换成其中一首并启用「换一首」
    poem = ('邮差照着旧地址，敲了三年的门。', '门后换了人，换了漆，换了门牌。', '他每次都问：「请问，是不是——」', '住户每次都说：「不是，进来喝口水。」', '信还在他包里。', '地址早就不存在了，', '水，倒一直是热的。')
    h += ('<main id="main" tabindex="-1" class="nf"><div class="nf-bg" aria-hidden="true"><i></i></div><div class="nf-in">'
          '<h1 class="nf-k"><span class="nf-n">404</span><span class="nf-sr"> 页面不存在</span><span class="nf-e" id="nfk" aria-hidden="true">(´･ω･`)</span></h1>'
          '<blockquote class="nf-pl" id="nfpl">' + ''.join('<span class="l">%s</span>' % t for t in poem) + '</blockquote>'
          '<p class="nf-by">—— Sonnet 5.5</p>'
          '<div class="nf-act"><a class="nf-b pri" href="/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11l9-8 9 8M5 10v10h5v-6h4v6h5V10"/></svg>回到首页</a><button class="nf-b" id="nfsw" type="button" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11a8 8 0 10-2.3 5.7M20 4v7h-7"/></svg>换一首</button></div>'
          '<p class="nf-cr" id="nfcr" hidden></p></div></main>\n')
    return h + FOOT_LITE.replace('<script src="/assets/js/dl.js" defer></script>\n', '').replace('<script src="/assets/js/fx.js" defer></script>', '<script src="/assets/js/fx.js" defer></script>\n<script src="/assets/js/nf.js" defer></script>')  # 404 没有版本号/下载区，不加载 dl.js

# 跨文档视图过渡：等首屏元素解析完再开始过渡，否则新页快照是半成品，淡入时会出现“残影”（modern-web-guidance: consistent-cross-document-transitions）
EXPECT = {'index.html': 'top', 'download.html': 'dltop', 'about.html': 'abtop', '404.html': 'main'}
def expect(name, html):
    return html.replace('</head>', '<link rel="expect" href="#%s" blocking="render">\n</head>' % EXPECT[name], 1)
for name, fn in (('index.html', home), ('download.html', download), ('about.html', about), ('404.html', notfound)):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(expect(name, vers(levels(fn()))))
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, p, datetime.date.today().isoformat()) for p in ('/', '/download.html', '/about.html')) + '</urlset>\n')
os.makedirs(os.path.join(OUT, 'm'), exist_ok=True)
open(os.path.join(OUT, 'm', 'index.html'), 'w', encoding='utf-8').write(expect('index.html', vers(levels(home(True)))))
print('ok')
