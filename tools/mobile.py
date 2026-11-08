# -*- coding: utf-8 -*-
import os
from PIL import Image

E = {}

JS_REDIR_M = ('<script>(function(){try{var u=navigator.userAgent,s=location.search,k="cf_view";if(/[?&]view=pc\\b/.test(s))localStorage.setItem(k,"pc");else if(/[?&]view=m\\b/.test(s))localStorage.setItem(k,"m");'
              'var v=localStorage.getItem(k),ph=/iPhone|iPod|Android.+Mobile|Windows Phone|IEMobile|BlackBerry|Opera Mini|Mobile.+Firefox/i.test(u);'
              'if(v==="pc"||(!ph&&v!=="m"&&Math.min(screen.width,innerWidth)>820)){location.replace("/"+location.hash)}}catch(e){}})()</script>\n')


def init(g):
    E.update(g)


def shot(src, alt, zw=720, native=3, cls='', hint=True):
    w, h = Image.open(os.path.join(E['OUT'], src.lstrip('/'))).size
    w, h = w // native, h // native
    z = '<b class="zi" aria-hidden="true">%s点按放大</b>' % E['ic']('search') if hint else ''
    return ('<figure class="shotf %s" data-zoom data-zw="%d" tabindex="0" role="button" aria-label="放大查看：%s"><img class="sk-i" src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">%s</figure>'
            % (cls, zw, alt, src, w, h, alt, z))


def main_panel():
    return shot('/assets/img/m/main.webp', '主界面：灵动岛显示今日课程与当前进度，下方为时钟、天气与倒计时组件', 720, 3, 'wide')


def rem_panel():
    names = ['准备上课', '上课', '课间休息']
    figs = ''.join('<div class="mrf%s" data-g="%d">%s</div>' % (' on' if i == 0 else '', i, shot('/assets/img/m/rem-g%d.webp' % i, '%s阶段的提醒样式' % n, 720, 3, 'wide', False)) for i, n in enumerate(names))
    return '<div class="mrem">' + figs + '</div>'


def editor_section():
    return shot('/assets/img/m/editor.webp', '档案编辑窗口：一周课表与科目面板', 760, 3, 'win')


def swap_section():
    return shot('/assets/img/m/swap.webp', '换课窗口：选择要调换的课程与替换科目', 760, 3, 'win')


def auto_shot():
    return shot('/assets/img/m/auto.webp', '自动化设置页面', 1100, 1, 'win')


def wid_shot():
    return shot('/assets/img/m/widgets.webp', '组件设置页面', 1000, 1, 'win')


def plg_shot():
    return shot('/assets/img/m/plugins.webp', '插件市场页面', 1000, 1, 'win')
