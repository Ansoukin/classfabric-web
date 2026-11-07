# -*- coding: utf-8 -*-
from ui import ic

E = {}


def init(g):
    E.update(g)


def bdg(txt, kind='', icn=None, cls=''):
    return '<span class="bdg %s %s">%s%s</span>' % (kind, cls, ic(icn) if icn else '<i class="dot"></i>', txt)


def hero(mob=False):
    REL, GH, GHSVG, ic_ = E['REL'], E['GH'], E['GHSVG'], ic
    gh = GHSVG.replace(' class="ghi"', '')
    isl = E['static_isl'](E['idle']('break', '56%', '78%', 3000)).replace('<div class="isl static"', '<div class="isl static on"')
    bg = r2 = ''
    if not mob:
        bg = '<div class="hz-bg" aria-hidden="true">' + E['vtask'](False).replace('%s', 'hzTray', 1) + '</div>'
        r2 = ('<div class="hz-r2" aria-hidden="true"><div class="isl static"><span data-now="time">00:00:00</span></div>'
              '<div class="isl static">' + ic_('sun') + '&nbsp;9℃</div><div class="isl static">' + ic_('timer') + '&nbsp;<span data-cd>元旦</span></div></div>')
    return ('<section class="hero hz" id="top"><div class="hz-pin">' + bg +
            '<div class="hz-isl" aria-hidden="true"><div class="isl-stack">' + isl + '</div></div>' + r2 +
            '<div class="hz-txt wrap">'
            '<p class="eyebrow rv d1"><img src="/assets/img/logo.png" width="26" height="26" alt="">ClassFabric<i></i>班级大屏课表</p>'
            '<h1 class="rv d1"><span class="seo-only">ClassFabric：</span>紧跟上游，<span class="g">再进一步</span></h1>'
            '<p class="sub rv d2">基于 ClassIsland 的个人修改版，原有课表、插件与主题无缝沿用</p>'
            '<div class="cta rv d2"><a class="btn blue" href="' + REL + '" data-dl data-releaselink rel="noopener">' + ic_('dl') + '立即下载</a><a class="btn glass" href="' + GH + '" rel="noopener">' + gh + 'GitHub 仓库</a></div>'
            '<p class="note rv d3">支持在 Windows 10/11 上运行　·　最新版本 <b data-ver class="sk"></b>　·　GPL-3.0 开源</p>'
            '</div></div></section>\n')


TH = [('classic', '经典', '单行岛条，天气、日期、课程与倒计时同排显示。', '#d9ab6e'),
      ('fluent', 'Fluent', '分体主界面，日期、时间与倒计时另起一行。', '#4aa3ff'),
      ('rect', 'Rectangles', '方块背景之上的醒目岛条。', '#e0489f')]


def themes(mob=False, app=''):
    bar = lambda k: '<img class="sk-i" src="/assets/img/theme-%s-bar.webp" alt="" width="656" height="119" loading="lazy" decoding="async">' % k
    seq1 = [TH[0][0], TH[1][0], TH[2][0]]
    seq2 = [TH[2][0], TH[0][0], TH[1][0]]
    r1 = ''.join(bar(k) for k in seq1) * 2
    r2 = ''.join(bar(k) for k in seq2) * 2
    tiles = ''
    for i, (k, n, d, ac) in enumerate(TH):
        tiles += ('<article class="thx-t rv d%d" style="--ac:%s"><div class="thx-pic"><img class="sk-i" src="/assets/img/theme-%s.webp" alt="%s 主题预览" width="322" height="144" loading="lazy" decoding="async"></div>'
                  '<div class="thx-tx"><div class="thx-n"><h4>%s</h4>%s</div><p>%s</p></div></article>') % (i, ac, k, n, n, bdg('内置', 'blue', None, 'sm'), d)
    tune = [('tv-s', '<i></i>', '界面缩放', '主界面的缩放大小'), ('tv-o', '<i></i>', '背景不透明度', '主界面背景的不透明度'),
            ('tv-r', '<i></i>', '圆角半径', '调至最大时，左右边缘为半圆'), ('tv-f', 'Aa', '字体', '更换主界面使用的字体')]
    tu = ''.join('<li class="tu rv d%d"><span class="tv %s">%s</span><div><b>%s</b><small>%s</small></div></li>' % (i, a, b, c, d) for i, (a, b, c, d) in enumerate(tune))
    return ('<div class="thx">'
            '<div class="thx-head rv"><div class="copy"><span class="tag o">#主题</span><h3>自由的主题系统</h3><p>内置经典、Fluent 与 Rectangles 三套主题，并支持调整界面缩放、背景透明度、圆角与字体，高度个性化你的界面。</p></div>'
            '</div>'
            '<div class="thx-reel rv" role="img" aria-label="三套主题的岛条效果"><div class="rw"><div class="trk">' + r1 + '</div></div><div class="rw rev"><div class="trk">' + r2 + '</div></div></div>'
            '<div class="thx-grid">' + tiles + '</div>'
            '<ul class="thx-tune">' + tu + '</ul>'
            + ('<div class="thx-app rv">' + app + '</div>' if app else '') + '</div>')


def skel_rows(n):
    return ''.join('<div class="skr"><i></i><span><b></b><u></u></span><em></em></div>' for _ in range(n))
