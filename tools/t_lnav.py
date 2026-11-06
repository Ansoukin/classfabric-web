import sys,time,subprocess
from playwright.sync_api import sync_playwright
SP=sys.argv[1]
srv=subprocess.Popen(['python3','-m','http.server','8773'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.7)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8773/index.html?view=pc'); pg.add_style_tag(content='html{scroll-behavior:auto!important}'); pg.wait_for_timeout(1000)
    print('lnav before',pg.evaluate("document.getElementById('lnav').classList.contains('on')"))
    for i,sel in enumerate(['#features','#custom','#grow','#start','#faqs']):
        pg.evaluate("scrollTo(0,document.querySelector('%s').getBoundingClientRect().top+scrollY+%d)"%(sel,200 if sel=='#features' else 100)); pg.wait_for_timeout(700)
        print(sel,'on:',pg.evaluate("[document.getElementById('lnav').classList.contains('on'),[...document.querySelectorAll('#lnav .ls a.on')].map(a=>a.textContent)]"))
        if i==1: pg.screenshot(path=SP+'/ln.png',clip={'x':0,'y':0,'width':1440,'height':200})
    print(pg.evaluate("document.querySelector('script[type=speculationrules]')?.textContent"), pg.evaluate("document.querySelector('.bld').textContent"))
    pg.keyboard.press('Tab'); pg.keyboard.press('Tab'); pg.wait_for_timeout(200); pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(300); pg.screenshot(path=SP+'/fo.png',clip={'x':0,'y':0,'width':1440,'height':80})
    print(errs); b.close()
finally: srv.kill()
