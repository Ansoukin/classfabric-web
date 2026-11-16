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
ck('seo: one h1, svg has label', src.count('<h1') == 1 and 'aria-label="404"' in src)
ck('seo: 404 is not in the sitemap', '404.html' not in open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read())
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, th in ((360, 'dark'), (390, 'light'), (1024, 'dark'), (1440, 'light'), (1920, 'dark')):
        c = b.new_context(viewport={'width': w, 'height': 800}, color_scheme=th); pg = c.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(B + '/404.html?x=/gone', wait_until='load'); pg.wait_for_timeout(1800)
        ev = pg.evaluate
        ck('%d/%s: no overflow, no pageerror' % (w, th), ev('document.documentElement.scrollWidth<=innerWidth') and not errs, errs[:1])
        ck('%d/%s: h1 revealed, island + digits visible' % (w, th), ev('!document.querySelector(".rv:not(.in)") && getComputedStyle(document.querySelector(".nf-isl .isl")).opacity==="1" && document.querySelectorAll(".nf-d").length===3 && document.querySelector(".nf-n").getBoundingClientRect().width>200'))
        ck('%d/%s: path shown, wallpaper set' % (w, th), ev('document.getElementById("nfp").textContent.includes("/gone") && !!document.documentElement.dataset.wp'))
        ck('%d/%s: CTA tap targets >=44px' % (w, th), ev('[...document.querySelectorAll(".nf-cta .btn")].every(a=>a.getBoundingClientRect().height>=44)'))
        c.close()
    c = b.new_context(viewport={'width': 1440, 'height': 800}, reduced_motion='reduce'); pg = c.new_page(); pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(500)
    ck('reduced motion: no running animations on the scene', pg.evaluate('[...document.querySelectorAll(".nf *")].every(e=>getComputedStyle(e).animationName==="none"||e.matches(".isl"))'))
    c.close(); b.close()
print('\n%d/%d passed' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
