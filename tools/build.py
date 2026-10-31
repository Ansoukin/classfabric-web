# -*- coding: utf-8 -*-
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import *

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ansoukin.top'
GH = 'https://github.com/Ansoukin/ClassFabric'
REL = GH + '/releases/latest'

def svg_(n, extra=''):
    return ic(n, extra)

# ------------------------------------------------------------------ islands
def idle(kind, p0, p1, ms, g=None):
    wx = '<span class="wx">%s9℃</span><span class="dt">周四 10/29</span>' % ic('sun')
    past = ''.join('<span class="s p">%s</span>' % c for c in '语数英')
    if kind == 'break':
        cur = '<span class="cur">%s<span>课间休息</span><small>10:00-10:30</small></span>' % ic('clock')
        fut = ''.join('<span class="s">%s</span>' % c for c in '物化生政历地自自')
    else:
        cur = '<span class="cur">%s<span>物理</span><span class="pill">-39m</span></span>' % ic('atom')
        fut = ''.join('<span class="s">%s</span>' % c for c in '化生政历地自自')
    return '<div class="isl"%s data-ms="%d" style="--dur:%.1fs;--p0:%s;--p1:%s">%s%s%s<span class="sep"></span>%s</div>' % (
        (' data-g="%d"' % g) if g is not None else '', ms, ms / 1000, p0, p1, wx, past, cur, fut)

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

def static_isl(h, w='50%'):
    return h.replace('class="isl bar', 'class="isl static bar').replace('<div class="isl"', '<div class="isl static"').replace('<div class="isl mask', '<div class="isl static mask')

# ------------------------------------------------------------------ chrome
def head(title, desc, path, extra=''):
    url = SITE + path
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n<meta name="theme-color" content="#141312">\n'
            '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icon-192.png">\n<link rel="apple-touch-icon" href="/assets/img/icon-180.png">\n'
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="ClassFabric">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n<meta property="og:image" content="%s/assets/img/og.jpg">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="color-scheme" content="dark light">\n<script>try{var t=localStorage.getItem("cf_theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>\n<link rel="stylesheet" href="/assets/css/site.css">\n%s</head>\n') % (title, desc, url, title, desc, url, SITE, extra)

def navbar(cur):
    def a(href, label, key):
        return '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if cur == key else '', label)
    return ('<body>\n<header class="nav" id="nav"><div class="wrap"><a class="brand" href="/"><img src="/assets/img/icon-64.png" width="26" height="26" alt="">ClassFabric</a>'
            '<nav class="links" id="links" aria-label="主导航">' + a('/', '首页', 'home') + a('/download.html', '下载', 'dl') + a('/about.html', '关于', 'about') + '<a href="' + GH + '" rel="noopener">GitHub 仓库</a></nav>'
            '<div class="tools"><button class="ibtn" id="theme" aria-label="切换明暗主题"><svg class="i-moon" viewBox="0 0 24 24"><path d="M20 14.5A8.5 8.5 0 019.5 4 8.5 8.5 0 1020 14.5z"/></svg><svg class="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>'
            '<a class="btn blue sm" href="/download.html">' + ic('dl') + '立即下载</a>'
            '<button class="ibtn menu-btn" id="menu" aria-label="菜单" aria-expanded="false"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div></div></header>\n')

FOOT = ('<footer class="foot"><div class="wrap"><div class="cols"><div><a class="brand" href="/"><img src="/assets/img/icon-64.png" width="26" height="26" alt="">ClassFabric</a>'
        '<p class="about">ClassIsland 的个人修改版班级大屏课表。紧跟上游，并加入来自社区与我们的改进。</p></div>'
        '<div><h5>产品</h5><ul><li><a href="/download.html">下载</a></li><li><a href="' + GH + '/releases" rel="noopener">版本发布</a></li><li><a href="/about.html#planned">计划中的功能</a></li></ul></div>'
        '<div><h5>项目</h5><ul><li><a href="' + GH + '" rel="noopener">GitHub 仓库</a></li><li><a href="' + GH + '/issues" rel="noopener">反馈问题</a></li><li><a href="/about.html#join">参与贡献</a></li></ul></div>'
        '<div><h5>了解更多</h5><ul><li><a href="/about.html">关于 ClassFabric</a></li><li><a href="/about.html#faq">常见问题</a></li><li><a href="https://classisland.tech" rel="noopener">ClassIsland 官网</a></li></ul></div></div>'
        '<div class="legal">© 2026 ClassFabric　基于 HelloWRC 的 ClassIsland（© 2023–2026 HelloWRC）二次开发，以 GPL-3.0 协议开源。<br>ClassFabric 是个人修改版，并非 ClassIsland 官方项目；ClassIsland 的名称与原有功能归其原作者所有。</div></div></footer>\n'
        '<script src="/assets/js/site.js" defer></script>\n</body>\n</html>\n')

def ld():
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"ClassFabric","applicationCategory":"EducationApplication","operatingSystem":"Windows 10, Windows 11",'
            '"description":"ClassIsland 的个人修改版班级大屏课表，紧跟上游更新，原有课表、插件与主题可直接沿用。","url":"%s/","license":"https://www.gnu.org/licenses/gpl-3.0.html","isBasedOn":"https://classisland.tech","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}</script>\n') % SITE

# ------------------------------------------------------------------ home
def panel_wall(inner, wx='50%', wy='50%', ws='170%', cls='pad'):
    return '<div class="panel %s" style="--wx:%s;--wy:%s;--ws:%s"><div class="wp"></div><div style="position:relative">%s</div></div>' % (cls, wx, wy, ws, inner)

def home():
    h = head('ClassFabric — 紧跟上游的 ClassIsland 个人修改版班级大屏课表',
             'ClassFabric 是基于 ClassIsland 的个人修改版班级大屏课表：积极同步上游特性，原有课表、自动化、插件与主题无缝沿用，并加入更多天气源、多语言等改进。', '/', ld())
    h += navbar('home')
    h += '<main>\n'
    # hero
    h += ('<section class="hero"><div class="wrap">'
          '<div class="lockup rv"><img src="/assets/img/logo.png" alt="">ClassFabric<span>班级大屏课表</span></div>'
          '<h1 class="rv">紧跟上游，<span class="g">再进一步</span></h1>'
          '<p class="sub rv d1">基于 ClassIsland 的个人修改版，原有课表、插件与主题无缝沿用</p>'
          '<div class="cta rv d2"><a class="btn blue" href="' + REL + '" data-dl data-releaselink rel="noopener">' + ic('dl') + '立即下载</a><a class="btn glass" href="' + GH + '" rel="noopener">' +
          '<svg viewBox="0 0 16 16" fill="currentColor" stroke="none"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>GitHub 仓库</a></div>'
          '<p class="note rv d2">支持在 Windows 10/11 上运行　·　最新版本 <b data-ver>—</b>　·　GPL-3.0 开源</p>'
          '<div class="desk rv d2" id="heroDesk" role="img" aria-label="ClassFabric 演示：右键托盘图标，打开档案编辑，填入课表，主界面随即在屏幕上方显示今日课程并发出上课提醒">'
          + fit('<div style="display:flex;justify-content:center;width:1180px"><div class="isl-stack" data-demo="hero" id="hIsl">' + HERO_STATES + '</div></div>', 1180, 'left:0;top:3.2%;width:100%', 640, 'hisl')
          + fit(editor_window(1500, 640, False, 'hEd'), 1500, 'left:7%;top:15%;width:60%', None, 'hwin')
          + fit(tray_menu(), 190, 'right:1.2%;bottom:6.2%;width:15%', None, 'htray')
          + '<div class="taskbar"><i></i><i></i><i></i><i></i><i></i><div class="tray"><b></b><b></b><span class="ctray" id="hTrayIco"><img src="/assets/img/icon-32.png" alt=""></span><span>10:12<br>2026/10/29</span></div></div>'
          '<svg class="cursor" id="hCur" viewBox="0 0 24 24"><path d="M4 2.5v17l4.6-4.4 3 6.9 2.9-1.3-3-6.8h6.5z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
          '</div></div></section>\n')

    # claim 1
    def fc(icn, t, d='', trail=''):
        return '<div class="fcard">%s<div class="tx"><b>%s</b>%s</div>%s</div>' % (ic(icn), t, ('<span>%s</span>' % d) if d else '', trail)
    ok = '<span class="ok">' + ic('check') + '已同步</span>'
    used = '<span class="ok">' + ic('check') + '已沿用</span>'
    on = '<span class="tg on"><i></i></span>'
    c_sync = fc('sync', '新功能', 'ClassIsland 发布的新功能', ok) + fc('bolt', '问题修复', 'ClassIsland 的修复与改进', ok) + fc('info', '上游版本', '底层代码与上游保持一致', ok)
    c_mig = fc('cal', '课表与档案', '', used) + fc('bolt', '自动化', '', used) + fc('plug', '插件', '', used) + fc('brush', '主题', '', used)
    c_enh = fc('cloud', '更多天气源', '小米天气 · OpenWeather · 和风天气', on) + fc('text', '多语言', '实验中', on) + fc('plug', '更好的插件预览', '', on) + fc('sync', '持续同步上游', '', on)
    h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">一款<span class="g">紧跟上游</span>的大屏课表软件</h2><div class="grid3">'
          '<div class="copy rv"><span class="tag">#同步</span><h3>积极同步上游特性</h3><p>ClassIsland 的新功能与修复，会尽快同步到 ClassFabric。</p><div class="fstack">' + c_sync + '</div></div>'
          '<div class="copy rv d1"><span class="tag p">#迁移</span><h3>无感切换，沿用现有配置</h3><p>底层代码与上游保持一致。原有的课表、自动化、插件与主题，安装后即可继续使用。</p><div class="fstack">' + c_mig + '</div></div>'
          '<div class="copy rv d2"><span class="tag o">#增强</span><h3>来自社区与我们的增强</h3><p>在上游之上加入更多天气源、多语言支持（实验中）与更好的插件预览，并将持续扩充。</p><div class="fstack">' + c_enh + '</div></div>'
          '</div></div></section>\n')

    # showcase
    def sidle(past, cur, fut):
        return '<div class="isl static on"><span class="pa">%s</span>%s<span class="sep"></span><span class="fu">%s</span></div>' % (''.join('<span class="s p">%s</span>' % c for c in past), cur, ''.join('<span class="s">%s</span>' % c for c in fut))
    def sbar2(l, ms=''):
        return '<div class="isl static on bar two"><span>%s</span><span class="nx">下节课是: <em>物理</em><small>10:30-11:10</small></span></div>' % l
    def smask(t, icn):
        return '<div class="isl static on mask">%s<span>%s</span>%s</div>' % (ic('info'), t, ic(icn))
    ST = [sbar2('距上课还剩 <b>16</b> 秒'),
          '<div class="isl static on bar">准备上课，请回到座位并保持安静，做好上课准备。</div>',
          smask('上课', 'atom'),
          sidle('语数英', '<span class="cur">' + ic('clock') + '<span>课间休息</span><small>10:20-10:30</small></span>', '物化生历政地'),
          smask('即将上课', 'atom'),
          sidle('语数', '<span class="cur">' + ic('text') + '<span>英语</span><span class="pill">-31s</span></span>', '物化生历政地'),
          smask('课间休息', 'clock'),
          sbar2('本节课间休息长 <b>10</b> 分钟')]
    wrapi = lambda x: '<div class="mq-i"><div class="isl-stack">' + x + '</div></div>'
    row1 = ''.join(wrapi(x) for x in (ST[0], ST[1], ST[2], ST[3]))
    row2 = ''.join(wrapi(x) for x in (ST[4], ST[5], ST[6], ST[7]))
    h += ('<section class="sec show"><div class="wrap"><h2 class="claim rv">上课与下课，<span class="g">一目了然</span></h2></div>'
          '<div class="marq rv" aria-label="灵动岛的各种状态"><div class="row"><div class="trk">' + row1 * 2 + '</div></div><div class="row rev"><div class="trk">' + row2 * 2 + '</div></div></div>'
          '<div class="wrap"><figure class="vid rv" id="vid"><video muted loop playsinline preload="none" data-src="https://www.classisland.tech/assets/notification-demo.web-Os7FSQPD.mp4" aria-label="提醒演示视频"></video></figure></div></section>\n')

    # claim 2
    h += '<section class="sec light"><div class="wrap"><h2 class="claim rv">一款<span class="g">功能强</span>的大屏课表软件</h2>'
    # 主界面
    row2 = '<div style="display:flex;gap:10px;justify-content:center;margin-top:14px;font-size:17px;font-family:var(--font)">' + ''.join('<div class="isl static" style="padding:0 1em">%s</div>' % t for t in ['12:30:44', ic('sun') + '&nbsp;9℃', ic('timer') + '&nbsp;元旦 62 天']) + '</div>'
    main_vis = panel_wall(fit('<div style="width:1000px;padding:14px 0 18px"><div style="display:flex;justify-content:center;font-size:19px"><div class="isl-stack">' + static_isl(idle('break', '56%', '78%', 3000)).replace('<div class="isl static"', '<div class="isl static on"') + '</div></div>' + row2.replace('17px', '19px') + '</div>', 1000, 'position:relative;width:100%', 520), '50%', '2%', '190%', 'pad')
    h += ('<div class="blk rv"><div class="copy"><span class="tag">#主界面</span><h3>直观的信息显示</h3><p>自动直观地显示今日的课程安排与当前进行的课程，并支持通过「组件」自定义主界面上显示的内容。</p></div>' + main_vis + '</div>')
    # 提醒
    tabs = ('<div class="subs" id="remTabs">'
            '<button class="sub-i on" data-g="0" style="text-align:left;cursor:pointer;color:inherit">' + ic('bell') + '<div><h4>准备上课</h4><p>在上课前一段时间发出提醒，提示做好上课准备。室内课程默认提前 60 秒，室外课程默认提前 600 秒。</p></div></button>'
            '<button class="sub-i" data-g="1" style="text-align:left;cursor:pointer;color:inherit">' + ic('school') + '<div><h4>上课</h4><p>在上课时发出提醒，提示已经上课，并在主界面标出当前课程与剩余时间。</p></div></button>'
            '<button class="sub-i" data-g="2" style="text-align:left;cursor:pointer;color:inherit">' + ic('clock') + '<div><h4>课间休息</h4><p>在下课时发出提醒，并显示本节课间的时长与下一节课。</p></div></button></div>')
    rem_vis = ('<div class="panel" style="--wx:60%;--wy:34%;--ws:200%"><div class="wp"></div><div style="position:relative;padding:20px 0 0">'
               + fit('<div style="display:flex;justify-content:center;width:1000px"><div class="isl-stack" data-demo="rem" id="remIsl" style="font-size:20px">' + REM_STATES + '</div></div>', 1000, 'position:relative;width:100%', 560)
               + '<div style="padding:18px 0 0 8%;position:relative;margin-bottom:-24px">' + fit(settings_window('remind', 1500, 640), 1500, 'position:relative;width:100%') + '</div></div></div>')
    h += ('<div class="blk full rv"><div class="copy"><span class="tag o">#提醒</span><h3>醒目的提醒系统</h3><p>在上课、下课等重要时间点发出醒目的提醒，提示语可以自行修改，并支持语音播报；放学提醒、天气预警和自动化行动同样可以通过它显示。</p>' + tabs + '</div>' + rem_vis + '</div>')
    # 课表
    subs = ('<div class="subs"><div class="sub-i">' + ic('cal') + '<div><h4>灵活的课表启用规则</h4><p>可为课表设置每周、某一天或循环启用的规则，支持多周轮换，到日期自动切换。</p></div></div>'
            '<div class="sub-i">' + ic('clock') + '<div><h4>时间与科目的自由定制</h4><p>不同课表可使用不同的时间表，并支持自定义科目，设置科目图标与主题色。</p></div></div>'
            '<div class="sub-i">' + ic('edit') + '<div><h4>简洁直观的编辑工具</h4><p>课表、时间表、科目分页编辑，时间表以时间轴方式直接拖动调整。</p></div></div></div>')
    ed_vis = panel_wall('<div style="padding:4% 3% 0">' + fit(editor_window(1500, 640, True, 'edMain'), 1500, 'position:relative;width:100%') + '</div>', '30%', '60%', '230%', '')
    h += ('<div class="blk full rv"><div class="copy"><span class="tag p">#课表</span><h3>强大的课表系统</h3><p>便捷地导入、编辑和调换课表。点击右侧的标签页，试试看。</p>' + subs + '</div>' + ed_vis + '</div>')
    # 调课
    swap_vis = panel_wall('<div style="padding:5% 4% 0"><div id="swapIsl" style="display:flex;justify-content:center;margin-bottom:12px">' + fit('<div style="display:flex;justify-content:center;width:640px;font-size:17px"><div class="isl-stack" id="swIsl"><div class="isl static on" id="swIslIn"></div></div></div>', 640, 'position:relative;width:100%') + '</div>' + fit(swap_dialog(), 640, 'position:relative;width:78%;margin:0 auto 5%') + '</div>', '70%', '36%', '210%', '')
    h += ('<div class="blk rev rv"><div class="copy" style="order:2"><span class="tag gr">#调课</span><h3>提前调整课程</h3><p>支持当日与跨天换课，灵活应对调课情景。可以只换这一次，也可以勾选「永久换课」。</p>'
          '<div class="subs"><div class="sub-i">' + ic('swap') + '<div><h4>临时启用课表</h4><p>可在当日或未来某一天临时启用另一个课表，应对调休与换课。</p></div></div>'
          '<div class="sub-i">' + ic('import') + '<div><h4>从其它软件导入课表</h4><p>支持直接导入其它课表软件的课表信息，也支持从 CSES 导入。</p></div></div></div></div>' + swap_vis + '</div>')
    # 自动化
    auto_vis = panel_wall('<div style="padding:3.5% 3%">' + fit(settings_window("auto", 1920, 700), 1920, 'position:relative;width:100%') + '</div>', '84%', '60%', '230%', '')
    h += ('<div class="blk full rv"><div class="copy"><span class="tag">#自动化</span><h3>智能的自动行为</h3><p>让 ClassFabric 在特定的时间节点执行特定的操作，比如切换组件配置、运行程序、显示提醒。简单来说，就是「当 XX 发生」，并且「满足 XX 规则」时「做什么」。</p>'
          '</div>' + auto_vis + '</div>')
    h += '</div></section>\n'

    # claim 3
    h += '<section class="sec"><div class="wrap"><h2 class="claim rv">一款<span class="g">可定制</span>的大屏课表软件</h2>'
    wid_vis = panel_wall('<div style="padding:3.5% 3%">' + fit(settings_window('widgets', 1242, 590), 1242, 'position:relative;width:100%') + '</div>', '8%', '44%', '230%', '')
    h += ('<div class="blk full rv"><div class="copy"><span class="tag p">#组件</span><h3>使用组件搭配你的主界面</h3><p>通过「组件」自由定制主界面上显示的内容，并支持轮播、滚动、分组与堆叠容器。除了课表，还可以显示日期、时钟、天气与倒计时。</p>'
          '<p>进入「编辑模式」，可以直接在主界面上拖动调整组件。</p></div>' + wid_vis + '</div>')
    thm_vis = panel_wall('<div style="padding:5% 4% 3%">' + fit(settings_window('themes', 1500, 640), 1500, 'position:relative;width:100%') + '</div>', '50%', '90%', '230%', '')
    h += ('<div class="blk full rv"><div class="copy"><span class="tag o">#主题</span><h3>自由的主题系统</h3><p>内置经典、Fluent 与 Rectangles 三套主题，并支持调整界面缩放、背景透明度、圆角与字体，高度个性化你的界面。</p></div>' + thm_vis + '</div>')
    plg_vis = panel_wall('<div style="padding:3.5% 3%">' + fit(settings_window('plugins', 1242, 590), 1242, 'position:relative;width:100%') + '</div>', '20%', '20%', '230%', '')
    h += ('<div class="blk full rv"><div class="copy"><span class="tag gr">#插件</span><h3>丰富的插件生态</h3><p>支持通过安装插件扩展应用功能，在应用内的插件市场即可浏览、搜索与安装。ClassIsland 的插件可直接使用，ClassFabric 还让插件详情页能预览更多内容。</p></div>' + plg_vis + '</div>')
    h += '</div></section>\n'

    # gallery
    G = [('shot-timeline', '时间表', '以时间轴的方式直接拖动调整每一节课的时间。'), ('shot-subjects', '科目', '自定义科目的名称、图标与主题色。')]
    gt = ''.join('<button role="tab" data-g="%d"%s>%s</button>' % (i, ' class="on" aria-selected="true"' if i == 0 else '', g[1]) for i, g in enumerate(G))
    gi = ''.join('<img class="gimg%s" data-cap="%s" src="/assets/img/%s.webp" alt="ClassFabric %s界面截图" loading="lazy" width="1920" height="1040">' % (' on' if i == 0 else '', g[2], g[0], g[1]) for i, g in enumerate(G))
    h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">档案编辑，<span class="g">所见即所得</span></h2><div class="gal rv"><div class="gtabs" role="tablist">' + gt + '</div>'
          '<div class="gframe" id="gframe" title="点击放大">' + gi + '</div></div></div></section>\n')

    # claim 4
    wx = ('<div class="cd s3 rv"><h4>更多天气源</h4><p>除 ClassIsland 内置的小米天气外，新增 OpenWeather 与和风天气（QWeather），可自行选择天气来源。</p><div class="vis"><div class="chips-row"><span class="chip on">小米天气 · 内置</span><span class="chip">OpenWeather</span><span class="chip">和风天气</span></div></div></div>')
    ln = ('<div class="cd s3 rv d1"><h4>多语言 <span style="font-size:13px;color:var(--faint);font-weight:500">实验中</span></h4><p>界面文字正在由写死改为可翻译的形式，目前支持简体中文、繁體中文与 English，翻译通过 Crowdin 协作。仍有不少文字与界面需要适配，欢迎参与。</p>'
          '<div class="vis"><div class="chips-row"><span class="chip on">简体中文</span><span class="chip">繁體中文</span><span class="chip">English</span></div><div class="bar40" id="bar40"><i></i></div><div style="font-size:12.5px;color:var(--faint);margin-top:8px">适配进度 约 40%</div></div></div>')
    pv = ('<div class="cd s2 rv"><h4>更好的插件预览</h4><p>插件市场的详情页可以预览更多内容，安装之前就能看清插件的样子。</p><div class="vis"><div style="display:flex;gap:14px;align-items:center;padding:14px;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.03)">'
          '<span style="width:46px;height:46px;border-radius:10px;background:#6a6a6a;display:grid;place-items:center;font-weight:800;font-size:20px;flex:none">U</span><div style="flex:1;min-width:0"><b style="display:block">UIAccess 提权</b><span style="font-size:13px;color:var(--muted)">2.0.0.0 · HelloWRC, Doubx690i</span></div><span class="chip on" style="padding:6px 14px">安装</span></div>'
          '<div style="height:70px;margin-top:10px;border-radius:10px;border:1px solid var(--line);background:linear-gradient(90deg,#0d1b2e,#15335a 45%,#0e2240);position:relative;overflow:hidden"><div style="position:absolute;left:10%;right:10%;top:46%;height:7px;border-radius:4px;background:rgba(98,179,242,.55)"></div></div></div></div>')
    jn = ('<div class="cd s2 rv d2"><h4>欢迎参与共建</h4><p>欢迎在 GitHub 提交 Issue 与 PR；有价值的改动，我们也会考虑定期提交回上游，一起建设 ClassIsland 生态。</p><div class="vis"><div class="cta" style="justify-content:flex-start"><a class="btn glass" href="' + GH + '/issues" rel="noopener">反馈问题</a><a class="btn glass" href="' + GH + '/pulls" rel="noopener">提交 PR</a></div></div></div>')
    tray = ('<div class="cd s2 rv d1 trayc"><h4>一切，都在托盘里</h4><p>右键托盘图标，即可编辑档案、换课、加载临时课表，或打开应用设置。</p><div class="vis"><img src="/assets/img/tray.webp" alt="托盘菜单" loading="lazy" width="187" height="390"></div></div>')
    h += '<section class="sec"><div class="wrap"><h2 class="claim rv">一款<span class="g">不断增强</span>的大屏课表软件</h2><div class="cards2">' + wx + ln + pv + tray + jn + '</div></div></section>\n'

    # 除了这些
    rec_vis = panel_wall('<div style="display:flex;gap:6%;align-items:flex-end;justify-content:center;padding:6% 5% 0">' + fit(recovery(), 420, 'position:relative;width:54%;margin-bottom:-4px') + '</div>', '70%', '70%', '240%', '')
    h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">除了这些…</h2>'
          '<div class="blk rv"><div class="copy"><span class="tag gr">#可靠</span><h3>出现问题，也能恢复</h3><p>内置恢复模式：可以安全模式或诊断模式继续使用，直接打开日志目录，恢复备份，必要时分级重置配置，减轻维护压力。</p></div>' + rec_vis + '</div></div></section>\n')

    # steps
    st = [('1', '下载', '前往下载页，获取适用于 Windows 的最新版本。'), ('2', '运行', '按文件类型安装或解压后启动，主界面会出现在屏幕上方。'), ('3', '接着用', '如果之前使用过 ClassIsland，原有的课表、自动化、插件与主题可直接沿用。')]
    h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">三步，<span class="g">开始使用</span></h2><div class="steps3">' +
          ''.join('<div class="st rv d%d"><i>%s</i><h4>%s</h4><p>%s</p></div>' % (k, a, b, c) for k, (a, b, c) in enumerate(st)) + '</div></div></section>\n')

    # relation
    h += ('<section class="sec"><div class="wrap"><h2 class="claim rv">与 ClassIsland 的关系</h2><div class="rel">'
          '<div class="copy rv"><p>ClassFabric 是在 ClassIsland 基础上二次开发的个人修改版，既不是它的完美替代品，也不是竞品。我们在保持同步上游最新特性的同时，融入来自个人与社区的修改。</p>'
          '<p>名字里的 Fabric，取自 Minecraft 社区知名的模组加载器 Fabric，寓意将社区与个人的功能连接起来；正如 ClassIsland 的 Island，来自 iOS 的灵动岛。</p>'
          '<a class="btn glass" href="/about.html">了解更多</a></div>'
          '<div class="fit2 rv d1"><div><h4>适合你，如果……</h4><p>你想在 ClassIsland 生态上保持现有内容，又希望及时体验上游的新功能；或者想要开箱即用，装完就能用上上游、社区与我们开发的各类新功能。</p></div>'
          '<div class="no"><h4>可能不适合，如果……</h4><p>你希望环境长期保持不变，或所在场合对稳定性有极高要求。ClassFabric 会积极同步上游的更改。</p></div></div></div></div></section>\n')

    # final
    h += ('<section class="final3"><div class="wrap"><h2 class="rv">立即体验 ClassFabric</h2><p class="rv d1">更多功能留给您自行探索！</p><div class="cta rv d2"><a class="btn blue" href="/download.html">' + ic('dl') + '立即下载</a><a class="btn glass" href="/about.html">了解更多</a></div></div></section>\n')
    h += '</main>\n'
    return h + FOOT

# ------------------------------------------------------------------ download
def download():
    h = head('下载 ClassFabric — Windows 版', '下载 ClassFabric，ClassIsland 的个人修改版班级大屏课表。支持 Windows 10 及更高版本，免费开源。', '/download.html')
    h += navbar('dl')
    h += ('<main><section class="phead"><div class="wrap"><h1>下载 ClassFabric</h1><p>目前提供 Windows 版本。</p></div></section><div class="wrap"><div class="dl-grid">'
          '<div class="dl-card"><div class="dl-os"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 5.5l7.6-1.1v7H3zM11.6 4.3L21 3v8.4h-9.4zM3 12.6h7.6v7l-7.6-1.1zM11.6 12.6H21V21l-9.4-1.3z"/></svg><h2>Windows</h2></div>'
          '<p class="dl-sub">Windows 10 及更高版本</p><div class="ver2"><span>最新版本 <code data-ver>读取中…</code></span><span>发布于 <span data-date>—</span></span></div>'
          '<div class="cta" style="justify-content:flex-start"><a class="btn blue" href="' + REL + '" data-dl data-releaselink rel="noopener">' + ic('dl') + '下载最新版</a><a class="btn glass" href="' + GH + '/releases" rel="noopener">全部版本</a></div>'
          '<div class="assets" id="assets"><div class="none">正在读取版本信息…</div></div>'
          '<ol class="steps"><li><span><b>下载</b>　选择上方的文件，保存到本地。</span></li><li><span><b>运行</b>　按文件类型安装或解压后启动，主界面会出现在屏幕上方。</span></li><li><span><b>接着用</b>　如果之前使用过 ClassIsland，原有的课表、自动化、插件与主题可直接沿用。</span></li></ol></div>'
          '<div class="dl-side"><div class="dl-card"><h3>Linux 与 macOS</h3><p>代码中保留了相关支持，但我们暂无测试环境，因此暂不提供官方构建。欢迎自行从源码构建，或帮助测试。</p></div>'
          '<div class="dl-card"><h3>更新与反馈</h3><p>新版本均发布在 GitHub Releases。遇到问题或有建议，欢迎提交 Issue。</p><div class="cta" style="justify-content:flex-start;margin-top:18px"><a class="btn glass sm" href="' + GH + '/issues" rel="noopener">反馈问题</a><a class="btn glass sm" href="/about.html">了解 ClassFabric</a></div></div></div></div>'
          '<div style="height:clamp(60px,9vw,120px)"></div></div></main>\n')
    return h + FOOT

# ------------------------------------------------------------------ about
def about():
    h = head('关于 ClassFabric — 与 ClassIsland 的关系、计划与常见问题', 'ClassFabric 是 ClassIsland 的个人修改版。了解它与上游的关系、从 ClassIsland 切换需要做什么、已完成与计划中的功能，以及常见问题。', '/about.html')
    h += navbar('about')
    h += ('<main><section class="phead"><div class="wrap"><h1>关于 ClassFabric</h1><p>它是什么，与 ClassIsland 是什么关系，已经做了什么，接下来想做什么。</p></div></section><div class="wrap"><div class="ab">'
          '<nav class="toc" aria-label="本页目录"><a href="#what">是什么</a><a href="#relation">与 ClassIsland 的关系</a><a href="#switch">如何切换</a><a href="#fit">适合谁</a><a href="#done">已经做了</a><a href="#planned">计划中</a><a href="#name">名字由来</a><a href="#join">参与贡献</a><a href="#faq">常见问题</a></nav><div class="prose">'
          '<section id="what"><h2>ClassFabric 是什么</h2><p>ClassFabric 是基于 HelloWRC 的 ClassIsland 二次开发的<strong>个人修改版</strong>。在保持积极同步上游最新特性的同时，融入来自个人与社区的修改，例如多语言、云功能、更好的自动化、更好的性能表现与更多功能。</p><p>其中一部分已经完成，另一部分仍处于规划阶段，详见下文「已经做了」与「计划中」。</p></section>'
          '<section id="relation"><h2>与 ClassIsland 的关系</h2><p>ClassFabric 不是 ClassIsland 的完美替代品，也不是它的竞品，而是在其基础上二次开发的版本。ClassIsland 的作者是 HelloWRC；ClassFabric 沿用上游的 GPL-3.0 开源协议，软件的「关于」页中也保留了上游的版权声明。</p></section>'
          '<section id="switch"><h2>从 ClassIsland 切换，需要做什么</h2><p>不需要复杂的前期工作。ClassFabric 的底层代码与上游保持一致，只需下载并安装，原有的课表、自动化、插件与主题即可接着使用。</p><div class="callout">我们正在把底层代码尽量还原到与上游一致，同时保持界面中显示的名称为 ClassFabric，目的就是让切换对你「无感」。</div></section>'
          '<section id="fit"><h2>适合谁，不适合谁</h2><p><strong>适合：</strong>想在 ClassIsland 生态上保持现有内容，又希望及时体验上游新功能的人；以及希望开箱即用，装完就能体验上游、社区与我们开发的各类新功能的人。</p><p><strong>不太适合：</strong>希望环境长期保持不变的人，或对稳定性有极高要求的场合。ClassFabric 会积极同步上游的更改，版本变化相对频繁。</p></section>'
          '<section id="done"><h2>已经做了什么</h2><ul><li><strong>紧跟上游</strong>：同步 ClassIsland 的新功能与修复。</li><li><strong>更多天气源</strong>：除小米天气外，新增 OpenWeather 与和风天气。</li><li><strong>多语言（实验中）</strong>：ClassIsland 的界面文字原本是写死的，我们已将其中大部分改为可翻译的形式，目前支持简体中文、繁體中文与 English，约完成 40%。仍有不少文字与界面需要适配，欢迎在 Crowdin 上参与翻译。</li><li><strong>更好的插件预览</strong>：插件市场的详情页可预览更多内容。</li></ul><p>想了解具体改动，可以查看 <a href="' + GH + '/commits/main" rel="noopener">GitHub 提交记录</a>。</p></section>'
          '<section id="planned"><h2>计划中</h2><p>以下内容仍在规划阶段，<strong>尚未可用</strong>。</p><div class="plan"><div><h4>云功能 · 远程提醒</h4><p>从远端向大屏发送提醒。</p></div>'
          '<div><h4>云功能 · 集中管理</h4><p>统一管理多台设备。上游暂未提供，社区项目 <a href="https://github.com/1sIancl/ClassislandControlHub" rel="noopener">ClassislandControlHub</a> 正在积极开发。</p></div>'
          '<div><h4>云功能 · 云端备份</h4><p>通过 SFTP、WebDAV、OpenList 等方式备份档案与配置。</p></div><div><h4>更好的自动化</h4><p>主要借助社区知名插件 SystemTools 实现。</p></div><div><h4>更好的性能表现</h4><p>持续优化。</p></div></div></section>'
          '<section id="name"><h2>名字由来</h2><p>ClassIsland 的 Island，来自 iOS 的「灵动岛」。ClassFabric 的 Fabric，则来自 Minecraft 社区知名的模组加载器 Fabric，寓意将社区与个人的功能连接起来。</p></section>'
          '<section id="join"><h2>参与贡献</h2><p>欢迎任何有价值的贡献：在 GitHub 提交 Issue 或 PR 即可。我们也会考虑定期将有意义的改动提交给上游，一起建设 ClassIsland 生态。</p><div class="cta" style="justify-content:flex-start"><a class="btn glass" href="' + GH + '" rel="noopener">GitHub 仓库</a><a class="btn glass" href="' + GH + '/issues" rel="noopener">反馈问题</a></div></section>'
          '<section id="faq" class="faq"><h2>常见问题</h2>'
          '<details><summary>支持 Linux 和 macOS 吗？</summary><p>目前仅提供 Windows 版本。代码中保留了相关支持，但我们暂无测试环境与精力维护，因此暂不提供官方构建。</p></details>'
          '<details><summary>有交流群吗？</summary><p>暂时没有。ClassIsland 现有的 QQ 频道与群属于上游项目，ClassFabric 的问题请直接在 GitHub 提交 Issue。</p></details>'
          '<details><summary>软件出现问题怎么办？</summary><p>可以先尝试内置的恢复模式：以安全模式启动、查看日志、恢复备份，必要时重置配置。仍无法解决，请在 GitHub 提交 Issue 并附上诊断信息。</p></details>'
          '<details><summary>它会取代 ClassIsland 吗？</summary><p>不会。ClassFabric 建立在 ClassIsland 之上，没有上游就没有它。可以把它看作一个「更早体验新功能，并带有额外改进」的选择。</p></details>'
          '<details><summary>开源协议是什么？</summary><p>GPL-3.0，与上游一致。ClassIsland 的版权归 HelloWRC，ClassFabric 的改动版权归各自贡献者。</p></details></section>'
          '</div></div></div></main>\n')
    return h + FOOT

for name, fn in (('index.html', home), ('download.html', download), ('about.html', about)):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(fn())
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>%s%s</loc></url>\n' % (SITE, p) for p in ('/', '/download.html', '/about.html')) + '</urlset>\n')
print('ok')
