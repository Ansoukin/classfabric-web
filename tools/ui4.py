# -*- coding: utf-8 -*-
from ui import ic

E = {}


def init(g):
    E.update(g)


def _isl_idle():
    return E['static_isl'](E['idle']('break', '56%', '78%', 3000)).replace('<div class="isl static"', '<div class="isl static on"')


def _step(i, n, tag, title, body, extra=''):
    return ('<div class="n5-tx" style="--r:%d"><div class="n5-no"><b>%02d</b><i></i><span>%02d</span></div><span class="tag">%s</span><h3>%s</h3>%s%s</div>' % (i + 1, i + 1, n, tag, title, body, extra))


def _subs(items):
    return '<div class="subs">' + ''.join('<div class="sub-i">%s<div><h4>%s</h4><p>%s</p></div></div>' % (ic(i), t, d) for i, t, d in items) + '</div>'


def stage():
    vdesk, tray_menu, ui2, REM_STATES = E['vdesk'], E['tray_menu'], E['ui2'], E['REM_STATES']
    bare = lambda inner, cls, tid, extra='': vdesk(inner, cls, 1280, 720, 680, 780, extra, tid)

    row2 = ('<div class="n5-r2"><div class="isl static"><span data-now="time">00:00:00</span></div>'
            '<div class="isl static">' + ic('sun') + '&nbsp;9℃</div>'
            '<div class="isl static">' + ic('timer') + '&nbsp;<span data-cd>元旦</span></div></div>')
    annos = ''.join('<div class="n5-anno" data-t="%s" style="--i:%d"><span>%s</span></div>' % (t, i, s) for i, (t, s) in enumerate([
        ('.wx', '天气与日期'), ('.s.p', '已上完的课'), ('.cur', '当前课程与剩余时间'), ('.sep + .s', '之后的课程')]))
    p0 = bare('<div class="visl"><div class="isl-stack">' + _isl_idle() + '</div></div><div class="visl r2">' + row2 + '</div>' + annos, 'vdk-main', 'tr0')

    p1 = bare('<div class="visl"><div class="isl-stack" data-demo="rem" id="remIsl">' + REM_STATES + '</div></div>'
              '<div class="vwin n5-win" style="left:80px;top:122px;width:1120px"><div class="app" data-app="settings" data-start="remind" data-h="490"></div></div>', 'vdk-set', 'tr1')

    p2 = bare('<div class="vwin">' + ui2.editor_app(seed='real') + '</div>', 'vdk-bare', 'tr2').replace('<div class="vtask">', '<div class="vtask" hidden>', 1)

    p3 = vdesk('<div class="vwin" data-vwin="swap"><div class="sw2 w" data-app="swap" data-modal="1"></div></div><div class="vtray-menu" data-vmenu>' + tray_menu() + '</div>', 'vdk-swap', 800, 500, 720, 520, ' data-vtray="swap"', 'swTray')
    p3 += '<p class="vcap">点击右下角的托盘图标，选择「换课…」，即可从托盘打开独立的换课窗口。</p>'

    p4 = bare('<div class="vwin n5-win" style="left:60px;top:26px;width:1160px"><div class="app" data-app="settings" data-start="auto" data-h="590"></div></div>', 'vdk-set', 'tr4')

    rem_tabs = ('<div class="subs" id="remTabs">'
                '<button class="sub-i on" data-g="0">' + ic('bell') + '<div><h4>准备上课</h4><p>在上课前一段时间发出提醒。室内课程默认提前 60 秒，室外课程默认提前 600 秒。</p></div></button>'
                '<button class="sub-i" data-g="1">' + ic('school') + '<div><h4>上课</h4><p>在上课时发出提醒，并在主界面标出当前课程与剩余时间。</p></div></button>'
                '<button class="sub-i" data-g="2">' + ic('clock') + '<div><h4>课间休息</h4><p>在下课时发出提醒，显示本节课间的时长与下一节课。</p></div></button></div>')
    flow = '<div class="n5-flow"><span>当 <b>时间到了</b></span><i></i><span>若 <b>满足规则</b></span><i></i><span>就 <b>自动执行</b></span></div>'

    S = [
        ('#主界面', '直观的信息显示', '<p>自动直观地显示今日的课程安排与当前进行的课程，并支持通过「组件」自定义主界面上显示的内容。</p>', '', p0),
        ('#提醒', '醒目的提醒系统', '<p>在上课、下课等重要时间点发出醒目的提醒，提示语可以自行修改，并支持语音播报；放学提醒、天气预警和自动化行动同样可以通过它显示。</p>', rem_tabs, p1),
        ('#课表', '强大的课表系统', '<p>便捷地导入、编辑和调换课表。点击窗口上方的标签页，试试看。</p>',
         _subs([('cal', '灵活的课表启用规则', '每周、某一天或循环启用，支持多周轮换，到日期自动切换。'), ('clock', '时间与科目的自由定制', '不同课表使用不同时间表，科目可设置图标与主题色。'), ('edit', '简洁直观的编辑工具', '时间表以时间轴方式直接拖动调整。')]), p2),
        ('#调课', '提前调整课程', '<p>支持当日与跨天换课，灵活应对调课情景。可以只换这一次，也可以勾选「永久换课」。</p>',
         _subs([('swap', '临时启用课表', '在当日或未来某一天临时启用另一个课表，应对调休与换课。'), ('import', '从其它软件导入课表', '支持直接导入其它课表软件的课表信息，也支持从 CSES 导入。')]), p3),
        ('#自动化', '智能的自动行为', '<p>让 ClassFabric 在特定的时间节点执行特定的操作，比如切换组件配置、运行程序、显示提醒。简单来说，就是「当 XX 发生」，并且「满足 XX 规则」时「做什么」。</p>', flow, p4),
    ]
    n = len(S)
    arts = ''.join('<article class="n5-ch%s" data-i="%d">%s<div class="n5-pn">%s</div></article>' % (' on' if i == 0 else '', i, _step(i, n, *s[:4]), s[4]) for i, s in enumerate(S))
    return ('<section class="sec n5-stg" id="features"><div class="wrap"><h2 class="claim rv">一款<span class="g">功能强</span>的大屏课表软件</h2></div>'
            '<div class="n5-stage wrapw" style="--n:%d">' % n + arts + '</div></section>\n')


def show(ST):
    wrap = lambda x: '<div class="n5-ln-i"><div class="isl-stack">' + x + '</div></div>'
    r1 = ''.join(wrap(x) for x in ST[:4])
    r2 = ''.join(wrap(x) for x in ST[4:])
    return ('<section class="sec n5-show" id="states"><div class="wrap"><h2 class="claim rv">上课与下课，<span class="g">一目了然</span></h2></div>'
            '<div class="wrapw"><div class="n5-band rv" role="img" aria-label="灵动岛的各种状态"><div class="n5-lane"><div class="trk">' + r1 * 2 + '</div></div>'
            '<div class="n5-lane rev"><div class="trk">' + r2 * 2 + '</div></div></div>'
            '<figure class="vid n5-vid rv" id="vid"><video muted loop playsinline preload="none" data-src="https://www.classisland.tech/assets/notification-demo.web-Os7FSQPD.mp4" aria-label="提醒演示视频"></video></figure></div></section>\n')


def split(tag, title, desc, extra=''):
    return ('<div class="wrap n5-sh"><div class="rv"><span class="tag">%s</span><h3>%s</h3></div><div class="rv d1"><p>%s</p>%s</div></div>' % (tag, title, desc, extra))


def chips(items):
    return '<div class="n5-cl">' + ''.join('<span style="--i:%d">%s</span>' % (i, t) for i, t in enumerate(items)) + '</div>'


def mix(panel_wall):
    inner = ('<div class="n5-mixin"><div class="n5-misl" data-wx-island aria-live="polite"></div>'
             '<div class="n5-mwin"><div class="app" data-app="settings" data-start="widgets" data-h="600" data-seed="课程表,天气简报"></div></div></div>')
    tpl = ('<template data-wx-tpl><span data-k="天气简报" class="wx">' + ic('sun') + '9℃</span>'
           '<span data-k="课程表" class="wsch"><span class="s p">语</span><span class="s p">数</span><span class="s p">英</span>'
           '<span class="cur">' + ic('clock') + '<span>课间休息</span><small>10:20-10:30</small></span><span class="sep"></span>'
           + ''.join('<span class="s">%s</span>' % c for c in '物化生历政地') + '</span></template>')
    out = split('#组件', '让主界面更多样', '主界面由「组件」搭配而成：文本、日期、时钟、天气、课表、倒计时，以及轮播、滚动、分组与堆叠容器。下方就是真实的组件页，点击或拖动组件库里的项目，上方的主界面会随之伸缩。')
    out += '<div class="n5-wide rv n5-mix">' + panel_wall(inner + tpl, '8%', '44%', '230%', '') + '</div>'
    return out


def themes():
    TH = [('classic', '经典', '单行岛条，天气、日期、课程与倒计时同排显示。', False),
          ('fluent', 'Fluent', '分体主界面，日期、时间与倒计时另起一行。', True),
          ('rect', 'Rectangles', '方块背景之上的醒目岛条。', False)]
    rows = ''.join(
        ('<button type="button" class="n5-th%s" data-th="%s" aria-pressed="%s"><span class="n5-thx"><span class="n5-thn"><h4>%s</h4><span class="bdg blue sm"><i class="dot"></i>内置</span></span><span class="n5-thd">%s</span></span>'
         '<span class="n5-thp"><img src="/assets/img/theme-%s-bar.webp" alt="%s 主题的主界面效果" width="656" height="119" loading="lazy" decoding="async"></span>'
         '<span class="tg%s"><i></i></span></button>') % (' on' if on else '', k, 'true' if on else 'false', n, d, k, n, ' on' if on else '')
        for k, n, d, on in TH)
    ctl = [('s', 'sliders', '界面缩放', '主界面的缩放大小', 'min="70" max="150" value="100"'),
           ('o', 'sliders', '背景不透明度', '主界面背景的不透明度', 'min="0" max="100" value="80"'),
           ('r', 'roundsq', '圆角半径', '调至最大时，左右边缘为半圆', 'min="0" max="100" value="37"')]
    cs = ''.join('<div class="n5-ctl"><span class="n5-ci">%s</span><div><b>%s</b><small>%s</small></div><input class="n5-rg" type="range" data-k="%s" %s aria-label="%s"></div>' % (ic(i), t, d, k, a, t) for k, i, t, d, a in ctl)
    cs += ('<div class="n5-ctl"><span class="n5-ci">Aa</span><div><b>字体</b><small>更换主界面使用的字体</small></div>'
           '<div class="n5-seg" role="group" aria-label="字体"><button type="button" class="on" data-ff="sans">默认</button><button type="button" data-ff="serif">衬线</button><button type="button" data-ff="mono">等宽</button></div></div>')
    live = ('<div class="n5-live"><div class="n5-tisl"><div class="isl-stack">' + _isl_idle() + '</div></div></div>')
    return ('<div class="wrap n5-thm">' + split('#主题', '自由的主题系统', '内置经典、Fluent 与 Rectangles 三套主题，并支持调整界面缩放、背景透明度、圆角与字体，高度个性化你的界面。')
            + '<div class="n5-ths rv">' + rows + '</div>'
            '<div class="n5-tune rv"><div class="n5-ctls">' + cs + '</div>' + live + '</div></div>')


def plugins():
    P = E['PLUGINS']
    card = lambda p: ('<a class="n5-pc" href="https://github.com/%s" target="_blank" rel="noopener"><img src="https://cdn.jsdelivr.net/gh/%s" alt="" loading="lazy" width="48" height="48"><div><b>%s</b><small>%s</small></div></a>' % (p[1], p[2], p[0], p[3]))
    a = ''.join(card(p) for p in P)
    b = ''.join(card(p) for p in reversed(P))
    return ('<div class="n5-plg rv" aria-label="社区插件"><div class="n5-lane"><div class="trk">' + a * 2 + '</div></div>'
            '<div class="n5-lane rev"><div class="trk">' + b * 2 + '</div></div></div>')


def custom(bigmq, panel_wall):
    out = bigmq(['组件', '主题', '插件', '自动化', '外观'], ['拖动', '搭配', '安装', '触发', '个性化'])
    out += '<section class="sec n5-cus" id="custom"><div class="wrap"><h2 class="claim rv">一款<span class="g">可定制</span>的大屏课表软件</h2></div>'
    out += mix(panel_wall)
    out += themes()
    out += split('#插件', '丰富的插件生态', '支持通过安装插件扩展应用功能，在应用内的插件市场即可浏览、搜索与安装。ClassIsland 的插件可直接使用，ClassFabric 还让插件详情页能预览更多内容。')
    out += plugins()
    plg = panel_wall('<div style="padding:3.5% 3%"><div class="app" data-app="settings" data-start="plugins" data-h="640"></div></div>', '20%', '20%', '230%', '')
    out += '<div class="n5-wide crop rv">' + plg + '</div>'
    return out + '</section>\n'


def grow():
    smask, tray_menu, GH, GHSVG = E['smask'], E['tray_menu'], E['GH'], E['GHSVG']
    wx = ('<div class="n5-t w5 rv d1"><h4>更多天气源</h4><p>除 ClassIsland 内置的小米天气外，新增 OpenWeather 与和风天气（QWeather），可自行选择天气来源。</p>'
          '<div class="n5-tv"><div class="chips-row"><span class="chip on">小米天气 · 内置</span><span class="chip">OpenWeather</span><span class="chip">和风天气</span></div></div></div>')
    ln = ('<div class="n5-t w7 rv"><h4>多语言 <small class="n5-exp">实验中</small></h4><p>界面文字正在由写死改为可翻译的形式，目前支持简体中文、繁體中文与 English，翻译通过 Crowdin 协作。仍有不少文字与界面需要适配，欢迎参与。</p>'
          '<div class="n5-tv"><div class="chips-row"><span class="chip on">简体中文</span><span class="chip">繁體中文</span><span class="chip">English</span></div><div class="bar40" id="bar40"><i></i></div><div class="n5-cap">适配进度 约 40%</div></div></div>')
    pv = ('<div class="n5-t rv"><h4>更好的插件预览</h4><p>插件市场的详情页可以预览更多内容，安装之前就能看清插件的样子。</p><div class="n5-tv"><div class="pvw">'
          '<div class="pvh"><span class="pva"><img src="https://cdn.jsdelivr.net/gh/HelloWRC/GrantUiAccess@master/GrantUiAccess/icon.png" alt="" width="46" height="46"></span><div><b>UIAccess 提权</b><small>2.0.0.0 · HelloWRC, Doubx690i</small></div><span class="pvb">安装</span></div>'
          '<div class="pvt"><span class="on">详情</span><span>版本</span><span>依赖</span></div>'
          '<div class="pvmd"><h5>UIAccess 提权</h5><p>为 ClassIsland 提升 UIAccess 令牌，使其可以置顶到全屏 UWP 应用和系统界面上。</p>'
          '<div class="pvimg"><div class="isl-stack">' + smask('上课', 'atom') + '</div></div></div></div></div></div>')
    tray = ('<div class="n5-t rv d1"><h4>一切，都在托盘里</h4><p>右键托盘图标，即可编辑档案、换课、加载临时课表，或打开应用设置。</p><div class="n5-tv"><div class="n5-tray"><div class="tzoom">' + tray_menu() + '</div></div></div></div>')
    jn = ('<div class="n5-t rv d2"><h4>欢迎参与共建</h4><p>欢迎在 GitHub 提交 Issue 与 PR；有价值的改动，我们也会考虑定期提交回上游，一起建设 ClassIsland 生态。</p>'
          '<div class="n5-tv"><div class="n5-repo"><div class="rh">' + GHSVG.replace(' class="ghi"', '') + '<b>Ansoukin/ClassFabric</b></div><p>ClassIsland 的个人修改版班级大屏课表</p><div class="rc"><span>GPL-3.0</span><span>Windows</span><span>欢迎 PR</span></div></div>'
          '<div class="n5-btns"><a class="btn glass" href="' + GH + '/issues" rel="noopener">反馈问题</a><a class="btn glass" href="' + GH + '/pulls" rel="noopener">提交 PR</a></div></div></div>')
    return ('<section class="sec n5-grow" id="grow"><div class="wrap"><h2 class="claim rv">一款<span class="g">不断增强</span>的大屏课表软件</h2>'
            '<div class="n5-bento">' + ln + wx + pv + tray + jn + '</div></div></section>\n')


def final(btns_dl, btns_more):
    rows = [('monitor', '系统', 'Windows 10 / 11'), ('plug', '运行时', '部分版本需要 .NET 10 桌面运行时'), ('doc', '开源协议', 'GPL-3.0'), ('sync', '最新版本', '<b data-ver class="sk"></b>')]
    li = ''.join('<li>%s<span>%s</span><b>%s</b></li>' % (ic(i), k, v) for i, k, v in rows)
    return ('<section class="n5-fin"><div class="wrap"><div class="n5-fc rv"><div class="n5-fl">'
            '<img src="/assets/img/icon-180.png" alt="" width="72" height="72"><h2>立即体验 ClassFabric</h2><p>更多功能留给您自行探索！</p>'
            '<div class="cta">' + btns_dl + btns_more + '</div></div>'
            '<div class="n5-fr"><h3>开始之前</h3><ul>' + li + '</ul><p>原有的课表、自动化、插件与主题可直接沿用。</p></div></div></div></section>\n')


def sync(c_sync, c_mig, c_enh, panel_wall):
    T = [('#同步', '积极同步上游特性', 'ClassIsland 的新功能与修复，会尽快同步到 ClassFabric。', c_sync, '30%', '36%'),
         ('#迁移', '无感切换，沿用现有配置', '底层代码与上游保持一致。原有的课表、自动化、插件与主题，安装后即可继续使用。', c_mig, '62%', '30%'),
         ('#增强', '来自社区与我们的增强', '在上游之上加入更多天气源、多语言支持（实验中）与更好的插件预览，并将持续扩充。', c_enh, '78%', '58%')]
    tabs = ''.join('<button type="button" class="n4-swt%s" role="tab" aria-selected="%s" data-i="%d"><span class="tag">%s</span><h3>%s</h3><div class="n4-swd"><p>%s</p></div><i class="n4-bar"><b></b></i></button>'
                   % (' on' if i == 0 else '', 'true' if i == 0 else 'false', i, t[0], t[1], t[2]) for i, t in enumerate(T))
    panes = ''.join('<div class="n4-swp%s" role="tabpanel" data-i="%d">%s</div>' % (' on' if i == 0 else '', i, panel_wall('<div class="fstack">' + t[3] + '</div>', t[4], t[5], '190%', 'pad')) for i, t in enumerate(T))
    return ('<section class="sec n4-sw" id="sync"><div class="wrap"><h2 class="claim rv">一款<span class="g">紧跟上游</span>的大屏课表软件</h2>'
            '<div class="n4-swc rv" data-sw><div class="n4-swl" role="tablist" aria-label="紧跟上游">' + tabs + '</div><div class="n4-swv">' + panes + '</div></div></div></section>\n')
