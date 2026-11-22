"""FAQ（弹簧手风琴：一次开一项、悬停展开、过冲落定）回归：python3 tools/t_faq.py"""
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
        ck('%s: 6 items, first open, buttons carry aria-expanded' % path, ev('(()=>{const d=[...document.querySelectorAll(".acc-i")];return d.length===6&&d[0].classList.contains("open")&&d[0].querySelector("button").getAttribute("aria-expanded")==="true"&&d[2].querySelector("button").getAttribute("aria-expanded")==="false"})()'))
        it = pg.locator('.acc-i').nth(2); it.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        pg.mouse.move(5, 5); pg.wait_for_timeout(600)
        h0 = ev('document.querySelectorAll(".acc-i")[2].getBoundingClientRect().height')
        it.locator('button').dispatch_event('click')
        hs = []
        for i in range(30): hs.append(ev('document.querySelectorAll(".acc-i")[2].getBoundingClientRect().height')); pg.wait_for_timeout(35)
        fin = hs[-1]
        ck('%s: click opens it and closes the others (exclusive)' % path, ev('document.querySelectorAll(".acc-i")[2].classList.contains("open") && !document.querySelectorAll(".acc-i")[0].classList.contains("open")') and fin > h0 + 20, (h0, fin))
        ck('%s: height springs past the target, then settles' % path, max(hs) > fin + 1 and abs(hs[-1] - hs[-2]) < 1, (round(max(hs)), round(fin)))
        it.locator('button').dispatch_event('click'); pg.wait_for_timeout(700)
        ck('%s: second click closes it' % path, not ev('document.querySelectorAll(".acc-i")[2].classList.contains("open")'))
        pg.mouse.move(700, ev('(()=>{const r=document.querySelectorAll(".acc-i")[4].getBoundingClientRect();return r.top+20})()')); pg.wait_for_timeout(200)
        pg.mouse.move(702, ev('(()=>{const r=document.querySelectorAll(".acc-i")[4].getBoundingClientRect();return r.top+22})()')); pg.wait_for_timeout(1000)
        ck('%s: hovering a closed item opens it' % path, ev('document.querySelectorAll(".acc-i")[4].classList.contains("open")'))
        ck('%s: no pageerror, no overflow' % path, not errs and ev('document.documentElement.scrollWidth<=innerWidth'), errs[:1])
        ctx.close()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page(); pg.route('https://**', lambda r: r.abort())
    pg.goto(B + '/about.html', wait_until='load'); pg.wait_for_timeout(500)
    pg.locator('.acc-i').nth(1).locator('button').dispatch_event('click'); pg.wait_for_timeout(100)
    ck('reduced motion: opens instantly, no scale transition', pg.evaluate('(()=>{const i=document.querySelectorAll(".acc-i")[1];return i.classList.contains("open")&&getComputedStyle(i).transform==="none"})()'))
    ctx.close(); b.close()
n = sum(res); print('%d/%d passed' % (n, len(res)))
raise SystemExit(0 if n == len(res) else 1)
