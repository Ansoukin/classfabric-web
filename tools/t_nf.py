"""404 页回归：python3 tools/t_nf.py（Bing 与站内壁纸都用 Playwright 路由模拟，不访问外网）"""
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
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
src = rd('404.html')
IMG = open(os.path.join(ROOT, 'assets/img/wp/pine.webp'), 'rb').read()
OK = {'url': 'https://www.bing.com/th?id=OHR.Test_1920x1080.jpg', 'copyright': '测试风景 (© Someone/Getty Images)', 'copyright_link': 'https://www.bing.com/search?q=test'}
def mock(pg, data=OK, fail=False, log=None):
    def api(r):
        if log is not None: log.append(r.request.url)
        if fail: return r.abort()
        r.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body=json.dumps(data))
    pg.route('**/bing.biturl.top/**', api)
    pg.route('https://www.bing.com/th**', lambda r: r.fulfill(status=200, content_type='image/webp', body=IMG))
    pg.route('https://evil.example/**', lambda r: (log.append('EVIL') if log is not None else None) or r.abort())
ck('seo: noindex, no canonical / hreflang / JSON-LD / og:url', 'noindex,follow' in src and not any(k in src for k in ('rel="canonical"', 'hreflang', 'ld+json', 'og:url')))
ck('seo: one h1, fallback poem + signature in the HTML', src.count('<h1') == 1 and 'Sonnet 5.5' in src and 'nf-pl' in src)
ck('seo: 404 is not in the sitemap, production host', '404.html' not in rd('sitemap.xml') and 'https://cf.ansoukin.top/' in rd('sitemap.xml') and 'cf.ansoukin.top/sitemap.xml' in rd('robots.txt'))
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, th in ((360, 'dark'), (390, 'light'), (1024, 'dark'), (1440, 'light'), (1920, 'dark')):
        c = b.new_context(viewport={'width': w, 'height': 800}, color_scheme=th); pg = c.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); mock(pg)
        pg.goto(B + '/404.html?x=/gone', wait_until='load'); pg.wait_for_timeout(2600)
        ev = pg.evaluate
        ck('%d/%s: no overflow, no pageerror' % (w, th), ev('document.documentElement.scrollWidth<=innerWidth') and not errs, errs[:1])
        ck('%d/%s: Bing wallpaper shown with credit, h1 revealed' % (w, th), ev('document.querySelector(".nf-bg").classList.contains("on") && getComputedStyle(document.querySelector(".nf-bg i")).backgroundImage.includes("bing.com/th") && !document.getElementById("nfc").hidden && document.getElementById("nfcl").href.startsWith("https://www.bing.com/") && !document.querySelector(".rv:not(.in)")'))
        ck('%d/%s: kaomoji, poem (4 lines), signature, path, CTA >=44px' % (w, th), ev('document.getElementById("nfk").textContent.length>2 && document.querySelectorAll(".nf-pl span").length===4 && document.querySelector(".nf-by").textContent.includes("Sonnet 5.5") && document.getElementById("nfp").textContent.includes("/gone") && document.querySelector(".nf-cta .btn").getBoundingClientRect().height>=44'))
        c.close()
    # 当天只请求一次接口（同一浏览器上下文里再开一次走缓存）
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); log = []; mock(pg, log=log)
    pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(1500); pg.goto(B + '/404.html?again', wait_until='load'); pg.wait_for_timeout(1500)
    ck('cache: API requested once per day', len(log) == 1 and pg.evaluate('document.querySelector(".nf-bg").classList.contains("on") && !document.getElementById("nfc").hidden'), log)
    c.close()
    # 接口失败 → 站内壁纸，无署名条
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); mock(pg, fail=True)
    pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(1500)
    ck('fallback: API failure uses a site wallpaper, no credit', pg.evaluate('document.querySelector(".nf-bg").classList.contains("on") && getComputedStyle(document.querySelector(".nf-bg i")).backgroundImage.includes("/assets/img/wp/") && document.getElementById("nfc").hidden'))
    c.close()
    # 接口返回非 bing.com 地址 → 不请求、不采用
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); log = []; mock(pg, data={'url': 'https://evil.example/x.jpg', 'copyright': 'x', 'copyright_link': 'https://evil.example/'}, log=log)
    pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(1500)
    ck('safety: non-bing image address is rejected', 'EVIL' not in log and pg.evaluate('getComputedStyle(document.querySelector(".nf-bg i")).backgroundImage.includes("/assets/img/wp/")'))
    c.close()
    # 版权链接不是 bing.com → 只显示文字，不生成链接
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); mock(pg, data=dict(OK, copyright_link='https://evil.example/'))
    pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(1500)
    ck('safety: non-bing credit link is not rendered as a link', pg.evaluate('!document.getElementById("nfcl").getAttribute("href") && document.getElementById("nfct").textContent.length>2'))
    c.close()
    # 诗：随机、不连续重复
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); mock(pg, fail=True); seen = []
    for i in range(9):
        pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(120); seen.append(pg.evaluate('document.querySelector(".nf-pt").textContent'))
    ck('poems: random, never the same twice in a row, >=4 distinct', all(a != b2 for a, b2 in zip(seen, seen[1:])) and len(set(seen)) >= 4, seen)
    c.close()
    c = b.new_context(viewport={'width': 1440, 'height': 800}, reduced_motion='reduce'); pg = c.new_page(); mock(pg); pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(600)
    ck('reduced motion: no animations, no transitions, wallpaper shown', pg.evaluate('[...document.querySelectorAll(".nf *")].every(e=>getComputedStyle(e).animationName==="none") && getComputedStyle(document.querySelector(".nf-bg i")).transitionDuration==="0s" && document.querySelector(".nf-bg").classList.contains("on")'))
    c.close(); b.close()
print('\n%d/%d passed' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
