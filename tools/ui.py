# -*- coding: utf-8 -*-
"""HTML/CSS recreations of ClassFabric 2.1.1.3 UI (Fluent dark). Text and data are taken from real screenshots."""

P = {
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 3v2.4M12 18.6V21M3 12h2.4M18.6 12H21M5.6 5.6l1.7 1.7M16.7 16.7l1.7 1.7M5.6 18.4l1.7-1.7M16.7 7.3l1.7-1.7"/>',
 'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/>',
 'bell': '<path d="M6 17v-6a6 6 0 1112 0v6l1.5 1.5h-15z"/><path d="M10 21h4"/>',
 'cloud': '<path d="M7 18a4 4 0 010-8 5.5 5.5 0 0110.6 1.5A3.3 3.3 0 0117 18z"/>',
 'bolt': '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
 'sync': '<path d="M4 12a8 8 0 0113.5-5.8L20 8.5M20 4v4.5h-4.5M20 12a8 8 0 01-13.5 5.8L4 15.5M4 20v-4.5h4.5"/>',
 'plug': '<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 01-12 0zM12 17v4"/>',
 'brush': '<path d="M4 20c3 0 5-1 5-3.5L18 5l2 2-9 9.5C10 19 8 20 4 20z"/>',
 'info': '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5"/><circle cx="12" cy="8" r=".7" fill="currentColor"/>',
 'layout': '<rect x="3.5" y="5" width="17" height="14" rx="2"/><path d="M3.5 9h17"/>',
 'widgets': '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
 'chev': '<path d="M6 9l6 6 6-6"/>',
 'chevr': '<path d="M9 6l6 6-6 6"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7"/>',
 'plus': '<path d="M12 5v14M5 12h14"/>',
 'cal': '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M8 3v4M16 3v4"/>',
 'doc': '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/>',
 'swap': '<path d="M4 8h14M14 4l4 4-4 4M20 16H6M10 12l-4 4 4 4"/>',
 'eyeoff': '<path d="M3 12s3.5-6 9-6 9 6 9 6-3.5 6-9 6-9-6-9-6zM4 4l16 16"/>',
 'help': '<rect x="5" y="3.5" width="14" height="17" rx="2"/><path d="M10 9.5a2 2 0 114 0c0 1.4-2 1.6-2 3"/><circle cx="12" cy="16" r=".6" fill="currentColor"/>',
 'school': '<path d="M3 9l9-4 9 4-9 4zM7 11.5V16c0 1.5 2.2 3 5 3s5-1.5 5-3v-4.5"/>',
 'edit': '<path d="M4 20l1-4L16.5 4.5l3 3L8 19z"/>',
 'power': '<path d="M12 4v8M7 7a7 7 0 1010 0"/>',
 'exit': '<path d="M10 4H5v16h5M14 8l4 4-4 4M18 12H9"/>',
 'text': '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h8M8 13h8M8 17h5"/>',
 'split': '<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M12 5v14"/>',
 'timer': '<circle cx="12" cy="13.5" r="7"/><path d="M12 9.5v4l2.5 1.5M9.5 3h5"/>',
 'carousel': '<rect x="4" y="6" width="13" height="12" rx="2"/><path d="M20 9v6"/>',
 'scroll': '<path d="M5 6h14M5 11h14M5 16h9"/>',
 'group': '<path d="M4 8V5h3M17 5h3v3M20 16v3h-3M7 19H4v-3"/><rect x="8" y="8" width="8" height="8" rx="1.5"/>',
 'stack': '<rect x="3.5" y="9" width="12" height="10" rx="2"/><path d="M8 5.5h10.5a2 2 0 012 2V15"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/>',
 'atom': '<circle cx="12" cy="12" r="1.6" fill="currentColor"/><ellipse cx="12" cy="12" rx="10" ry="4.2"/><ellipse cx="12" cy="12" rx="10" ry="4.2" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.2" transform="rotate(120 12 12)"/>',
 'folder': '<path d="M3.5 7a2 2 0 012-2H10l2 2h6.5a2 2 0 012 2v8a2 2 0 01-2 2h-13a2 2 0 01-2-2z"/>',
 'undo': '<path d="M9 7L4 12l5 5M4 12h10a6 6 0 010 8"/>',
 'back': '<path d="M3 11a8 8 0 1114 5.3M3 6v5h5"/>',
 'trash': '<path d="M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13"/>',
 'shield': '<path d="M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6z"/>',
 'sliders': '<path d="M4 8h9M17 8h3M4 16h3M11 16h9"/><circle cx="15" cy="8" r="2"/><circle cx="9" cy="16" r="2"/>',
 'save': '<path d="M5 4h11l3 3v13H5z"/><path d="M8 4v5h7V4M8 20v-6h8v6"/>',
 'import': '<path d="M12 4v10M8 10l4 4 4-4M5 19h14"/>',
 'list': '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
 'monitor': '<rect x="3.5" y="4.5" width="17" height="11" rx="2"/><path d="M9 20h6M12 15.5V20"/>',
 'play': '<circle cx="12" cy="12" r="8"/><path d="M10.5 9l4 3-4 3z"/>',
 'window': '<rect x="3.5" y="5" width="17" height="14" rx="2"/><path d="M3.5 9.5h17"/>',
 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
 'search': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
 'tri': '<path d="M3 20h18L12 4z"/><path d="M12 10v5"/>',
 'dl': '<path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 20h14"/>',
}

def ic(n, cls=''):
    return '<svg viewBox="0 0 24 24"%s aria-hidden="true">%s</svg>' % ((' class="%s"' % cls) if cls else '', P[n])

def tg(on=True, label=None):
    return '<span class="tg%s"><i></i><span>%s</span></span>' % (' on' if on else '', label if label is not None else ('开' if on else '关'))

def cb(on, text):
    return '<span class="cb%s"><i>%s</i>%s</span>' % (' on' if on else '', ic('check') if on else '', text)

def titlebar(title, ver=None, isl=None, icon=True):
    return ('<div class="wt">' + ('<img class="ico" src="/assets/img/icon-32.png" alt="">' if icon else '') + title +
            ('<span class="w-title-island">%s</span>' % isl if isl else '') +
            ('<span class="ver">%s</span>' % ver if ver else '') +
            '<span class="ctl" style="margin-left:%s"><i>%s</i><i>%s</i><i class="x">%s</i></span></div>' % (
                '0' if ver else 'auto',
                '<svg viewBox="0 0 10 10"><path d="M0 5h10"/></svg>', '<svg viewBox="0 0 10 10"><rect x=".5" y=".5" width="9" height="9"/></svg>', '<svg viewBox="0 0 10 10"><path d="M0 0l10 10M10 0L0 10"/></svg>'))

TITLE_ISL = '<span>周四 10/29</span><span style="font-weight:400">今天没有课程。</span>'

# ---------------------------------------------------------------- settings window
NAV = [
 ('gear', '通用', 'g'), ('sub', '基本'), ('sub', '时钟'), ('sub', '存储'), ('sub', '隐私'), ('sub', '翻新与迎新'), ('sub', '高级'),
 ('layout', '主界面', 'g'), ('sub', '组件'), ('sub', '外观'), ('sub', '窗口'),
 ('bell', '提醒'), ('cloud', '天气'), ('bolt', '自动化'), ('sync', '更新'), ('hr',),
 ('plug', '插件'), ('brush', '主题'), ('hr',), ('info', '关于 ClassFabric'),
]

SUBIC = {'基本': 'gear', '时钟': 'clock', '存储': 'save', '隐私': 'shield', '翻新与迎新': 'sync', '高级': 'sliders', '组件': 'widgets', '外观': 'brush', '窗口': 'window'}

def nav(on):
    o = ['<div class="nv"><div class="nvtop">' + '<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>' + ic('search') + '</div>']
    for it in NAV:
        if it[0] == 'hr':
            o.append('<hr>'); continue
        if it[0] == 'sub':
            o.append('<div class="it sb%s">%s%s</div>' % (' on' if it[1] == on else '', ic(SUBIC.get(it[1], 'gear')), it[1]))
        else:
            chev = '<svg class="chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>' if len(it) > 2 else ''
            o.append('<div class="it%s">%s%s%s</div>' % (' on' if it[1] == on else '', ic(it[0]), it[1], chev))
    o.append('</div>')
    return ''.join(o)

def pg_remind():
    left = (
     '<div style="width:44%;flex:none">'
     '<div class="sc"><span style="width:20px">' + ic('bell') + '</span><div class="tx"><b>启用提醒</b><span>启用提醒后，将会在对重要事件发出醒目提醒。拖动提醒提供方以调整对应类型提醒的优先级。</span></div>' + tg(True) + '</div>'
     '<div class="tabs"><span class="on">提醒提供方</span><span>高级设置</span></div>'
     '<div class="sc" style="min-height:44px"><span style="width:20px">' + ic('school') + '</span><div class="tx"><b>上下课提醒</b><span>在准备上课、上课和下课时发出醒目提醒，并预告下一节课。</span></div></div>'
     '<div class="sc" style="min-height:34px;background:#2d2d2d;padding:6px 14px;font-size:12.5px;justify-content:space-between">提醒渠道' + ic('chev') + '</div>'
     '<div class="sc flat" style="min-height:40px;border-left:3px solid var(--blue);border-radius:0;padding-left:14px"><div class="tx"><b>准备上课提醒</b><span>在上课前指定时间发出提醒。</span></div></div>'
     '<div class="sc flat" style="min-height:40px;padding-left:17px"><div class="tx"><b>上课提醒</b><span>在上课时发出提醒。</span></div></div>'
     '<div class="sc flat" style="min-height:40px;padding-left:17px"><div class="tx"><b>下课提醒</b><span>在下课时发出提醒。</span></div></div>'
     '<div class="sc flat" style="min-height:40px"><span style="width:20px">' + ic('doc') + '</span><div class="tx"><b>放学提醒</b><span>在当天的课程结束后发出提醒。</span></div></div>'
     '<div class="sc flat" style="min-height:40px"><span style="width:20px">' + ic('cloud') + '</span><div class="tx"><b>天气预警</b><span>当有降雨或者极端天气时发出提醒。</span></div></div>'
     '<div class="sc flat" style="min-height:40px"><span style="width:20px">' + ic('bolt') + '</span><div class="tx"><b>行动提醒</b><span>显示由行动发出的提醒。</span></div></div>'
     '</div>')
    right = (
     '<div style="flex:1;min-width:0;padding-left:14px;border-left:1px solid #383838">'
     '<h2 style="font-size:20px;margin-bottom:4px">上下课提醒</h2><div class="tabs"><span class="on">基本设置</span><span>高级设置</span></div>'
     '<div class="sc"><span style="width:20px">' + ic('bell') + '</span><div class="tx"><b>在课前准备时发出提醒</b><span>在上课前一段时间发出醒目提醒，提示做好上课准备。</span></div>' + tg(True) + '</div>'
     '<div style="padding:8px 14px">' + cb(True, '启用语音') + '</div>'
     '<div class="sc flat"><div class="tx"><b>室内课程课前提醒时间</b><span>在室内课程的上课前指定时间进行上课提醒。</span></div><div class="num">60<em>' + ic('chev') + '</em></div><span style="font-size:12px">秒</span></div>'
     '<div class="sc flat"><div class="tx"><b>室外课程课前提醒时间</b><span>在室外课程的上课前指定时间进行上课提醒。</span></div><div class="num">600<em>' + ic('chev') + '</em></div><span style="font-size:12px">秒</span></div>'
     '<div class="fld" style="padding:0 14px"><label>室内课程准备上课提醒文字</label><div class="inp">准备上课，请回到座位并保持安静，做好上课准备。</div></div>'
     '<div class="fld" style="padding:0 14px"><label>室内课程准备上课遮罩文字</label><div class="inp">即将上课</div></div>'
     '<div class="fld" style="padding:0 14px"><label>户外课程准备上课提醒文字</label><div class="inp">下节课程为户外课程，请合理规划时间，做好上课准备。</div></div>'
     '</div>')
    return '<div class="pg" style="display:flex;padding-top:12px">' + left + right + '</div>'

def pg_auto():
    lft = (
     '<div class="auto"><div class="lft">'
     '<div class="sc"><span style="width:20px">' + ic('bolt') + '</span><div class="tx"><b>启用自动化</b><span>自动化是一种可使 ClassFabric 自动作出行动的功能。</span></div>' + tg(True) + '</div>'
     '<div style="display:flex;align-items:center;gap:8px;margin:8px 0;font-size:12.5px"><span style="display:flex;gap:6px;color:var(--blue)">' + ic('plus') + '添加自动化</span><span class="sel" style="margin-left:auto;min-width:96px">Default' + ic('chev') + '</span></div>'
     '<div class="arow on"><span style="flex:1">新自动化</span>' + tg(True) + '</div>'
     '</div>'
     '<div class="rgt" style="position:relative">'
     '<div style="display:flex;gap:10px;align-items:center;margin-bottom:12px;font-size:14px"><div class="inp" style="width:148px;flex:none;height:32px;font-weight:600">新自动化</div>' + cb(True, '启用恢复') + '<span class="btnw" style="margin-left:2px;background:#303a46;border-color:transparent;font-weight:600">' + ic('play') + '触发</span><span style="opacity:.7">' + ic('play') + '</span><span style="display:flex;gap:6px;align-items:center;font-weight:600;margin-left:8px">' + ic('undo') + '恢复</span><span style="width:1px;height:20px;background:#555;margin:0 4px"></span>' + ic('doc') + '<span style="color:#ff6f7d;margin-left:6px">' + ic('trash') + '</span></div>'
     '<div class="hdr">' + ic('bolt') + '当事件触发时' + ic('chev', 'chev') + '</div>'
     '<div class="bd" style="min-height:76px"><span class="sel" id="selTrig" style="width:112px;margin-right:6px">&nbsp;' + ic('chev') + '</span><div style="margin-top:12px;color:var(--blue);display:flex;gap:6px;align-items:center;font-size:12.5px">' + ic('plus') + '添加触发器</div></div>'
     '<div class="hdr">' + ic('shield') + '并且满足规则集时' + tg(False) + ic('chev', 'chev') + '</div>'
     '<div class="bd">工作流运行时不会考虑规则集。</div>'
     '<div class="hdr">' + ic('bolt') + '触发行动' + ic('chev', 'chev') + '</div>'
     '<div class="bd" style="min-height:70px"><div id="btnAct" style="color:var(--blue);display:flex;gap:6px;align-items:center;font-size:12.5px;cursor:pointer">' + ic('plus') + '添加行动</div></div>'
     + flyout_trig() + flyout_act() +
     '</div></div>')
    return '<div class="pg"><h2>自动化</h2>' + lft + '</div>'

def flyout_trig():
    items = ['规则集更新时', '收到信号时', '调用 Uri 时', '从托盘菜单运行时', 'cron', '应用启动时', '应用退出时', '上课时', '课间休息时', '放学时', '当前时间状态变化时', '特定时间点前']
    ico = ['shield', 'bell', 'import', 'list', 'sync', 'window', 'exit', 'school', 'clock', 'power', 'clock', 'clock']
    return '<div class="fly open" id="flyTrig" style="left:5px;top:122px;width:182px">' + ''.join('<div class="mi">%s%s</div>' % (ic(i), t) for i, t in zip(ico, items)) + '</div>'

def flyout_act():
    h = '<div class="fly" id="flyAct" style="left:-6px;top:150px;width:130px">'
    h += '<div class="mi">' + ic('bell') + '广播信号</div><div class="mi">' + ic('clock') + '等待时长</div>'
    h += '<div class="mi">' + ic('gear') + '应用设置' + ic('chevr', 'chev') + '</div><div class="mi hl">' + ic('import') + '运行' + ic('chevr', 'chev') + '</div>'
    h += '<div class="mi">' + ic('bell') + '提醒' + ic('chevr', 'chev') + '</div><div class="mi">' + ic('info') + 'ClassFabric' + ic('chevr', 'chev') + '</div></div>'
    h += '<div class="fly" id="flyAct2" style="left:128px;top:180px;width:112px"><div class="mi">' + ic('window') + '应用程序</div><div class="mi">' + ic('list') + 'cmd 命令</div><div class="mi">' + ic('doc') + '文件</div><div class="mi">' + ic('folder') + '文件夹</div><div class="mi">' + ic('import') + 'Url 链接</div></div>'
    return h

def pg_widgets():
    lib = [('text', '文本', '显示自定义文本。'), ('split', '分割线', '显示一个分割线，视觉上对组件进行分组。'), ('doc', '课程表', '显示当前的课程表信息。'), ('cal', '日期', '显示今天的日期和星期。'),
           ('clock', '时钟', '显示现在的时间，支持精确到秒。'), ('sun', '天气简报', '显示当前的天气概况和气象预警。'), ('timer', '倒计时', '显示距离某一天的倒计时。'), ('carousel', '轮播容器', '轮播多个组件。'),
           ('scroll', '滚动容器', '滚动显示组件内的内容。'), ('group', '分组容器', '将多个组件组合到一个组件中显示。'), ('stack', '堆叠容器', '将多个容器堆叠显示。')]
    g = ''.join('<div>%s<span class="x"><b>%s</b><span>%s</span></span></div>' % (ic(i), t, d) for i, t, d in lib)
    return ('<div class="pg"><div style="display:flex;align-items:flex-start"><div style="flex:1"><h2>组件</h2><div style="font-size:12.5px;color:#ddd;margin:-4px 0 10px">以下组件将显示在主界面上，从组件库拖动组件以添加组件。</div></div>'
            '<div style="font-size:12px;display:grid;gap:4px;justify-items:end"><span>配置方案</span><span class="sel" style="min-width:120px">Default' + ic('chev') + '</span></div></div>'
            '<div class="placed"><span class="pc">' + ic('cal') + '日期</span><span class="pc">' + ic('doc') + '课程表</span></div>'
            '<div class="tabs"><span class="on">组件库</span><span>高级设置</span></div><div style="font-size:12px;font-weight:600;margin-top:6px">内置</div>'
            '<div class="lib">' + g + '</div>'
            '<div class="ibar"><span class="dot">i</span>新功能：现在可以使用「编辑模式」更加直观地编辑主界面上的组件！<span class="btnw" style="margin-left:auto">进入编辑模式</span></div></div>')

def pg_plugins():
    def icon(kind):
        if kind == 'win':
            return '<span class="pi"><i style="left:3px;top:6px;width:28px;height:18px;background:#3d8fd8"></i><i style="left:10px;top:13px;width:28px;height:20px;background:#d9d9d9"></i><i style="left:15px;top:19px;width:6px;height:6px;background:#3d8fd8"></i></span>'
        if kind == 'ua':
            return '<span class="pi" style="background:#fff;border-radius:11px"><svg viewBox="0 0 24 24" style="stroke:#222;width:30px;height:30px;margin:9px"><rect x="3" y="5" width="18" height="12" rx="3"/><circle cx="15" cy="15" r="4.5" fill="#222"/><path d="M15 17.3v-4.4M13.2 14.6l1.8-1.8 1.8 1.8" stroke="#fff"/></svg></span>'
        if kind == 'gsv':
            return '<span class="pi" style="border-radius:50%;background:radial-gradient(circle at 50% 40%,#f3d9a8 0 38%,#d9b45a 40% 62%,#3a3a5a 64%)"></span>'
        return '<span class="pi"><svg viewBox="0 0 24 24" style="stroke:#2fd1b8;stroke-width:2.2;width:38px;height:38px;margin:5px"><path d="M3 18a9 9 0 0118 0"/><path d="M8 18a4 4 0 018 0"/></svg></span>'
    rows = [('win', '随机抽选', '1.3K', '2', '桌面抽人悬浮窗。点击抽取名单中的一人，屏幕中央弹出大字；支持拍照抽人，从合影中检测人脸随机抽取。名单为纯文本，一行一个名字。'),
            ('win', '像素流动', '1.3K', '0', '仿 Claude Code UltraCode 的像素流动动画，替换提醒的遮罩层与正文层背景。配色跟随应用主题色，倒计时以彩带长度表示剩余时间。'),
            ('ua', 'UIAccess 提权', '9.7K', '17', '本插件可以为 ClassIsland 提升 UIAccess 令牌，使 ClassIsland 可以置顶到全屏 UWP 应用和系统界面上。'),
            ('gsv', 'GSVIsland', '3.4K', '5', '使 ClassIsland 的语音服务适配 GPT-SoVITS 推理特化包（GSVI）的 API'),
            ('om', 'OmniTTS', '403', '3', '多引擎文字转语音服务。')]
    dl = '<span class="dlb"><svg viewBox="0 0 24 24"><path d="M12 5v10M8 12l4 4 4-4"/></svg></span>'
    r = ''.join('<div class="row%s">%s<div class="rt"><b>%s<small><svg viewBox="0 0 24 24"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>%s <svg viewBox="0 0 24 24" style="fill:currentColor;stroke:none"><path d="M12 3l2.7 5.8 6.3.8-4.6 4.4 1.2 6.2L12 17.1 6.4 20.2l1.2-6.2L3 9.6l6.3-.8z"/></svg>%s</small></b><span>%s</span></div>%s</div>' % (' on' if n == 'UIAccess 提权' else '', icon(k), n, d, st, t, dl) for k, n, d, st, t in rows)
    return ('<div class="pg pl-pg"><h2>插件</h2><div class="plw"><div class="pll"><div class="inp srch">' + ic('search') + '搜索插件...</div>'
            '<div class="ptabs"><span class="on">市场</span><span>已安装</span><span class="rf">' + ic('sync') + '刷新</span><span>···</span></div><div class="lst">' + r + '</div></div>'
            '<div class="plr"><div class="ph">' + icon('ua').replace('class="pi"', 'class="pi big"') + '<div><h3>UIAccess 提权</h3><div class="pm">2.0.0.0 <u>|</u> <a>项目主页</a> <u>|</u> HelloWRC, Doubx690i <u>|</u> ' + ic('info') + ' 未加载</div><span class="inst">' + ic('dl') + ' 安装</span></div></div>'
            '<div class="ptabs sm"><span class="on">概览</span><span>依赖项</span></div>'
            '<div class="md"><div class="mshot"></div><h1>UIAccess 提权</h1><blockquote>提权方法及核心由 Doubx690i(Dubi906w/kriastans) 提供。</blockquote>'
            '<p>本插件可以为 ClassIsland 提升 UIAccess 令牌，使 ClassIsland 可以置顶到全屏 UWP 应用和系统界面上。</p><p><b>注意事项:</b> - 您需要以管理员身份运行 ClassIsland 才能正常使用本插件的功能。- 本插件进行的操作涉及敏感操作，可能会触发安全软件拦截。建议将 ClassIsland 工作目录添加到安全软件的排除名单中，以避免误报。</p><h1 style="font-size:22px">截图</h1></div></div></div></div>')

def pg_themes():
    def tc(img, name, on):
        return '<div class="tc"><img src="/assets/img/%s.webp" alt="" loading="lazy" width="322" height="144"><div class="nm">%s<small>ClassFabric</small></div>%s</div>' % (img, name, tg(on, ''))
    return ('<div class="pg"><h2>主题</h2><div class="ibar" style="margin:0 0 10px"><span class="dot">i</span>在启用了支持的主题（如 Fluent）后，可以在直接【外观】设置中开启【分体主界面】选项使主界面分开。</div>'
            '<div class="tabs"><span>市场</span><span class="on">已安装</span></div>'
            '<div class="thm">' + tc('theme-classic', '经典', False) + tc('theme-fluent', 'Fluent', True) + tc('theme-rect', 'Rectangles', False) + '</div>'
            '<div style="margin-top:18px;display:grid;gap:3px">'
            '<div class="sc"><div class="tx"><b>界面缩放</b><span>主界面的缩放大小。</span></div><div style="width:150px;height:4px;border-radius:2px;background:linear-gradient(90deg,var(--blue) 24%,#777 24%)"></div></div>'
            '<div class="sc"><div class="tx"><b>圆角半径</b><span>主界面圆角半径，调至最大数值时左右边缘为半圆。</span></div><div style="width:150px;height:4px;border-radius:2px;background:linear-gradient(90deg,var(--blue) 52%,#777 52%)"></div></div>'
            '<div class="sc"><div class="tx"><b>自定义字体</b><span>自定义主界面显示课表的字体。</span></div><span class="sel" style="min-width:160px">HarmonyOS Sans SC（默认）' + ic('chev') + '</span></div></div></div>')

PAGES = {'remind': ('提醒', pg_remind), 'auto': ('自动化', pg_auto), 'widgets': ('组件', pg_widgets), 'plugins': ('插件', pg_plugins), 'themes': ('主题', pg_themes)}

def settings_window(page, dw=860, dh=520):
    on, fn = PAGES[page]
    body = fn()
    h = ('<div class="w" style="--dw:%dpx;--dh:%dpx">' % (dw, dh)) + titlebar('应用设置', '2.1.1.3', TITLE_ISL) + '<div class="wb">' + nav(on) + body + '</div></div>'
    return h

# ---------------------------------------------------------------- profile editor
ROWS = [('07:40-08:20', '语文'), ('08:30-09:10', '数学'), ('09:20-10:00', '英语'), ('10:30-11:10', '物理'), ('11:20-12:00', '化学'), ('13:50-14:30', '生物'),
        ('14:40-15:20', '政治'), ('15:30-16:10', '历史'), ('16:20-17:00', '地理'), ('17:30-18:50', '自习'), ('19:05-20:25', '自习')]
DAYS = [('日', '10/25'), ('一', '10/26'), ('二', '10/27'), ('三', '10/28'), ('四', '10/29'), ('五', '10/30'), ('六', '10/31')]
SUBJ = ['语', '数', '英', '历', '政', '物', '化', '生', '地', '信', '体', '自', '技', '音', '美', '选', '社', '心', '早', '班', '测']

def grid_view(filled=True):
    th = '<th style="width:92px;height:50px"><span style="color:#ddd;font-size:11px">时间</span></th>'
    for d, dt in DAYS:
        if d == '四':
            th += '<th style="background:#363636">周四<small>%s</small><span style="display:block;margin-top:4px;text-align:right;color:#cfcfcf">%s</span></th>' % (dt, ic('gear'))
        else:
            th += '<th>周%s<small>%s</small><span class="nb">+ 新课表</span></th>' % (d, dt)
    tr = ''
    for i, (t, s) in enumerate(ROWS):
        tds = ''.join('<td></td>' if d != '四' else '<td class="c%s" data-i="%d" data-s="%s">%s</td>' % (' sel' if (filled and i == 1) else '', i, s, s if filled else '') for d, _ in DAYS)
        tr += '<tr><td class="t">%s</td>%s</tr>' % (t, tds)
    chips = ''.join('<span%s data-s="%s">%s</span>' % (' class="on"' if (filled and s == '数') else '', s, s) for s in SUBJ)
    return ('<div class="view on" data-v="grid"><div class="grid"><div class="gh"><span class="dp">2026/10/29' + ic('cal') + '</span><span>←</span><span>→</span><span>第9周</span></div>'
            '<table class="tt"><thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table></div>'
            '<div class="side"><div class="tb"><span class="on">编辑科目</span><span>编辑课程</span></div><div class="chips">' + chips + '</div>'
            '<div style="margin-top:96px">' + cb(True, '选完科目自动移动到下一个课程') + '</div></div></div>')

def timeline_view():
    px = 1.5
    def t(m): return int((m - (7 * 60 + 30)) * px)
    def hm(m): return '%02d:%02d' % (m // 60, m % 60)
    lines = ''.join('<div class="hr" style="top:%dpx"><span>%s</span></div>' % (t(m), hm(m)) for m in range(7 * 60 + 30, 12 * 60 + 1, 30))
    seq = [(7 * 60 + 40, 8 * 60 + 20, 'k'), (8 * 60 + 20, 8 * 60 + 30, 'b'), (8 * 60 + 30, 9 * 60 + 10, 'k'), (9 * 60 + 10, 9 * 60 + 20, 'b'), (9 * 60 + 20, 10 * 60, 'k'), (10 * 60, 10 * 60 + 30, 'b'), (10 * 60 + 30, 11 * 60 + 10, 'k'), (11 * 60 + 10, 11 * 60 + 20, 'b'), (11 * 60 + 20, 12 * 60, 'k')]
    blocks = ''
    for a, b, k in seq:
        if k == 'k':
            blocks += '<div class="blk2 k" style="top:%dpx;height:%dpx"><span>%s - %s</span><span style="opacity:.8">%02d:%02d:00</span></div>' % (t(a), (b - a) * px, hm(a) + ':00', hm(b) + ':00', (b - a) // 60, (b - a) % 60)
        else:
            blocks += '<div class="blk2 b" style="top:%dpx;height:%dpx">%s %s - %s</div>' % (t(a), (b - a) * px, ic('clock'), hm(a) + ':00', hm(b) + ':00')
    return ('<div class="view" data-v="tl"><div class="tl"><div class="lst"><div>新时间表</div></div><div class="cv">' + lines + blocks + '</div>'
            '<div class="side"><div style="font-size:19px;font-weight:600;margin-bottom:10px">编辑时间点</div><div style="color:#ddd">开始时间</div>'
            '<div class="num" style="margin:4px 0 10px;min-width:0;justify-content:space-around;padding:0">7<span>40</span><span>00</span></div><div style="color:#ddd">结束时间</div>'
            '<div class="num" style="margin:4px 0 10px;min-width:0;justify-content:space-around;padding:0">8<span>20</span><span>00</span></div><div style="color:#ddd;margin-bottom:6px">类型</div>'
            '<div style="display:flex;gap:6px"><span class="btnw acc" style="height:26px">上课</span><span class="btnw" style="height:26px;background:transparent;border-color:transparent">课间休息</span></div>'
            '<div style="margin-top:12px">' + cb(False, '默认隐藏') + '</div><div style="margin:12px 0 4px;color:#ddd">默认课程</div><div class="sel" style="width:100%">&nbsp;' + ic('chev') + '</div>'
            '<div style="margin-top:14px;color:#ddd">更多选项</div><div class="sc" style="min-height:34px;margin-top:6px;padding:4px 10px;font-size:12px">上课提醒设置<span style="margin-left:auto">' + tg(False, '') + '</span></div>'
            '<div class="sc" style="min-height:34px;padding:4px 10px;font-size:12px">课程显示设置<span style="margin-left:auto">' + tg(False, '') + '</span></div></div></div></div>')

def subjects_view():
    data = [('语文', '语', '#e5576b', 0), ('数学', '数', '#5a78d8', 0), ('英语', '英', '#7e62d3', 0), ('历史', '历', '#c58b3d', 0), ('政治', '政', '#df4f6d', 0), ('物理', '物', '#3a9ae2', 0),
            ('化学', '化', '#2fb2a1', 0), ('生物', '生', '#4faf53', 0), ('地理', '地', '#8bb347', 0), ('信息技术', '信', '#2f9cc9', 1), ('体育', '体', '#f0872e', 1), ('自习', '自', '#6c7d9d', 0), ('通用技术', '技', '#a8774f', 0)]
    r = '<div class="r h"><span></span><span>主题</span><span>科目名</span><span>简称</span><span>户外课程?</span></div>'
    for i, (n, s, c, o) in enumerate(data):
        r += '<div class="r%s"><span style="color:#ddd">%s</span><span class="sw" style="background:%s"></span><span>%s</span><span>%s</span><span><i class="cbx%s">%s</i></span></div>' % (' on' if i == 0 else '', ic('doc'), c, n, s, ' on' if o else '', ic('check') if o else '')
    return '<div class="view" data-v="sj"><div class="sj">' + r + '</div><div class="side"><div style="font-size:19px;font-weight:600;margin-bottom:10px">编辑科目信息</div><div style="color:#ddd">科目名</div><div class="inp" style="margin:4px 0 10px">语文</div><div style="color:#ddd">简称</div><div class="inp" style="margin:4px 0 10px">语</div><div style="color:#ddd">科任老师</div><div class="inp" style="margin:4px 0 10px"></div>' + cb(False, '该科目是户外课程') + '</div></div>'

def editor_window(dw=860, dh=520, filled=True, wid=''):
    tools = ''.join('<span>%s%s</span>' % (ic(i), t) for i, t in [('doc', '周四'), ('info', '详细信息'), ('list', '详细看板'), ('stack', '创建临时层'), ('trash', '删除')])
    tabs = '<div class="tabs2"><span class="on" data-tab="grid">课表</span><span data-tab="tl">时间表</span><span data-tab="sj">科目</span><span>调课</span><div class="r"><span>' + ic('doc') + 'Default.json</span><span>' + ic('shield') + '不信任</span><span>' + ic('save') + '保存</span><span>' + ic('import') + '导入/导出</span></div></div>'
    return ('<div class="w editor"%s style="--dw:%dpx;--dh:%dpx">' % ((' id="%s"' % wid) if wid else '', dw, dh)) + titlebar('档案编辑', None, TITLE_ISL) + \
           '<div class="ed" style="height:calc(var(--dh) - 32px)">' + tabs + '<div class="tool"><span>' + ic('sync') + '刷新</span><b></b>' + tools + '</div>' + grid_view(filled) + timeline_view() + subjects_view() + '</div></div>'

# ---------------------------------------------------------------- swap dialog
def swap_dialog():
    subs = ''.join('<span class="pick" data-s="%s" data-n="%s">%s</span>' % (s, n, s) for s, n in zip('语数英物化生政历地自自', ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '自习', '自习']))
    return ('<div class="w swp" id="swap" style="--dw:640px">' + titlebar('换课', None, None, False) +
            '<div class="wb"><div style="width:100%"><div class="top"><h4>换课 <span>' + ic('doc') + '周四</span><em id="swHint">→ 选择要调换的课程。</em></h4></div>'
            '<div class="mid" id="swMid">' + subs + '</div><div class="done" id="swDone">' + ic('check') + '已交换：语文 与 数学 的位置对调</div>'
            '<div class="bot"><span class="btnw" id="swCancel">' + ic('x') + '取消</span><span class="btnw ghost" id="swBack" style="display:none">← 上一步</span><span class="btnw ghost">高级换课…</span><span class="sp"></span>'
            '<span id="swPerm" style="display:none">' + cb(False, '永久换课') + '</span><span class="btnw acc" id="swOk" style="display:none">' + ic('check') + '确认换课</span></div></div></div></div>')

# ---------------------------------------------------------------- tray menu / recovery
def tray_menu():
    items = [('info', 'ClassFabric', ''), ('school', '教学…', ''), ('help', '帮助文档…', ''), ('hr',), ('eyeoff', '隐藏主界面', ''), ('hr',), ('doc', '编辑档案…', 'edit'), ('doc', '加载临时课表…', ''), ('swap', '换课…', ''), ('hr',), ('edit', '编辑主界面…', ''), ('gear', '应用设置…', ''), ('hr',), ('sync', '重启', ''), ('exit', '退出', '')]
    h = '<div class="tmenu">'
    for it in items:
        if it[0] == 'hr': h += '<hr>'
        else: h += '<div class="mi" data-k="%s">%s%s</div>' % (it[2], ic(it[0]), it[1])
    return h + '</div>'

def recovery():
    def o(i, t, s='', dis=False, ext=False):
        return '<div class="o%s">%s<div><b>%s</b>%s</div>%s</div>' % (' dis' if dis else '', ic(i), t, ('<small>%s</small>' % s) if s else '', ic('chevr', 'go'))
    return ('<div class="rcv" style="--dw:420px"><div class="t">恢复<span class="ctl"><i>–</i><i>▢</i><i>✕</i></span></div><h5>选择一个选项</h5><p class="s">选择一个操作以继续。</p>'
            '<div class="g1">' + o('chevr', '继续使用 ClassFabric') + o('chevr', '以安全模式继续使用 ClassFabric', '禁用所有插件和自动化功能。') + o('chevr', '以诊断模式继续使用 ClassFabric', '在日志中记录详细的信息，并启用控制台输出。') + o('folder', '打开日志目录') + '</div>'
            '<div class="g1">' + o('back', '恢复备份', '从先前的备份恢复处于正确状态的配置文件。') + o('undo', '回滚', '回滚到之前的 ClassFabric 版本', True) + '</div>'
            '<div class="g1">' + o('trash', '清除临时文件', '删除所有缓存和临时文件。') + o('sync', '重置应用设置', '重置应用的设置信息，不影响档案、组件、自动化、插件等的配置。') + o('save', '重置全部配置', '重置应用的所有配置，包括应用设置、组件配置、自动化配置、插件设置等，不影响档案配置。') + o('back', '重置全部信息', '重置应用的所有信息，恢复到安装前的状态。') + '</div></div>')
