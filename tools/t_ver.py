"""版本号占位（骨架）回归：python3 tools/t_ver.py —— 读到版本后，首页/手机首页/下载页不能再留着骨架底色。"""
import os, sys, json, threading, http.server, socketserver
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
REL = [{'tag_name': 'v2.1.0.1', 'name': 'v2.1.0.1', 'prerelease': False, 'draft': False, 'published_at': '2026-11-01T00:00:00Z', 'body': '', 'html_url': 'https://github.com/x', 'assets': []}]
JS = '[...document.querySelectorAll("[data-ver]")].map(e=>({t:e.textContent,cls:e.className,bg:getComputedStyle(e).backgroundImage}))'
with sync_playwright() as p:
    b = p.chromium.launch()
    for path, w in (('/', 1440), ('/', 390), ('/m/', 390), ('/download.html', 1440), ('/download.html', 390)):
        for mode in ('ok', 'fail'):
            c = b.new_context(viewport={'width': w, 'height': 800}); pg = c.new_page()
            pg.route('https://api.github.com/**', (lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps(REL))) if mode == 'ok' else (lambda r: r.abort()))
            pg.goto(B + path, wait_until='load'); pg.wait_for_timeout(1800)
            r = pg.evaluate(JS)
            ck('%s @%d (%s): version filled, no skeleton class or background left' % (path, w, mode), len(r) > 0 and all(x['t'].strip() and 'sk' not in x['cls'].split() and 'dl-sk' not in x['cls'].split() and x['bg'] == 'none' for x in r), r)
            c.close()
    b.close()
print('\n%d/%d passed' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
