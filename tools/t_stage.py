import sys,time,subprocess
from playwright.sync_api import sync_playwright
SP=sys.argv[1]; th=sys.argv[2]; W=int(sys.argv[3]); H=int(sys.argv[4])
srv=subprocess.Popen(['python3','-m','http.server','8771'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.7)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://localhost:8771/index.html?view=pc'); pg.add_style_tag(content='html{scroll-behavior:auto!important}')
    pg.evaluate('document.documentElement.dataset.theme="%s"'%th); pg.wait_for_timeout(1200)
    top=pg.evaluate("document.querySelector('#features').getBoundingClientRect().top+scrollY")
    ph=pg.evaluate("document.querySelector('.n4-pn').getBoundingClientRect().height")
    print('top',top,'ph',ph,'docH',pg.evaluate('document.body.scrollHeight'))
    offs=[int(x) for x in sys.argv[5:]]
    for i,o in enumerate(offs):
        pg.evaluate('scrollTo(0,%d)'%(top+o)); pg.wait_for_timeout(900); pg.screenshot(path='%s/st_%d.png'%(SP,i))
    print(errs[:8]); b.close()
finally: srv.kill()
