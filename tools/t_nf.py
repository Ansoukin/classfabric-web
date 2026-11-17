"""404 页回归：python3 tools/t_nf.py（Bing 壁纸与站内壁纸都用 Playwright 路由模拟，不访问外网）"""
import os, sys, threading, http.server, socketserver
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
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
src = rd('404.html')
IMG = open(os.path.join(ROOT, 'assets/img/wp/pine.webp'), 'rb').read()
def mock(pg, fail=False, log=None):
    def api(r):
        if log is not None: log.append(r.request.url)
        r.abort() if fail else r.fulfill(status=200, content_type='image/webp', body=IMG)
    pg.route('https://api.bimg.cc/today**', api)
ck('seo: noindex, no canonical / hreflang / JSON-LD / og:url', 'noindex,follow' in src and not any(k in src for k in ('rel="canonical"', 'hreflang', 'ld+json', 'og:url')))
ck('seo: one h1; fallback poem + signature in the HTML; swap button hidden until JS', src.count('<h1') == 1 and 'Sonnet 5.5' in src and 'nf-pl' in src and 'id="nfsw" type="button" hidden' in src)
ck('seo: 404 is not in the sitemap, production host', '404.html' not in rd('sitemap.xml') and 'https://cf.ansoukin.top/' in rd('sitemap.xml') and 'cf.ansoukin.top/sitemap.xml' in rd('robots.txt'))
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h, th, size in ((360, 800, 'dark', 'w=1080&h=1920'), (390, 800, 'light', 'w=1080&h=1920'), (1024, 800, 'dark', 'w=1366&h=768'), (1440, 800, 'light', 'w=1920&h=1080'), (1920, 900, 'dark', 'w=1920&h=1080')):
        c = b.new_context(viewport={'width': w, 'height': h}, color_scheme=th); pg = c.new_page(); errs = []; log = []
        pg.on('pageerror', lambda e: errs.append(str(e))); mock(pg, log=log)
        pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(1800)
        ev = pg.evaluate
        ck('%d/%s: no overflow, no pageerror' % (w, th), ev('document.documentElement.scrollWidth<=innerWidth') and not errs, errs[:1])
        ck('%d/%s: Bing wallpaper requested with the right size and shown' % (w, th), len(log) == 1 and size + '&mkt=zh-CN' in log[0] and ev('document.querySelector(".nf-bg").classList.contains("on") && getComputedStyle(document.querySelector(".nf-bg i")).backgroundImage.includes("api.bimg.cc/today")'), log)
        ck('%d/%s: dialog shows kaomoji, 4 poem lines, signature, two buttons >=40px' % (w, th), ev('document.getElementById("nfk").textContent.length>2 && document.querySelectorAll("#nfpl span").length===4 && document.querySelector(".nf-by").textContent.includes("Sonnet 5.5") && !document.getElementById("nfsw").hidden && [...document.querySelectorAll(".cfm-btn")].every(a=>a.getBoundingClientRect().height>=40)'))
        ck('%d/%s: no small print (every text >=15px)' % (w, th), ev('[...document.querySelectorAll(".nf *")].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).every(e=>parseFloat(getComputedStyle(e).fontSize)>=15)'))
        c.close()
    # 接口失败 → 站内壁纸
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); mock(pg, fail=True)
    pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(1500)
    ck('fallback: failure uses a site wallpaper', pg.evaluate('document.querySelector(".nf-bg").classList.contains("on") && getComputedStyle(document.querySelector(".nf-bg i")).backgroundImage.includes("/assets/img/wp/")'))
    # 「换一首」：每次都换，颜文字跟着换
    pg.wait_for_timeout(300); seen = []
    for i in range(8):
        pg.click('#nfsw'); pg.wait_for_timeout(330); seen.append(pg.evaluate('document.getElementById("nfk").textContent+"|"+document.querySelector("#nfpl span").textContent'))
    ck('swap: every click changes the poem and kaomoji, 4 lines each time', all(a != b2 for a, b2 in zip(seen, seen[1:])) and pg.evaluate('document.querySelectorAll("#nfpl span").length===4 && !document.querySelector(".nf-dlg").classList.contains("sw")'), seen)
    c.close()
    # 刷新：随机、不连续重复
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); mock(pg, fail=True); seen = []
    for i in range(9):
        pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(100); seen.append(pg.evaluate('document.querySelector("#nfpl span").textContent'))
    ck('poems: random per load, never the same twice in a row, >=4 distinct', all(a != b2 for a, b2 in zip(seen, seen[1:])) and len(set(seen)) >= 4, seen)
    c.close()
    c = b.new_context(viewport={'width': 1440, 'height': 800}, reduced_motion='reduce'); pg = c.new_page(); mock(pg); pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(500)
    ck('reduced motion: no animations or transitions, dialog and wallpaper shown', pg.evaluate('[...document.querySelectorAll(".nf *")].every(e=>getComputedStyle(e).animationName==="none") && getComputedStyle(document.querySelector(".nf-bg i")).transitionDuration==="0s" && getComputedStyle(document.querySelector(".nf-k")).transitionDuration==="0s" && getComputedStyle(document.querySelector(".nf-dlg")).opacity==="1" && document.querySelector(".nf-bg").classList.contains("on")'))
    c.close(); b.close()
print('\n%d/%d passed' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
