"""FAQ（原生 <details> + 弹簧展开）回归：python3 tools/t_faq.py"""
import os, threading, http.server, socketserver
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
with sync_playwright() as p:
    b = p.chromium.launch()
    for path in ('/about.html', '/'):
        ctx = b.new_context(viewport={'width': 1440, 'height': 900}); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.route('https://**', lambda r: r.abort())
        pg.goto(B + path, wait_until='load'); pg.wait_for_timeout(600)
        ev = pg.evaluate
        ck('%s: 6 native details, first open, no heading/button inside summary' % path, ev('(()=>{const d=[...document.querySelectorAll(".acc > details.acc-i")];return d.length===6&&d[0].open&&d.slice(1).every(x=>!x.open)&&d.every(x=>!x.querySelector("summary h1,summary h2,summary h3,summary button"))})()'))
        it = pg.locator('.acc-i').nth(2); it.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        h0 = ev('document.querySelectorAll(".acc-i")[2].getBoundingClientRect().height')
        it.locator('summary').click()
        hs = []
        for i in range(24): hs.append(ev('document.querySelectorAll(".acc-i")[2].getBoundingClientRect().height')); pg.wait_for_timeout(35)
        fin = hs[-1]
        ck('%s: click opens it, others stay open (not exclusive)' % path, ev('document.querySelectorAll(".acc-i")[2].open && document.querySelectorAll(".acc-i")[0].open') and fin > h0 + 20, (h0, fin))
        sup = ev('CSS.supports("interpolate-size","allow-keywords") && CSS.supports("selector(::details-content)")')
        if sup:
            ck('%s: height animates and springs past the target, then settles' % path, max(hs) > fin + 1 and hs[0] < fin - 5 and abs(hs[-1] - hs[-2]) < 1, (round(max(hs)), round(fin), [round(x) for x in hs[:12]]))
        else:
            ck('%s: (no ::details-content here) opens instantly' % path, True)
        it.locator('summary').press('Enter'); pg.wait_for_timeout(1200)
        ck('%s: Enter on summary closes it' % path, not ev('document.querySelectorAll(".acc-i")[2].open'))
        ck('%s: no pageerror, no overflow' % path, not errs and ev('document.documentElement.scrollWidth<=innerWidth'), errs[:1])
        ctx.close()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page(); pg.route('https://**', lambda r: r.abort())
    pg.goto(B + '/about.html', wait_until='load'); pg.wait_for_timeout(500)
    ck('reduced motion: no transition on the panel', pg.evaluate('getComputedStyle(document.querySelector(".acc-i"),"::details-content").transitionDuration').replace('0s', '').replace(',', '').replace(' ', '') == '')
    ctx.close(); b.close()
print('%d/%d passed' % (sum(res), len(res)))
