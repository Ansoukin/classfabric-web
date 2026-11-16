"""404 页回归：python3 tools/t_nf.py"""
import os, sys, threading, http.server, socketserver, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(s, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); B = 'http://127.0.0.1:%d' % srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
res = []
def ck(n, ok, extra=''):
    res.append(ok); print(('PASS ' if ok else 'FAIL ') + n + (' ' + str(extra) if extra and not ok else ''))
src = open(os.path.join(ROOT, '404.html'), encoding='utf-8').read()
ck('seo: noindex, no canonical / hreflang / JSON-LD / og:url', 'noindex,follow' in src and not any(k in src for k in ('rel="canonical"', 'hreflang', 'ld+json', 'og:url')))
ck('seo: one h1, 404 labelled', src.count('<h1') == 1 and 'aria-label="404"' in src)
ck('seo: 404 is not in the sitemap', '404.html' not in open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read())
ck('seo: sitemap/robots use the production host', 'https://cf.ansoukin.top/' in open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read() and 'cf.ansoukin.top/sitemap.xml' in open(os.path.join(ROOT, 'robots.txt'), encoding='utf-8').read())
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, th in ((360, 'dark'), (390, 'light'), (1024, 'dark'), (1440, 'light'), (1920, 'dark')):
        c = b.new_context(viewport={'width': w, 'height': 800}, color_scheme=th); pg = c.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(B + '/404.html?x=/gone', wait_until='load'); pg.wait_for_timeout(3400)
        ev = pg.evaluate
        ck('%d/%s: no overflow, no pageerror' % (w, th), ev('document.documentElement.scrollWidth<=innerWidth') and not errs, errs[:1])
        ck('%d/%s: h1 revealed, code + card visible, no wallpaper' % (w, th), ev('!document.querySelector(".rv:not(.in)") && document.querySelectorAll(".nf-code span").length===3 && document.querySelectorAll(".nf-rows ol li").length===5 && !document.documentElement.dataset.wp && !document.querySelector(".isl")'))
        ck('%d/%s: selector ends on the unscheduled slot' % (w, th), ev('Math.abs(document.querySelector(".nf-sel").getBoundingClientRect().top-document.querySelector(".nf-miss").getBoundingClientRect().top)<=1'))
        ck('%d/%s: request path shown' % (w, th), ev('[...document.querySelectorAll("[data-nfp]")].every(e=>e.textContent.includes("/gone"))'))
        ck('%d/%s: CTA and links tap targets >=44px' % (w, th), ev('[...document.querySelectorAll(".nf-cta .btn,.nf-link")].every(a=>a.getBoundingClientRect().height>=44)'))
        if w == 1440:
            pg.hover('.nf-rows ol li:nth-child(1)'); pg.wait_for_timeout(1300)
            ck('1440: hover moves the selector, leaving returns it', ev('Math.abs(document.querySelector(".nf-sel").getBoundingClientRect().top-document.querySelector(".nf-rows ol li:nth-child(1)").getBoundingClientRect().top)<=1'))
            pg.mouse.move(5, 5); pg.wait_for_timeout(1300)
            ck('1440: selector back on the unscheduled slot', ev('Math.abs(document.querySelector(".nf-sel").getBoundingClientRect().top-document.querySelector(".nf-miss").getBoundingClientRect().top)<=1'))
        c.close()
    c = b.new_context(viewport={'width': 1440, 'height': 800}, reduced_motion='reduce'); pg = c.new_page(); pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(300)
    ck('reduced motion: no animations, selector already on the slot', pg.evaluate('[...document.querySelectorAll(".nf *")].every(e=>getComputedStyle(e).animationName==="none") && Math.abs(document.querySelector(".nf-sel").getBoundingClientRect().top-document.querySelector(".nf-miss").getBoundingClientRect().top)<=1'))
    c.close(); b.close()
print('\n%d/%d passed' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
