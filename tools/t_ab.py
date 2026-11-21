#!/usr/bin/env python3
"""关于页回归测试：目录条滚动联动、指示条、文案、减少动态、各宽度溢出 / CLS。自带本地服务器，不访问外网。
用法：python3 tools/t_ab.py"""
import os, sys, threading, functools, http.server
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = 'http://127.0.0.1:%d/about.html' % srv.server_address[1]
fails = []
def ck(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + (' ' + str(info) if info and not ok else ''))
    if not ok: fails.append(name)

with sync_playwright() as p:
    b = p.chromium.launch()
    def mk(w=1440, h=900, theme='dark', rm='no-preference', touch=False):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, reduced_motion=rm, has_touch=touch, is_mobile=touch)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.add_init_script('window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:"layout-shift",buffered:true})')
        pg.goto(URL); pg.evaluate('document.documentElement.dataset.theme="%s"' % theme); pg.wait_for_timeout(1500)
        return ctx, pg, errs
    ev = lambda pg, s: pg.evaluate(s)

    ctx, pg, errs = mk(w=700)
    ids = ev(pg, '[...document.querySelectorAll("#abNav a")].map(a=>a.getAttribute("href").slice(1))')
    ck('7 anchors, all targets exist', len(ids) == 7 and all(ev(pg, '!!document.getElementById("%s")' % i) for i in ids), ids)
    ck('no diagram / stage in header', ev(pg, '!document.querySelector(".ab-stage,.ab-rel,.ab-node,.ab-lane")'))
    txt = ev(pg, 'document.body.innerText')
    ck('copy: no "competitor / replacement" disclaimers', '竞品' not in txt and '替代品' not in txt and '取代' not in txt)
    ck('top: bar not stuck, no current', ev(pg, '!document.querySelector(".ab-bar").classList.contains("stuck") && !document.querySelector("#abNav [aria-current]") && !document.querySelector("#abNav").hasAttribute("data-has")'))
    pg.click('#abNav a[href="#progress"]'); pg.wait_for_timeout(1400)
    ck('click: section reached + aria-current', ev(pg, 'document.querySelector("#abNav [aria-current=true]").getAttribute("href")') == '#progress')
    ck('click: bar stuck, indicator placed', ev(pg, 'document.querySelector(".ab-bar").classList.contains("stuck") && document.querySelector("#abNav").hasAttribute("data-has") && document.querySelector("#abNav .ab-ind").style.getPropertyValue("--x")!==""'))
    ck('click: heading below sticky bars', ev(pg, 'document.querySelector("#progress h2").getBoundingClientRect().top>=document.querySelector(".ab-bar").getBoundingClientRect().bottom'))
    x1 = ev(pg, 'document.querySelector("#abNav .ab-ind").style.getPropertyValue("--x")')
    pg.click('#abNav a[href="#name"]'); pg.wait_for_timeout(1400)
    ck('indicator moves with section', ev(pg, 'document.querySelector("#abNav .ab-ind").style.getPropertyValue("--x")') != x1)
    pg.evaluate('document.getElementById("progress").scrollIntoView()'); pg.wait_for_timeout(1200)
    ck('progress bar reaches 40%', ev(pg, '(()=>{const e=document.querySelector(".ab-pb i");const m=getComputedStyle(e).transform;return m==="none"||Math.abs(parseFloat(m.split(",")[0].replace("matrix(",""))-1)<.02})()'))
    ck('progress list has rows', ev(pg, 'document.querySelectorAll("#progress .ab-list>li").length===9'))
    ck('faq kept (6 items)', ev(pg, 'document.querySelectorAll("#faq details.acc-i").length===6'))
    ck('no pageerror', not errs, errs)
    ctx.close()

    ctx, pg, errs = mk(rm='reduce')
    ck('rm: no entrance / row animations', ev(pg, '[".ab-lead",".ab-link",".ab-in"].every(s=>{const e=document.querySelector(s);return !e||getComputedStyle(e).animationName==="none"})'))
    ck('rm: indicator no transition', ev(pg, 'parseFloat(getComputedStyle(document.querySelector("#abNav .ab-ind")).transitionDuration)===0'))
    ctx.close()

    ctx, pg, errs = mk(w=390, h=844, touch=True)
    ck('mobile: nav scrolls horizontally', ev(pg, 'document.querySelector("#abNav").scrollWidth>document.querySelector("#abNav").clientWidth'))
    ck('mobile: nav links >=44px tall', ev(pg, '[...document.querySelectorAll("#abNav a")].every(a=>a.getBoundingClientRect().height>=44)'))
    ck('mobile: sections single column', ev(pg, 'getComputedStyle(document.querySelector(".ab-sec")).gridTemplateColumns.split(" ").length===1'))
    ctx.close()

    ctx, pg, errs = mk(w=1440)
    ck('desktop: only the site nav, in-page bar hidden', ev(pg, 'getComputedStyle(document.querySelector(".ab-bar")).display==="none"'))
    ck('desktop: anchor lands below site nav', (pg.click('.ab-link'), pg.wait_for_timeout(1200), ev(pg, 'document.querySelector("#switch").getBoundingClientRect().top>=56'))[2])
    ctx.close()

    for w in (360, 390, 1024, 1440, 1920):
        for th in ('dark', 'light'):
            ctx, pg, errs = mk(w=w, theme=th, touch=(w < 500))
            H = ev(pg, 'document.documentElement.scrollHeight')
            for y in range(0, H, 400): pg.evaluate('scrollTo(0,%d)' % y); pg.wait_for_timeout(50)
            pg.wait_for_timeout(500); pg.evaluate('scrollTo(0,0)')
            ov = ev(pg, 'document.documentElement.scrollWidth-document.documentElement.clientWidth')
            rv = ev(pg, 'document.querySelectorAll(".rv:not(.in)").length')
            cls = ev(pg, 'window.__cls')
            ck('%d/%s: overflow=0 rv=0 cls<.05' % (w, th), ov == 0 and rv == 0 and cls < .05 and not errs, (ov, rv, round(cls, 3), errs))
            ctx.close()
    b.close()
print('\n%d failed' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
