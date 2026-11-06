# -*- coding: utf-8 -*-
from ui import ic

E = {}


def init(g):
    E.update(g)


def _isl_idle():
    return E['static_isl'](E['idle']('break', '56%', '78%', 3000)).replace('<div class="isl static"', '<div class="isl static on"')


def _step(i, n, tag, tcls, title, body, extra=''):
    return ('<div class="n4-tx"><div class="n4-no"><b>%02d</b><i></i><span>%02d</span></div><span class="tag %s">%s</span><h3>%s</h3>%s%s</div>' % (i, n, tcls, tag, title, body, extra))


def _subs(items):
    return '<div class="subs">' + ''.join('<div class="sub-i">%s<div><h4>%s</h4><p>%s</p></div></div>' % (ic(i), t, d) for i, t, d in items) + '</div>'


def stage():
    vdesk, tray_menu, ui2, REM_STATES, fit = E['vdesk'], E['tray_menu'], E['ui2'], E['REM_STATES'], E['fit']
    bare = lambda inner, cls, tid, extra='': vdesk(inner, cls, 1280, 720, 680, 780, extra, tid)

    row2 = ('<div class="n4-r2"><div class="isl static"><span data-now="time">00:00:00</span></div>'
            '<div class="isl static">' + ic('sun') + '&nbsp;9℃</div>'
            '<div class="isl static">' + ic('timer') + '&nbsp;<span data-cd>元旦</span></div></div>')
    annos = ''.join('<div class="n4-anno" data-t="%s" style="--i:%d"><span>%s</span></div>' % (t, i, s) for i, (t, s) in enumerate([
        ('.wx', '天气与日期'), ('.s.p', '已上完的课'), ('.cur', '当前课程与剩余时间'), ('.sep + .s', '之后的课程')]))
    p0 = bare('<div class="visl"><div class="isl-stack">' + _isl_idle() + '</div></div><div class="visl r2">' + row2 + '</div>' + annos, 'vdk-main', 'tr0')

    p1 = bare('<div class="visl"><div class="isl-stack" data-demo="rem" id="remIsl">' + REM_STATES + '</div></div>'
              '<div class="vwin n4-win" style="left:80px;top:122px;width:1120px"><div class="app" data-app="settings" data-start="remind" data-h="490"></div></div>', 'vdk-set', 'tr1')

    p2 = bare('<div class="vwin">' + ui2.editor_app(seed='real') + '</div>', 'vdk-bare', 'tr2').replace('<div class="vtask">', '<div class="vtask" hidden>', 1)

    p3 = vdesk('<div class="vwin" data-vwin="swap"><div class="sw2 w" data-app="swap" data-modal="1"></div></div><div class="vtray-menu" data-vmenu>' + tray_menu() + '</div>', 'vdk-swap', 800, 500, 720, 520, ' data-vtray="swap"', 'swTray')
    p3 += '<p class="vcap">点击右下角的托盘图标，选择「换课…」，即可从托盘打开独立的换课窗口。</p>'

    p4 = bare('<div class="vwin n4-win" style="left:60px;top:26px;width:1160px"><div class="app" data-app="settings" data-start="auto" data-h="590"></div></div>', 'vdk-set', 'tr4')

    rem_tabs = ('<div class="subs" id="remTabs">'
                '<button class="sub-i on" data-g="0">' + ic('bell') + '<div><h4>准备上课</h4><p>在上课前一段时间发出提醒。室内课程默认提前 60 秒，室外课程默认提前 600 秒。</p></div></button>'
                '<button class="sub-i" data-g="1">' + ic('school') + '<div><h4>上课</h4><p>在上课时发出提醒，并在主界面标出当前课程与剩余时间。</p></div></button>'
                '<button class="sub-i" data-g="2">' + ic('clock') + '<div><h4>课间休息</h4><p>在下课时发出提醒，显示本节课间的时长与下一节课。</p></div></button></div>')
    flow = '<div class="n4-flow"><span>当 <b class="f1">时间到了</b></span><i></i><span>若 <b class="f2">满足规则</b></span><i></i><span>就 <b class="f3">自动执行</b></span></div>'

    S = [
        ('#主界面', '', '直观的信息显示', '<p>自动直观地显示今日的课程安排与当前进行的课程，并支持通过「组件」自定义主界面上显示的内容。</p>', '', p0),
        ('#提醒', 'o', '醒目的提醒系统', '<p>在上课、下课等重要时间点发出醒目的提醒，提示语可以自行修改，并支持语音播报；放学提醒、天气预警和自动化行动同样可以通过它显示。</p>', rem_tabs, p1),
        ('#课表', 'p', '强大的课表系统', '<p>便捷地导入、编辑和调换课表。点击窗口上方的标签页，试试看。</p>',
         _subs([('cal', '灵活的课表启用规则', '每周、某一天或循环启用，支持多周轮换，到日期自动切换。'), ('clock', '时间与科目的自由定制', '不同课表使用不同时间表，科目可设置图标与主题色。'), ('edit', '简洁直观的编辑工具', '时间表以时间轴方式直接拖动调整。')]), p2),
        ('#调课', 'gr', '提前调整课程', '<p>支持当日与跨天换课，灵活应对调课情景。可以只换这一次，也可以勾选「永久换课」。</p>',
         _subs([('swap', '临时启用课表', '在当日或未来某一天临时启用另一个课表，应对调休与换课。'), ('import', '从其它软件导入课表', '支持直接导入其它课表软件的课表信息，也支持从 CSES 导入。')]), p3),
        ('#自动化', '', '智能的自动行为', '<p>让 ClassFabric 在特定的时间节点执行特定的操作，比如切换组件配置、运行程序、显示提醒。简单来说，就是「当 XX 发生」，并且「满足 XX 规则」时「做什么」。</p>', flow, p4),
    ]
    n = len(S)
    arts = ''.join('<article class="n4-stp" data-i="%d">%s<div class="n4-pn">%s</div></article>' % (i, _step(i + 1, n, *s[:5]), s[5]) for i, s in enumerate(S))
    return ('<section class="sec light n4-stg" id="features"><div class="wrap"><h2 class="claim rv">一款<span class="g">功能强</span>的大屏课表软件</h2></div>'
            '<div class="n4-stage wrapw">' + arts + '</div></section>\n')


def chips(items):
    return '<div class="n4-cl">' + ''.join('<span style="--i:%d">%s</span>' % (i, t) for i, t in enumerate(items)) + '</div>'


def split(tag, tcls, title, desc, extra=''):
    return ('<div class="wrap n4-sh"><div class="rv"><span class="tag %s">%s</span><h3>%s</h3></div><div class="rv d1"><p>%s</p>%s</div></div>' % (tcls, tag, title, desc, extra))


def custom(bigmq, panel_wall, themes_html, plugins):
    wid = panel_wall('<div style="padding:3.5% 3%"><div class="app" data-app="settings" data-start="widgets" data-h="600"></div></div>', '8%', '44%', '230%', '')
    plg = panel_wall('<div style="padding:3.5% 3%"><div class="app" data-app="settings" data-start="plugins" data-h="640"></div></div>', '20%', '20%', '230%', '')
    out = bigmq(['组件', '主题', '插件', '自动化', '外观'], ['拖动', '搭配', '安装', '触发', '个性化'])
    out += '<section class="sec n4-cus" id="custom"><div class="wrap"><h2 class="claim rv">一款<span class="g">可定制</span>的大屏课表软件</h2></div>'
    out += split('#组件', 'p', '使用组件搭配你的主界面', '通过「组件」自由定制主界面上显示的内容，并支持轮播、滚动、分组与堆叠容器。进入「编辑模式」，可以直接在主界面上拖动调整组件。',
                 chips(['课表', '日期', '时钟', '天气', '倒计时', '轮播', '滚动', '分组', '堆叠']))
    out += '<div class="n4-wide crop rv">' + wid + '</div>'
    out += '<div class="wrap">' + themes_html + '</div>'
    out += '<div class="wrap">' + plugins + '</div>'
    out += split('#插件', 'gr', '丰富的插件生态', '支持通过安装插件扩展应用功能，在应用内的插件市场即可浏览、搜索与安装。ClassIsland 的插件可直接使用，ClassFabric 还让插件详情页能预览更多内容。')
    out += '<div class="n4-wide crop rv">' + plg + '</div>'
    return out + '</section>\n'


def final(btns_dl, btns_more):
    return ('<section class="n4-fin"><div class="n4-fbg" aria-hidden="true"></div><div class="wrap">'
            '<div class="n4-fisl rv" aria-hidden="true"><div class="isl-stack" data-demo="cta">' + E['HERO_STATES'] + '</div></div>'
            '<h2 class="rv d1">立即体验 ClassFabric</h2><p class="rv d2">更多功能留给您自行探索！</p>'
            '<div class="cta rv d2">' + btns_dl + btns_more + '</div>'
            '<p class="n4-note rv d3">支持在 Windows 10/11 上运行　·　最新版本 <b data-ver class="sk"></b>　·　GPL-3.0 开源</p></div></section>\n')
