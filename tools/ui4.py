# -*- coding: utf-8 -*-
from ui import ic

E = {}


def init(g):
    E.update(g)


def _isl_idle():
    return E['static_isl'](E['idle']('break', '56%', '78%', 3000)).replace('<div class="isl static"', '<div class="isl static on" data-sched')


def _step(i, n, tag, title, body, extra=''):
    return ('<div class="n5-tx" style="--r:%d"><div class="n5-no"><b>%02d</b><i></i><span>%02d</span></div><h3>%s</h3>%s%s</div>' % (i + 1, i + 1, n, title, body, extra))


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

    p4 = bare('<div class="vwin n5-win" style="left:60px;top:26px;width:1160px"><div class="app" data-app="settings" data-start="auto" data-h="590"></div></div>', 'vdk-set', 'tr4')

    rem_tabs = ('<div class="subs" id="remTabs">'
                '<button class="sub-i on" data-g="0">' + ic('bell') + '<div><h4>准备上课</h4><p>在上课前一段时间发出提醒。室内课程默认提前 60 秒，室外课程默认提前 600 秒。</p></div></button>'
                '<button class="sub-i" data-g="1">' + ic('school') + '<div><h4>上课</h4><p>在上课时发出提醒，并在主界面标出当前课程与剩余时间。</p></div></button>'
                '<button class="sub-i" data-g="2">' + ic('clock') + '<div><h4>课间休息</h4><p>在下课时发出提醒，显示本节课间的时长与下一节课。</p></div></button></div>')
    flow = '<div class="n5-flow"><span>当 <b data-tw>时间到了</b><i></i></span><span>若 <b>满足规则</b><i></i></span><span>就 <b>自动执行</b></span></div>'

    S = [
        ('#主界面', '直观的信息显示', '<p>自动直观地显示今日的课程安排与当前进行的课程，并支持通过「组件」自定义主界面上显示的内容。</p>', '', p0),
        ('#提醒', '醒目的提醒系统', '<p>在上课、下课等重要时间点发出醒目的提醒，提示语可以自行修改，并支持语音播报；放学提醒、天气预警和自动化行动同样可以通过它显示。</p>', rem_tabs, p1),
        ('#课表', '强大的课表系统', '<p>便捷地导入、编辑和调换课表。</p>',
         _subs([('cal', '灵活的课表启用规则', '每周、某一天或循环启用，支持多周轮换，到日期自动切换。'), ('clock', '时间与科目的自由定制', '不同课表使用不同时间表，科目可设置图标与主题色。'), ('edit', '简洁直观的编辑工具', '时间表以时间轴方式直接拖动调整。')]), p2),
        ('#换课', '为高效而生的换课', '<p>换课窗口专为快速调课而设计：从托盘一键打开，选中要调换的课程，再选替换科目，几秒钟完成，无需进入完整的档案编辑器。</p>',
         _subs([('swap', '当日与跨天都能换', '支持当日与跨天换课。可以只换这一次，也可以勾选「永久换课」。'), ('cal', '临时启用课表', '在当日或未来某一天临时启用另一个课表，应对调休与大调整。')]), p3),
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
    return ('<div class="wrap n5-sh"><div class="rv"><h3>%s</h3></div><div class="rv d1"><p>%s</p>%s</div></div>' % (title, desc, extra))


def chips(items):
    return '<div class="n5-cl">' + ''.join('<span style="--i:%d">%s</span>' % (i, t) for i, t in enumerate(items)) + '</div>'


def mix(panel_wall):
    inner = ('<div class="n5-mixin"><div class="n5-misl" data-wx-island aria-live="polite"></div>'
             '<div class="n5-mwin"><div class="app" data-app="settings" data-start="widgets" data-h="600" data-seed="文本=Hello World!" data-script="1"></div></div></div>')
    tpl = ('<template data-wx-tpl><span data-k="天气简报" class="wx">' + ic('sun') + '9℃</span>'
           '<span data-k="课程表" class="wsch" data-sched><span class="s p">语</span><span class="s p">数</span><span class="s p">英</span>'
           '<span class="cur">' + ic('clock') + '<span>课间休息</span><small>10:20-10:30</small></span><span class="sep"></span>'
           + ''.join('<span class="s">%s</span>' % c for c in '物化生历政地') + '</span></template>')
    out = split('#组件', '让主界面更多样', '主界面由「组件」搭配而成。点击或拖动下方组件库里的项目，上方的主界面会随之变化。')
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
    cs = ''.join('<div class="n5-ctl"><span class="n5-ci">%s</span><div><b>%s</b></div><input class="n5-rg" type="range" data-k="%s" %s aria-label="%s"></div>' % (ic(i), t, k, a, t) for k, i, t, d, a in ctl)
    cs += ('<div class="n5-ctl"><span class="n5-ci">Aa</span><div><b>字体</b></div>'
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
    GH, GHSVG = E['GH'], E['GHSVG']
    CR = 'https://zh.crowdin.com/project/classfabric'
    ST = 'https://github.com/Programmer-MrWang/SystemTools'
    IS = 'https://github.com/ClassIsland/ClassIsland/issues/'
    arr = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
    ln = ('<article class="n5-t w5 rv"><h4>让界面说你的语言</h4>'
          '<p>界面文字正在由写死改为可翻译的形式，目前支持简体中文、繁體中文与 English。翻译由 Crowdin 协作完成。</p>'
          '<div class="n5-tv"><div class="chips-row"><span class="chip on">简体中文</span><span class="chip">繁體中文</span><span class="chip">English</span></div>'
          '<a class="n5-ln" href="' + CR + '" rel="noopener">在 Crowdin 参与翻译' + arr + '</a></div></article>')
    wx = ('<article class="n5-t w7 rv d1"><h4>三个天气源，自己选</h4>'
          '<p>除内置的小米天气外，新增 OpenWeather 与和风天气（QWeather）。所选来源不可用时，可自动回退到小米天气，并可限制 API 用量。</p>'
          '<div class="n5-tv"><div class="n5-shot"><img src="/assets/img/grow-weather.webp" alt="设置页中的天气数据源：选择和风天气后出现 API Key 等选项" width="1020" height="235" loading="lazy"></div></div></article>')
    pv = ('<article class="n5-t w7 rv"><h4>插件说明，清爽统一</h4>'
          '<p>用 Markdig 清洗各插件各不相同的 README，以统一、美观的方式展示，并单独处理图片与 SVG。</p>'
          '<div class="n5-tv"><div class="n5-cmp" style="--p:50%"><img src="/assets/img/grow-cmp-ours.webp" alt="ClassFabric 中的 SystemTools 插件详情" width="808" height="374" loading="lazy">'
          '<img class="o" src="/assets/img/grow-cmp-orig.webp" alt="原版中的同一插件详情" width="808" height="374" loading="lazy">'
          '<span class="n5-cmpl a">原版</span><span class="n5-cmpl b">ClassFabric</span><i class="n5-cmph" aria-hidden="true"></i>'
          '<input type="range" min="0" max="100" value="50" aria-label="对比原版与 ClassFabric 的插件详情"></div></div></article>')
    ac = ('<article class="n5-t n5-stmt w5 rv d1"><h4>更多行动与触发器</h4>'
          '<p>实现参考了 SystemTools 插件的能力。</p>'
          '<div class="n5-tv"><div class="n5-big">75<em>+</em></div><div class="n5-cap">触发器 + 规则集 + 动作，合计 75+ 项</div>'
          '<a class="n5-ln" href="' + ST + '" rel="noopener">查看 SystemTools' + arr + '</a></div></article>')
    GITEE = ('<svg viewBox="0 0 1024 1024" aria-hidden="true"><path fill="#C71D23" d="M512 1024C229.222 1024 0 794.778 0 512S229.222 0 512 0s512 229.222 512 512-229.222 512-512 512zm259.149-568.883h-290.74a25.293 25.293 0 0 0-25.292 25.293l-.026 63.206c0 13.952 11.315 25.293 25.267 25.293h177.024c13.978 0 25.293 11.315 25.293 25.267v12.646a75.853 75.853 0 0 1-75.853 75.853h-240.23a25.293 25.293 0 0 1-25.267-25.293V417.203a75.853 75.853 0 0 1 75.827-75.853h353.946a25.293 25.293 0 0 0 25.267-25.292l.077-63.207a25.293 25.293 0 0 0-25.268-25.293H417.152a189.62 189.62 0 0 0-189.62 189.645V771.15c0 13.977 11.316 25.293 25.294 25.293h372.94a170.65 170.65 0 0 0 170.65-170.65V480.384a25.293 25.293 0 0 0-25.293-25.267z"/></svg>')
    ch = ('<article class="n5-t w5 rv"><h4>多通道下载与更新</h4>'
          '<p>除官方 PDCC 外，可从 GitHub 与 Gitee 下载更新。保留 PDCC 是为方便恢复原版，之后将提供自建 PDCC。</p>'
          '<div class="n5-tv"><div class="n5-src"><span>' + ic('cloud') + 'PDCC<small>官方 · 恢复原版</small></span><span>' + GHSVG.replace(' class="ghi"', '') + 'GitHub</span><span>' + GITEE + 'Gitee</span></div></div></article>')
    iss = ''.join('<li><a href="%s%s" rel="noopener"><code>#%s</code><span>%s</span>%s</a></li>' % (IS, n, n, s, ic('check')) for n, s in (('2032', '系统切换为深色模式后，天气简报的温度置空'), ('2039', '更改时间偏移后，以 cron 为触发器的自动化会执行两次')))
    steps = [('info', '社区反馈', '', '<ul class="n5-iss">' + iss + '</ul>'),
             ('bolt', '修复与优化', '', ''),
             ('sync', '随更新送达', '', '')]
    flow = '<ol class="n5-fflow">' + ''.join('<li style="--i:%d"><i class="n5-fnd">%s</i><div><b>%s</b>%s%s</div></li>' % (i, ic(ic_), h, ('<p>%s</p>' % d) if d else '', x) for i, (ic_, h, d, x) in enumerate(steps)) + '</ol>'
    fx = ('<article class="n5-t w7 rv d1 n5-fix"><h4>大量修复与优化</h4>'
          '<p>听从社区意见，修复并优化了许多问题。</p>' + flow +
          '<a class="n5-ln" href="' + GH + '/releases" rel="noopener">查看全部更新日志' + arr + '</a></article>')
    jn = ('<div class="n5-join rv"><div><b>欢迎参与共建</b></div>'
          '<div class="n5-btns"><a class="btn glass" href="' + GH + '/issues" rel="noopener">反馈问题</a><a class="btn glass" href="' + GH + '/pulls" rel="noopener">提交 PR</a></div></div>')
    return ('<section class="sec n5-grow" id="grow"><div class="wrap"><h2 class="claim rv">一款<span class="g">不断增强</span>的大屏课表软件</h2>'
            '<div class="n5-bento">' + ln + wx + pv + ac + ch + fx + '</div>' + jn + '</div></section>\n')


def final(btns_dl, btns_more):
    rows = [('monitor', '系统', 'Windows 10 / 11'), ('plug', '运行时', '部分版本需要 .NET 10 桌面运行时'), ('doc', '开源协议', 'GPL-3.0'), ('sync', '最新版本', '<b data-ver class="sk"></b>')]
    li = ''.join('<li>%s<span>%s</span><b>%s</b></li>' % (ic(i), k, v) for i, k, v in rows)
    return ('<section class="n5-fin"><div class="wrap"><div class="n5-fc rv"><div class="n5-fl">'
            '<img src="/assets/img/icon-180.png" alt="" width="72" height="72"><h2>立即体验<br><span class="g">ClassFabric</span></h2><p>更多功能留给您自行探索！</p>'
            '<div class="cta">' + btns_dl + btns_more + '</div></div>'
            '<div class="n5-fr"><h3>开始之前</h3><ul>' + li + '</ul></div></div></div></section>\n')


def sync(c_sync, c_mig, c_enh, panel_wall):
    T = [('#同步', '积极同步上游特性', 'ClassIsland 的新功能与修复，会尽快同步到 ClassFabric。', c_sync, '30%', '36%'),
         ('#迁移', '无感切换，沿用现有配置', '底层代码与上游保持一致。原有的课表、自动化、插件与主题，安装后即可继续使用。', c_mig, '62%', '30%'),
         ('#增强', '来自社区与我们的增强', '在上游之上加入更多天气源、多语言支持（实验中）与更好的插件预览，并将持续扩充。', c_enh, '78%', '58%')]
    tabs = ''.join('<button type="button" class="n4-swt%s" role="tab" aria-selected="%s" data-i="%d"><h3>%s</h3><div class="n4-swd"><p>%s</p></div><i class="n4-bar"><b></b></i></button>'
                   % (' on' if i == 0 else '', 'true' if i == 0 else 'false', i, t[1], t[2]) for i, t in enumerate(T))
    panes = ''.join('<div class="n4-swp%s" role="tabpanel" data-i="%d">%s</div>' % (' on' if i == 0 else '', i, panel_wall('<div class="fstack">' + t[3] + '</div>', t[4], t[5], '190%', 'pad')) for i, t in enumerate(T))
    return ('<section class="sec n4-sw" id="sync"><div class="wrap"><h2 class="claim rv">一款<span class="g">紧跟上游</span>的大屏课表软件</h2>'
            '<div class="n4-swc rv" data-sw><div class="n4-swl" role="tablist" aria-label="紧跟上游">' + tabs + '</div><div class="n4-swv">' + panes + '</div></div></div></section>\n')
