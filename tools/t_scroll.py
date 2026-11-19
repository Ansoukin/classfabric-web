"""桌面端滚动规范回归：时间线动画只动合成属性；≥900px 无滚动淡入；首屏收缩终态是圆角卡片；无横向溢出。"""
import sys, http.server, socketserver, threading, os
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=R, **k)
    def log_message(s, *a): pass
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); srv.daemon_threads = True
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = 'http://127.0.0.1:%d' % srv.server_address[1]
OKP = {'transform', 'opacity', 'pointerEvents', 'translate', 'scale', 'rotate'}
JS = '''()=>{const bad=[];for(const a of document.getAnimations()){const t=a.timeline&&a.timeline.constructor.name;if(t!=='ScrollTimeline'&&t!=='ViewTimeline')continue;
 for(const k of a.effect.getKeyframes())for(const p in k)if(!['offset','easing','composite','computedOffset'].includes(p))bad.push([a.animationName,p])}return bad}'''
ok = fail = 0
def chk(n, c, d=''):
    global ok, fail
    if c: ok += 1; print('PASS', n)
    else: fail += 1; print('FAIL', n, d)
with sync_playwright() as p:
    b = p.chromium.launch()
    for page in ('/', '/download.html', '/about.html'):
        for w, h in ((1440, 900), (1280, 720)):
            c = b.new_context(viewport={'width': w, 'height': h}); pg = c.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e))); pg.route('https://**', lambda r: r.abort())
            pg.goto(B + page, wait_until='load'); pg.wait_for_timeout(900)
            H_ = pg.evaluate('document.documentElement.scrollHeight'); y = 0
            while y < H_:
                y += 700; pg.evaluate('y=>scrollTo({top:y,behavior:"instant"})', y); pg.wait_for_timeout(40)
            bad = [x for x in pg.evaluate(JS) if x[1] not in OKP]
            chk('%s @%d: scroll-timeline keyframes only transform/opacity' % (page, w), not bad, bad)
            rv = pg.evaluate('[...document.querySelectorAll(".rv")].filter(e=>{const s=getComputedStyle(e);return s.opacity!=="1"||s.transitionDuration.split(",").some(x=>parseFloat(x)>0)&&!e.closest(".hz")}).length')
            chk('%s @%d: no scroll reveal on .rv (desktop)' % (page, w), rv == 0, rv)
            chk('%s @%d: no overflow / no errors' % (page, w), pg.evaluate('document.documentElement.scrollWidth-innerWidth') == 0 and not errs, errs)
            if page == '/' and w == 1440:
                pg.evaluate('scrollTo({top:0,behavior:"instant"})'); pg.wait_for_timeout(300)
                pg.evaluate('y=>scrollTo({top:y,behavior:"instant"})', int(h * .95)); pg.wait_for_timeout(400)
                r = pg.evaluate('(()=>{const e=document.querySelector(".hz-bg"),s=getComputedStyle(e),b=e.getBoundingClientRect();return [s.borderTopLeftRadius,Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]})()')
                chk('hero end-state is the rounded inset card', r[0] == '16px' and r[1] > 20 and r[2] > 60 and r[3] < 1440 - 20 and r[4] < h, r)
                pg.evaluate('scrollTo({top:0,behavior:"instant"})'); pg.wait_for_timeout(400)
                r = pg.evaluate('(()=>{const b=document.querySelector(".hz-bg").getBoundingClientRect();return [b.left,b.top,b.right,b.bottom]})()')
                chk('hero start-state covers the viewport', r[0] <= 0 and r[1] <= 0 and r[2] >= 1440 and r[3] >= h, r)
            c.close()
    b.close()
print('\n%d/%d passed' % (ok, ok + fail)); sys.exit(1 if fail else 0)
