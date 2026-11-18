"""壁纸随机回归：下载页 / 首页 / 手机首页。python3 tools/t_wp.py"""
import os, sys, threading, http.server, socketserver, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
H.log_message = lambda *a, **k: None
srv = socketserver.TCPServer(('127.0.0.1', 0), H); B = 'http://127.0.0.1:%d' % srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
ALL = {'lake', 'pine', 'dune', 'dawn', 'ember', 'bloom'}
POOL = {'d': {'lake', 'pine', 'dune'}, 't': {'pine', 'dawn', 'ember'}, 'n': {'bloom', 'ember'}}
HOUR = {3: 'n', 6: 't', 12: 'd', 18: 't', 22: 'n'}
res = []
def ck(n, ok, extra=''):
    res.append(ok); print(('PASS ' if ok else 'FAIL ') + n + (' ' + str(extra) if extra and not ok else ''))
def info(pg):
    return pg.evaluate('({k:document.documentElement.dataset.wp,m:document.documentElement.dataset.wpm,t:document.documentElement.dataset.wpt})')
with sync_playwright() as p:
    b = p.chromium.launch()
    # 1 下载页：随机两种模式都出现、图在池内、只请求一张、舞台背景匹配
    seen, modes, bad, reqs, mism = [], set(), [], [], []
    for i in range(24):
        c = b.new_context(viewport={'width': 1280, 'height': 800}); pg = c.new_page(); rq = []
        pg.on('request', lambda r, rq=rq: rq.append(r.url) if '/assets/img/wp/' in r.url else None)
        pg.goto(B + '/download.html', wait_until='load'); d = info(pg)
        seen.append(d['k']); modes.add(d['m'])
        if d['k'] not in ALL: bad.append(d)
        bg = pg.evaluate('getComputedStyle(document.querySelector(".dl-st-l1")).backgroundImage')
        if '/wp/%s.webp' % d['k'] not in bg: mism.append((d['k'], bg))
        reqs.append(len(rq)); c.close()
    ck('dl: key always valid', not bad, bad[:1])
    ck('dl: stage background = chosen wallpaper', not mism, mism[:1])
    ck('dl: both modes appear across 24 loads', modes == {'time', 'random'}, modes)
    ck('dl: >=4 distinct wallpapers across 24 loads', len(set(seen)) >= 4, set(seen))
    ck('dl: only one wallpaper file requested per load', max(reqs) == 1 and min(reqs) == 1, reqs)
    # 2 时间模式：只选符合当前时段的画面
    for h, ph in HOUR.items():
        c = b.new_context(viewport={'width': 1280, 'height': 800}); c.add_init_script('Date.prototype.getHours=function(){return %d}' % h)
        pg = c.new_page(); badt = []; tm = 0; ks = []
        for i in range(16):
            pg.goto(B + '/download.html', wait_until='domcontentloaded'); d = info(pg); ks.append(d['k'])
            if d['t'] != ph: badt.append(('phase', d))
            if d['m'] == 'time':
                tm += 1
                if d['k'] not in POOL[ph]: badt.append(d)
        ck('time mode @%02d:00 (%s): picks fit the phase (%d time-mode loads)' % (h, ph, tm), not badt and tm > 0, badt[:2])
        ck('no immediate repeat @%02d:00' % h, all(a != b2 for a, b2 in zip(ks, ks[1:])), ks)
        c.close()
    # 3 首页：大图变量 + 预加载；hero 之外的壁纸区块
    c = b.new_context(viewport={'width': 1440, 'height': 900}); pg = c.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(B + '/', wait_until='domcontentloaded'); d = info(pg)
    pre = pg.evaluate('[...document.querySelectorAll("link[rel=preload][as=image]")].map(l=>l.href)')
    ck('home: wallpaper chosen', d['k'] in ALL, d)
    ck('home: preloads the large file', any(('/wp/%s-l.webp' % d['k']) in u for u in pre), pre)
    uses = pg.evaluate('[...document.querySelectorAll(".n5-band,.n5-live,.hz-bg,.panel .wp")].map(e=>getComputedStyle(e).backgroundImage)')
    ck('home: wallpaper blocks use the chosen large file', len(uses) > 0 and all(('/wp/%s-l.webp' % d['k']) in u for u in uses), (len(uses), uses[:1]))
    ck('home: no pageerror', not errs, errs[:1]); c.close()
    # 4 手机首页：小图，预载同一张小图（首屏背景即 LCP）
    c = b.new_context(viewport={'width': 390, 'height': 800}); pg = c.new_page()
    pg.goto(B + '/m/', wait_until='domcontentloaded'); d = info(pg)
    v = pg.evaluate('document.documentElement.style.getPropertyValue("--wpl")')
    ck('m: small wallpaper variable', ('/wp/%s.webp' % d['k']) in v and '-l.webp' not in v, v)
    pre = pg.evaluate('[...document.querySelectorAll("link[rel=preload][as=image]")].map(l=>l.href)')
    ck('m: preloads the small file only', len(pre) == 1 and ('/wp/%s.webp' % d['k']) in pre[0] and '-l.webp' not in pre[0], pre)
    c.close()
    # 5 下载页：舞台只用 --wp（小图），预载同一张
    c = b.new_context(viewport={'width': 390, 'height': 800}); pg = c.new_page()
    pg.goto(B + '/download.html', wait_until='domcontentloaded'); d = info(pg)
    pre = pg.evaluate('[...document.querySelectorAll("link[rel=preload][as=image]")].map(l=>l.href)')
    ck('download: preloads the small file only', len(pre) == 1 and ('/wp/%s.webp' % d['k']) in pre[0] and '-l.webp' not in pre[0], pre)
    c.close(); b.close()
print('\n%d/%d passed' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
