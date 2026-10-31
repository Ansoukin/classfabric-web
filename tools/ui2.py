# -*- coding: utf-8 -*-
"""可交互、可响应式的软件界面复刻（设置窗口）。静态 HTML，交互在 assets/js/apps.js。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import ic, tg, cb, pg_auto, pg_plugins, pg_themes, titlebar, TITLE_ISL

def sc(icon, title, desc='', trail='', cls=''):
    return '<div class="sc %s"><span style="width:22px;display:grid;place-items:center">%s</span><div class="tx"><b>%s</b>%s</div>%s</div>' % (cls, ic(icon) if icon else '', title, ('<span>%s</span>' % desc) if desc else '', trail)

def combo(text, w=120, icon='', opts=''):
    return '<span class="sel" style="min-width:%dpx"%s>%s<span class="v">%s</span>%s</span>' % (w, (' data-o="%s"' % opts) if opts else '', ic(icon) if icon else '', text, ic('chev'))

def slider(v):
    return '<span class="sld" data-sld><i style="width:%d%%"></i><b style="left:%d%%"></b></span>' % (v, v)

def num(v, w=150):
    return '<span class="num" style="min-width:%dpx"><span data-edit contenteditable="true" spellcheck="false">%s</span><em><i data-s="1">%s</i><i data-s="-1">%s</i></em></span>' % (w, v, ic('chev').replace('<path d="M6 9l6 6 6-6"/>', '<path d="M6 15l6-6 6 6"/>'), ic('chev'))

def field(label, value, disabled=False):
    return '<div class="fld2"><label>%s</label><div class="inp" contenteditable="true" spellcheck="false">%s</div></div>' % (label, value)

def exp(icon, title, desc, body, on=True, open_=True, tgl=True):
    return ('<div class="exp%s"><div class="eh">%s<div class="tx"><b>%s</b><span>%s</span></div>%s<span class="car">%s</span></div><div class="eb">%s</div></div>' %
            (' open' if open_ else '', ic(icon), title, desc, tg(on) if tgl else '', ic('chev'), body))

EMPTY = '<div class="empty"><svg viewBox="0 0 48 48"><rect x="6" y="6" width="36" height="36" rx="9" stroke-dasharray="9 7"/></svg><b>啥都没有</b></div>'

# ---------------------------------------------------------------- 提醒
def page_remind():
    prov = [('school', '上下课提醒', '在准备上课、上课和下课时发出醒目提醒，并预告下一节课程。'), ('power', '放学提醒', '在当天的课程结束后发出提醒。'),
            ('cloud', '天气预警', '当有降雨或者极端天气时发出提醒。'), ('bolt', '行动提醒', '显示由行动发出的提醒。')]
    chan = [('bell', '准备上课提醒', '在上课前指定时间发出提醒。'), ('school', '上课提醒', '在上课时发出提醒。'), ('clock', '下课提醒', '在下课时发出提醒。')]
    rows = ''
    for i, (ico, t, d) in enumerate(prov):
        rows += '<div class="prov%s" data-prov="%d">%s<div class="tx"><b>%s</b><span>%s</span></div></div>' % ('', i, ic(ico), t, d)
        if i == 0:
            rows += ('<div class="chan" hidden><div class="ch-h" data-chan>提醒渠道<span class="car">%s</span></div><div class="ch-b">' % ic('chev') +
                     ''.join('<div class="ci%s">%s<div class="tx"><b>%s</b><span>%s</span></div></div>' % (' on' if k == 0 else '', ic(a), b, c) for k, (a, b, c) in enumerate(chan)) + '</div></div>')
    left = ('<div class="rcol">' + sc('bell', '启用提醒', '启用提醒后，将会在对重要事件发出醒目提醒。拖动提醒提供方以调整对应类型提醒的优先级。', tg(True)) +
            '<div class="tabs2x" data-tabs><span class="on" data-t="p">提醒提供方</span><span data-t="a">高级设置 <i class="pill">' + ic('shield') + '</i></span></div>'
            '<div class="provs" data-pane="p">' + rows + '</div><div data-pane="a" hidden></div></div>')
    basic = ('<div class="info">' + ic('info') + '此处的设置可以在档案设置中被附加设置覆盖。<span class="btnw">查看…</span></div>' +
             exp('bell', '在课前准备时发出提醒', '在上课前一段时间发出醒目提醒，提示做好上课准备。',
                 '<div class="row1">' + cb(True, '启用语音') + '</div>' +
                 '<div class="row2">' + ic('bell') + '<div class="tx"><b>室内课程课前提醒时间</b><span>在室内课程的上课前指定时间进行上课提醒。</span></div>' + num('60') + '<em class="u">秒</em></div>' +
                 '<div class="row2">' + ic('bell') + '<div class="tx"><b>室外课程课前提醒时间</b><span>在室外课程的上课前指定时间进行上课提醒。</span></div>' + num('600') + '<em class="u">秒</em></div>' +
                 field('室内课程准备上课提醒文字', '准备上课，请回到座位并保持安静，做好上课准备。') + field('室内课程准备上课遮罩文字', '即将上课') +
                 field('户外课程准备上课提醒文字', '下节课程为户外课程，请合理规划时间，做好上课准备。') + field('户外课程准备上课遮罩文字', '即将上课')) +
             exp('school', '在上课时发出提醒', '在上课时发出醒目提醒，提示已经上课。', '<div class="row1">' + cb(True, '启用语音') + '</div>' + field('上课遮罩文字', '上课')) +
             exp('clock', '在下课时发出提醒', '在下课时发出醒目提醒，提示已经下课。', '<div class="row1">' + cb(True, '启用语音') + '</div>' + field('下课遮罩文字', '课间休息')))
    adv = (sc('shield', '对此提醒来源启用特殊高级设置', '启用后，此处的设置将覆盖全局设置和提醒请求中要求的设置。', tg(False)) +
           '<div class="dis">' + sc('text', '启用提醒语音', '在发出提醒时用语音播报提醒内容。', tg(False)) + sc('stack', '启用提醒强调特效', '启用后，发出提醒时会播放全屏强调特效。', tg(True)) +
           sc('monitor', '启用提醒音效', '启用后，发出提醒时会播放音效。', tg(False)) + sc('import', '置顶提醒', '在发出提醒时强制显示并置顶主界面。', tg(False)) + '</div>')
    right = ('<div class="rcol rr"><div class="rdetail" hidden><h3>上下课提醒</h3><div class="tabs2x" data-tabs><span class="on" data-t="b">基本设置</span><span data-t="a">高级设置 <i class="ring"></i></span></div>'
             '<div class="scr" data-pane="b">' + basic + '</div><div class="scr" data-pane="a" hidden>' + adv + '</div></div><div class="rempty">' + EMPTY + '</div></div>')
    return '<h2>提醒</h2><div class="two">' + left + right + '</div>'

# ---------------------------------------------------------------- 组件
def page_widgets():
    lib = [('text', '文本', '显示自定义文本。'), ('split', '分割线', '显示一个分割线，视觉上对组件进行分组。'), ('doc', '课程表', '显示当前的课程表信息。'), ('cal', '日期', '显示今天的日期和星期。'),
           ('clock', '时钟', '显示现在的时间，支持精确到秒。'), ('sun', '天气简报', '显示当前的天气概况和气象预警。'), ('timer', '倒计时', '显示距离某一天的倒计时。'), ('carousel', '轮播容器', '轮播多个组件。'),
           ('scroll', '滚动容器', '滚动显示组件内的内容。'), ('group', '分组容器', '将多个组件组合到一个组件中显示。'), ('stack', '堆叠容器', '将多个容器堆叠显示。')]
    g = ''.join('<div class="li" data-w="%s">%s<span class="tx"><b>%s</b><span>%s</span></span></div>' % (t, ic(i), t, d) for i, t, d in lib)
    return ('<div class="pg pgc"><div class="wtop"><div><h2>组件</h2><p class="sub2">以下组件将显示在主界面上，从组件库拖动组件以添加组件。</p></div>'
            '<div class="cfg"><label>配置方案</label><div class="cfgr">' + combo('Default', 150) + '<span class="ib">' + ic('sync') + '</span><span class="ib">' + ic('plus') + '</span><span class="ib">' + ic('folder') + '</span></div></div></div>'
            '<div class="rowbar"><span class="ins"></span><div class="chips2" id="wchips"><span class="wc on">' + ic('cal') + '日期</span><span class="wc">' + ic('doc') + '课程表</span></div>'
            '<div class="rtools"><span class="ib">' + ic('layout') + '</span><span class="ib acc">' + ic('bell') + '</span><span class="ib">' + ic('plus') + '</span><span class="ib red">' + ic('trash') + '</span></div></div>'
            '<div class="tabs2x" data-tabs><span class="on" data-t="l">组件库</span><span data-t="r">行设置</span></div>'
            '<div data-pane="l"><div class="grp">内置</div><div class="lib2">' + g + '</div></div><div data-pane="r" hidden><div class="grp">行设置</div>' +
            sc('layout', '行高', '', '<span class="num" style="min-width:120px">默认</span>') + sc('sliders', '行间隔', '', '<span class="num" style="min-width:120px">5</span>') + '</div>'
            '<div class="ibar"><span class="dot">i</span>新功能：现在可以使用「编辑模式」更加直观地编辑主界面上的组件！<span class="btnw">进入编辑模式</span><span class="x">' + ic('x') + '</span></div></div>')

# ---------------------------------------------------------------- 外观
def page_appearance():
    def sec(icon, t): return '<div class="sech">%s%s</div>' % (ic(icon), t)
    return ('<div class="pg pgc"><h2>外观</h2>' + sec('gear', '基本') +
            sc('search', '界面缩放', '主界面的缩放大小。', slider(18)) + sc('brush', '背景颜色', '主界面背景颜色，禁用时将根据应用主题自动选择颜色。', tg(False)) +
            sc('layout', '背景不透明度', '主界面背景的不透明度。', slider(50)) + sc('window', '圆角半径', '主界面圆角半径，调至最大数值时左右边缘为半圆。', slider(42)) +
            sc('layout', '行间隔', '主界面行间间隔。', slider(2) + num('5', 126)) + sc('split', '分体主界面', '启用后组件会分开。', tg(False)) +
            sec('brush', '主题') + sc('sun', '应用主题', '控制应用的明暗主题。', combo('黑暗', 92, 'sun', '黑暗|明亮|跟随系统')) + sc('brush', '主题色来源', '控制应用选取主题色的途径。', combo('系统', 92, 'monitor', '系统|壁纸|自定义')) +
            sec('text', '字体') + sc('text', '自定义字体', '自定义主界面显示课表的字体。', combo('HarmonyOS Sans SC（默认）', 240)) + sc('text', '自定义字重', '自定义主界面显示的字体的字重，需要对应字体支持。', combo('Medium', 98, '', 'Light|Regular|Medium|Bold')) +
            sc('text', '字体大小', '调整主界面上各类字体的大小。', '<span class="car2">' + ic('chev') + '</span>') + sc('text', '字体颜色', '调整字体颜色，将覆盖主题默认值。', tg(False)) + '</div>')

# ---------------------------------------------------------------- 窗口
def page_window():
    pos = ''.join('<span class="dock%s" data-dock="%d" style="%s"></span>' % (' on' if i == 1 else '', i, st) for i, st in enumerate(
        ['left:8%;top:10%', 'left:46%;top:10%', 'right:8%;top:10%', 'left:8%;bottom:20%', 'left:46%;bottom:20%', 'right:8%;bottom:20%']))
    return ('<div class="pg pgc"><h2>窗口</h2><div class="sech">' + ic('monitor') + '窗口停靠位置</div>'
            '<div class="dockrow"><div class="scr2">' + pos + '<span class="tb"></span></div><div class="dockf"><div class="two2"><div><label>向右偏移</label>' + num('0', 100) + '</div><div><label>向下偏移</label>' + num('0', 100) + '</div></div>'
            '<label>显示器</label><div class="sel wide">' + ic('monitor') + '( x )' + ic('chev') + '</div><div class="rf">' + ic('sync') + '刷新显示器列表</div>'
            '<p class="ds">应用会以左图的位置显示在指定的显示器上。如果指定的显示器不存在，那么应用会显示在主显示器上。</p></div></div>'
            + exp('stack', '窗口层级', '窗口在屏幕上的层级。置底则会显示在所有窗口的后方，置顶则将显示在所有窗口的前方。', sc('sync', '窗口层级设置频率', 'ClassFabric 在什么时候重新设置窗口置顶/置底状态。请注意，较高的设置频率可能会产生较高的性能占用并导致主界面内容闪烁。', combo('窗口层级变化时（默认）', 200), 'flat'), False, True, False).replace('<span class="car">', '<span class="up">置顶' + ic('chev') + '</span><span class="car">', 1)
            + exp('brush', '自定义背景效果', '自定义主界面的背景效果，仅在较新版本的 Windows 上可用，可能会产生额外性能开销。', '', False, False)
            + exp('monitor', '指针移入淡化', '启用后，在鼠标移入或触屏点击主界面区域时，将淡化主界面。',
                  sc('doc', '使用原始输入', '启用后，ClassFabric 将使用 RawInput 接收鼠标/触屏事件，而不是轮询获取光标位置。这允许应用辨别鼠标和触摸事件，并分别做出更适宜的响应。如果出现不兼容的问题，请尝试禁用此选项。', tg(False), 'flat') +
                  sc('eyeoff', '反转指针移入淡化', '启用后，将默认淡化主界面，使主界面仅在鼠标移入时显示。此开关不影响隐藏主界面。', tg(False), 'flat'), True, True) +
            sc('import', '使用原始屏幕尺寸', '若启用，主界面调整位置时将忽略系统工作区设置（通常包括任务栏和部分顶栏应用）。', tg(False)) +
            sc('monitor', '录制模式', '启用后，ClassFabric 将调整窗口属性以便被录屏软件录制。这会导致主界面窗口显示在任务栏中且主界面窗口只会在一个虚拟桌面上显示，如您没有录制 ClassFabric 窗口的需求，请勿开启此选项。', tg(False)) +
            sc('shield', '阻止截图', '开启后，其他应用无法截取 ClassFabric 主界面窗口内容，录制时也不会录制到主页面。', tg(False)) + '</div>')

# ---------------------------------------------------------------- 外壳
NAVX = [('gear', '通用', 'g', None), ('gear', '基本', 's', None), ('clock', '时钟', 's', None), ('save', '存储', 's', None), ('shield', '隐私', 's', None), ('sync', '翻新与迎新', 's', None), ('sliders', '高级', 's', None),
        ('layout', '主界面', 'g', None), ('widgets', '组件', 's', 'widgets'), ('brush', '外观', 's', 'appearance'), ('window', '窗口', 's', 'window'),
        ('bell', '提醒', 'i', 'remind'), ('cloud', '天气', 'i', None), ('bolt', '自动化', 'i', 'auto'), ('sync', '更新', 'i', None), ('hr',),
        ('plug', '插件', 'i', 'plugins'), ('brush', '主题', 'i', 'themes'), ('hr',), ('info', '关于 ClassFabric', 'i', None)]

def settings_app(island='周六 10/31　今天没有课程。', ver='2.1.1.4'):
    nav = '<nav class="nv"><div class="nvtop"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>' + ic('search') + '</div>'
    for it in NAVX:
        if it[0] == 'hr':
            nav += '<hr>'; continue
        ico, t, kind, pg = it
        cls = 'it' + (' sb' if kind == 's' else '') + ('' if pg else ' off')
        chev = '<svg class="chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>' if kind == 'g' else ''
        nav += '<div class="%s"%s><span class="ni">%s</span><span class="nt">%s</span>%s</div>' % (cls, (' data-go="%s"' % pg) if pg else '', ic(ico), t, chev)
    nav += '</nav>'
    pages = {'remind': page_remind(), 'widgets': page_widgets(), 'appearance': page_appearance(), 'window': page_window(),
             'auto': pg_auto(), 'plugins': pg_plugins(), 'themes': pg_themes()}
    body = ''
    for k, v in pages.items():
        if not v.startswith('<div class="pg'):
            v = '<div class="pg">' + v + '</div>'
        body += '<section class="pgx" data-p="%s">%s</section>' % (k, v)
    a, b = island.split('\u3000')
    return ('<div class="w sapp">' + titlebar('应用设置', ver, '<span>%s</span><span style="font-weight:400">%s</span>' % (a, b)) +
            '<div class="wb">' + nav + '<div class="pgs">' + body + '</div></div></div>')


# ---------------------------------------------------------------- 档案编辑（内容由 apps.js 渲染）
def editor_app(island='周六 10/31　今天没有课程。', ver='2.1.1.4', h=620):
    a, b = island.split('　')
    tabs = ''.join('<span%s data-v="%s">%s</span>' % (' class="on"' if k == 'grid' else '', k, t) for k, t in [('grid', '课表'), ('tl', '时间表'), ('sj', '科目'), ('sw', '调课')])
    acts = ''.join('<span>%s<em>%s</em></span>' % (ic(i), t) for i, t in [('doc', 'Default.json'), ('shield', '不信任'), ('save', '保存'), ('import', '导入/导出')])
    return ('<div class="app"><div class="w ed2" data-app="editor" style="--h:%dpx">' % h + titlebar('档案编辑', ver, '<span>%s</span><span style="font-weight:400">%s</span>' % (a, b)) +
            '<div class="e2tabs">' + tabs + '<div class="e2act">' + acts + '</div></div><div class="e2body"></div></div></div>')
