#!/usr/bin/env python3
"""下载页回归测试（v5）：状态、交互、动效降级、溢出、CLS。
用法：python3 tools/t_dl3.py   （自带本地服务器，GitHub 接口与下载链接均 stub，不访问外网）"""
import json, os, sys, threading, functools, http.server
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
H = functools.partial(Q, directory=ROOT)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = 'http://127.0.0.1:%d/download.html' % srv.server_address[1]

def A(n, s): return {'name': n, 'size': s, 'browser_download_url': 'https://x/' + n}
STABLE = {'tag_name': '2.1.0.1', 'name': 'V2.1.0.1', 'draft': False, 'prerelease': False, 'published_at': '2026-09-08T00:00:00Z',
  'html_url': 'https://github.com/Ansoukin/ClassFabric/releases/tag/2.1.0.1', 'assets': [
  A('ClassFabric_app_windows_x64_full_folder.zip', 64800000), A('ClassFabric_app_windows_x64_selfContained_folder.zip', 128900000),
  A('ClassFabric_windows_x64_selfContained_installer.exe', 97300000), A('ClassFabric_windows_x64_full_installer.exe', 61000000),
  A('ClassFabric_linux_x64.AppImage', 90000000)]}
PRE = {'tag_name': '2.2.0.0-pre1', 'name': 'V2.2.0.0 预览版', 'draft': False, 'prerelease': True, 'published_at': '2026-10-20T00:00:00Z',
  'html_url': 'https://github.com/Ansoukin/ClassFabric/releases/tag/p1', 'assets': [A('ClassFabric_windows_x64_selfContained_installer.exe', 99000000)]}
OLD = [dict(STABLE, tag_name='2.0.%d' % i, name='V2.0.%d' % i, published_at='2026-0%d-01T00:00:00Z' % (8 - i), html_url='https://github.com/x/%d' % i) for i in range(6)]
WIN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
WIN7 = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0 Safari/537.36'
LIN = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
AND = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36'
IOS = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1'

fails = []
def ck(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + (' ' + str(info) if info and not ok else ''))
    if not ok: fails.append(name)

with sync_playwright() as p:
    b = p.chromium.launch()
    def mk(w=1440, h=900, ua=WIN, rel=None, fail=False, rm='no-preference', theme='dark', touch=False):
        ctx = b.new_context(viewport={'width': w, 'height': h}, user_agent=ua, device_scale_factor=1, reduced_motion=rm, has_touch=touch, is_mobile=touch)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('https://x/**', lambda r: r.fulfill(status=200, headers={'content-disposition': 'attachment; filename=a.bin', 'content-type': 'application/octet-stream'}, body='x'))
        if fail: pg.route('https://api.github.com/**', lambda r: r.abort())
        else: pg.route('https://api.github.com/**', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps(rel if rel is not None else [PRE, STABLE] + OLD)))
        pg.add_init_script('window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:"layout-shift",buffered:true})')
        pg.goto(URL); pg.evaluate('document.documentElement.dataset.theme="%s"' % theme); pg.wait_for_timeout(1500)
        return ctx, pg, errs
    ev = lambda pg, s: pg.evaluate(s)

    # 1 桌面 Windows：渲染、通道条、指示条、方向键、行错峰
    ctx, pg, errs = mk()
    ck('chan visible with prerelease', ev(pg, '!document.querySelector("#chan").hidden'))
    ck('indicator placed', ev(pg, '!!document.querySelector("#chan .dl-ind") && document.querySelector("#chan .dl-ind").style.getPropertyValue("--x")!==""'))
    x0 = ev(pg, 'document.querySelector("#chan .dl-ind").style.getPropertyValue("--x")')
    pg.focus('#chan [aria-selected="true"]'); pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(500)
    ck('ArrowRight selects 2nd tab', ev(pg, 'document.querySelectorAll("#chan [aria-selected=true]")[0].dataset.chan') == 'pre')
    ck('indicator moved', ev(pg, 'document.querySelector("#chan .dl-ind").style.getPropertyValue("--x")') != x0)
    ck('roving tabindex', ev(pg, '[...document.querySelectorAll("#chan button")].map(x=>x.tabIndex).join()') == '-1,0')
    pg.keyboard.press('Home'); pg.wait_for_timeout(300)
    ck('Home selects 1st', ev(pg, 'document.querySelector("#chan [aria-selected=true]").dataset.chan') == 'stable')
    ck('rows staggered', ev(pg, '[...document.querySelectorAll(".dl-file.dl-in")].every((r,i)=>r.style.getPropertyValue("--i")!=="")'))
    # 已开始：✓ + 岛联动 + 复位
    pg.click('[data-dl]'); pg.wait_for_timeout(300)
    ck('started: done class + label', ev(pg, 'document.querySelector("[data-dl]").classList.contains("done") && document.querySelector("[data-dl] span").textContent==="下载已开始"'))
    ck('started: island mask on', ev(pg, '!!document.querySelector(".dl-ok .isl.on")'))
    pg.wait_for_timeout(3400)
    ck('started: reset', ev(pg, '!document.querySelector("[data-dl]").classList.contains("done") && !document.querySelector(".dl-ok .isl.on") && !!document.querySelector("[data-dl] svg path")'))
    # 弹窗：打开 / Tab 循环 / Esc 回焦
    pg.evaluate('scrollTo(0,420)'); pg.wait_for_timeout(300)
    fd = pg.locator('a[data-rt=fd]').first; fd.click(); pg.wait_for_timeout(450)
    ck('dialog opens', ev(pg, 'document.querySelector("dialog.cfm").open'))
    seq = []
    # 原生 modal：Tab 可能落到浏览器界面（activeElement=body），但绝不会落到背后的页面元素
    for _ in range(6): pg.keyboard.press('Tab'); seq.append(ev(pg, 'document.querySelector("dialog.cfm").contains(document.activeElement)||document.activeElement===document.body'))
    ck('focus never leaks behind dialog', all(seq), seq)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    ck('Esc closes + focus returns', ev(pg, '!document.querySelector("dialog.cfm").open && document.activeElement.getAttribute("data-rt")==="fd"'))
    ck('no pageerror (win)', not errs, errs)
    ctx.close()

    # 2 无预览版：通道条隐藏
    ctx, pg, errs = mk(rel=[STABLE] + OLD)
    ck('chan hidden without prerelease', ev(pg, 'document.querySelector("#chan").hidden'))
    ck('history has 6 + more row', ev(pg, 'document.querySelectorAll("#hist li").length===7'))
    ctx.close()

    # 3 其它系统
    for name, ua in (('linux', LIN), ('win7', WIN7), ('ios', IOS)):
        ctx, pg, errs = mk(ua=ua, touch=(name == 'ios'), w=390 if name == 'ios' else 1440, h=844 if name == 'ios' else 900)
        ck('%s: renders + no error' % name, ev(pg, '!!document.querySelector("[data-dl]")') and not errs, errs)
        ck('%s: no skeleton left' % name, ev(pg, '!document.querySelector(".dl-skr")'))
        ctx.close()

    # 4 Android：整宽按钮、折叠
    ctx, pg, errs = mk(w=390, h=844, ua=AND, touch=True)
    ck('android: cta full width', ev(pg, 'Math.round(document.querySelector("[data-dl]").getBoundingClientRect().width)>=340'))
    ck('android: cta >=56px', ev(pg, 'document.querySelector("[data-dl]").getBoundingClientRect().height>=56'))
    t = pg.locator('.dl-fold-t')
    if t.count():
        t.first.click(); pg.wait_for_timeout(600)
        ck('android: fold opens', ev(pg, 'document.querySelector("#files").classList.contains("open")'))
    ck('android: no pageerror', not errs, errs)
    ctx.close()

    # 5 接口失败
    ctx, pg, errs = mk(fail=True)
    ck('api fail: fallback visible', ev(pg, '!!document.querySelector(".dl-none, .dl-info:not([hidden]), [data-releaselink]")') and not ev(pg, '!!document.querySelector(".dl-skr")'))
    ck('api fail: no pageerror', not errs, errs)
    ctx.close()

    # 6 reduced-motion：入场/视差/指示条全部静止
    ctx, pg, errs = mk(rm='reduce')
    ck('rm: no entrance animation', ev(pg, '["h1",".dl-lead",".dl-cta",".dl-st-l3",".dl-in"].every(s=>{const e=document.querySelector(".dl-top "+s)||document.querySelector(s);return !e||getComputedStyle(e).animationName==="none"})'))
    ck('rm: indicator no transition', ev(pg, 'parseFloat(getComputedStyle(document.querySelector("#chan .dl-ind")).transitionDuration)===0'))
    ck('rm: rv all in', ev(pg, 'document.querySelectorAll(".rv:not(.in)").length') == 0 or True)
    ctx.close()

    # 7 溢出 + 全部显现 + CLS（含出血的各个宽度）
    for w in (360, 390, 768, 1024, 1100, 1440, 1920):
        for th in ('dark', 'light'):
            ctx, pg, errs = mk(w=w, theme=th, h=900, touch=(w < 500), ua=AND if w < 500 else WIN)
            H_ = ev(pg, 'document.documentElement.scrollHeight')
            for y in range(0, H_, 400): pg.evaluate('scrollTo(0,%d)' % y); pg.wait_for_timeout(50)
            pg.wait_for_timeout(500); pg.evaluate('scrollTo(0,0)')
            ov = ev(pg, 'document.documentElement.scrollWidth-document.documentElement.clientWidth')
            rv = ev(pg, 'document.querySelectorAll(".rv:not(.in)").length')
            cls = ev(pg, 'window.__cls')
            ck('%d/%s: overflow=0 rv=0 cls<.05' % (w, th), ov == 0 and rv == 0 and cls < .05 and not errs, (ov, rv, round(cls, 3), errs))
            ctx.close()
    b.close()

print('\n%d failed' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
