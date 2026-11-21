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
    pg.route('https://api.bimg.cc/all**', lambda r: r.abort() if fail else r.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body='{"code":200,"data":[{"title":"Winter wonderland","copyright":"Banff National Park, Alberta, Canada (© Jeff Wallace/Getty Images)","copyrightlink":"https://www.bing.com/search?q=Banff"}]}'))
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
        ck('%d/%s: h1 404, kaomoji, poem (>=4 lines), signature, two buttons >=44px' % (w, th), ev('document.getElementById("nfk").textContent.length>2 && document.querySelector("h1").textContent.includes("404") && document.querySelector("h1").textContent.includes("页面不存在") && document.querySelectorAll("#nfpl .l").length>=4 && parseFloat(getComputedStyle(document.getElementById("nfpl")).fontSize)>=26 && document.querySelector(".nf-by").textContent.includes("5.5") && !document.getElementById("nfsw").hidden && [...document.querySelectorAll(".nf-b")].every(a=>a.getBoundingClientRect().height>=44)'))
        ck('%d/%s: wallpaper credit shown with title, author and a bing.com link' % (w, th), ev('(()=>{const c=document.getElementById("nfcr");return !c.hidden&&c.textContent.includes("Jeff Wallace")&&c.textContent.includes("Winter wonderland")&&/bing\\.com/.test(c.querySelector("a").href)})()'))
        ck('%d/%s: no small print (every text >=15px)' % (w, th), ev('[...document.querySelectorAll(".nf *")].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).every(e=>parseFloat(getComputedStyle(e).fontSize)>=15)'))
        c.close()
    # 接口失败 → 站内壁纸
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); mock(pg, fail=True)
    pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(1500)
    ck('fallback: failure uses a site wallpaper', pg.evaluate('document.querySelector(".nf-bg").classList.contains("on") && getComputedStyle(document.querySelector(".nf-bg i")).backgroundImage.includes("/assets/img/wp/")'))
    # 打字机：逐字出现、版面不跳动、结束后署名出现、读屏拿到完整的诗
    c2 = b.new_context(viewport={'width': 1280, 'height': 800}); pg2 = c2.new_page(); mock(pg2, fail=True)
    pg2.goto(B + '/404.html', wait_until='load'); pg2.wait_for_timeout(1900)
    t1 = pg2.evaluate('({on:document.querySelectorAll("#nfpl .c.on").length,all:document.querySelectorAll("#nfpl .c").length,bar:document.querySelector(".nf-act").getBoundingClientRect().top,k:document.querySelector(".nf-k").getBoundingClientRect().top,by:getComputedStyle(document.querySelector(".nf-by")).opacity,cur:document.querySelectorAll("#nfpl .c.cur").length})')
    ck('typewriter: typing in progress, one caret, signature still hidden', 0 < t1['on'] < t1['all'] and t1['cur'] == 1 and t1['by'] == '0', t1)
    pg2.wait_for_function('document.querySelector(".nf-in").classList.contains("done")', timeout=25000); pg2.wait_for_timeout(1100)
    t2 = pg2.evaluate('({on:document.querySelectorAll("#nfpl .c.on").length,all:document.querySelectorAll("#nfpl .c").length,bar:document.querySelector(".nf-act").getBoundingClientRect().top,k:document.querySelector(".nf-k").getBoundingClientRect().top,by:getComputedStyle(document.querySelector(".nf-by")).opacity,label:document.getElementById("nfpl").getAttribute("aria-label"),text:[...document.querySelectorAll("#nfpl .l")].map(e=>e.textContent).join("")})')
    ck('typewriter: all characters shown, signature visible, aria-label has the whole poem', t2['on'] == t2['all'] and t2['by'] == '1' and t2['label'] == t2['text'] and len(t2['label']) > 40, t2)
    ck('typewriter: layout does not move while typing', abs(t1['bar'] - t2['bar']) < 1 and abs(t1['k'] - t2['k']) < 1, (t1, t2))
    pg2.click('#nfsw'); sw_by = pg2.evaluate('(()=>{const e=document.querySelector(".nf-by");return [getComputedStyle(e).opacity,document.querySelector(".nf-in").classList.contains("done")]})()')
    ck('swap poem: signature hidden immediately (never before the typewriter)', sw_by == ['0', False], sw_by)
    c2.close()
    # 全部诗：两种署名都出现，每首都不溢出 360px、至少 4 行
    c3 = b.new_context(viewport={'width': 360, 'height': 800}); pg3 = c3.new_page(); mock(pg3, fail=True)
    pg3.goto(B + '/404.html', wait_until='load'); pg3.wait_for_timeout(300)
    seen3 = pg3.evaluate('() => { var out = {by: {}, bad: 0}; var btn = document.getElementById("nfsw"); for (var i = 0; i < 24; i++) { btn.click(); var by = document.querySelector(".nf-by").textContent; out.by[by] = (out.by[by] || 0) + 1; if (document.documentElement.scrollWidth > innerWidth || document.querySelectorAll("#nfpl .l").length < 4) out.bad++; } return out; }')
    ck('all poems: both signatures appear, every poem fits 360px and has >=4 lines', '—— Sonnet 5.5' in seen3['by'] and '—— Haiku 5.5' in seen3['by'] and seen3['bad'] == 0, seen3)
    c3.close()
    # 「换一首」：每次都换，颜文字跟着换
    pg.wait_for_timeout(300); seen = []
    for i in range(8):
        pg.click('#nfsw'); pg.wait_for_timeout(330); seen.append(pg.evaluate('document.getElementById("nfk").textContent+"|"+document.querySelector("#nfpl .l").textContent'))
    ck('swap: every click changes the poem and kaomoji', all(a != b2 for a, b2 in zip(seen, seen[1:])) and pg.evaluate('document.querySelectorAll("#nfpl .l").length>=4'), seen)
    c.close()
    # 刷新：随机、不连续重复
    c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); mock(pg, fail=True); seen = []
    for i in range(9):
        pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(100); seen.append(pg.evaluate('document.querySelector("#nfpl .l").textContent'))
    ck('poems: random per load, never the same twice in a row, >=4 distinct', all(a != b2 for a, b2 in zip(seen, seen[1:])) and len(set(seen)) >= 4, seen)
    c.close()
    c = b.new_context(viewport={'width': 1440, 'height': 800}, reduced_motion='reduce'); pg = c.new_page(); mock(pg); pg.goto(B + '/404.html', wait_until='load'); pg.wait_for_timeout(500)
    ck('reduced motion: whole poem shown at once, no animations or transitions', pg.evaluate('[...document.querySelectorAll(".nf *")].every(e=>getComputedStyle(e).animationName==="none") && getComputedStyle(document.querySelector(".nf-bg i")).transitionDuration==="0s" && getComputedStyle(document.querySelector(".nf-k")).transitionDuration==="0s" && document.querySelectorAll("#nfpl .c.on").length===document.querySelectorAll("#nfpl .c").length && document.querySelector(".nf-in").classList.contains("done") && document.querySelector(".nf-bg").classList.contains("on")'))
    c.close(); b.close()
print('\n%d/%d passed' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
