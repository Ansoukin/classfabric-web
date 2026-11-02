import time, subprocess
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8772'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8772/about.html'); pg.add_style_tag(content='html{scroll-behavior:auto!important}'); pg.evaluate('document.documentElement.dataset.theme="light"'); pg.wait_for_timeout(500)
        pg.screenshot(path=S+'about_top.png',clip={'x':0,'y':0,'width':1440,'height':420})
        it=pg.locator('.acc-i').nth(3); it.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
        bx=it.bounding_box(); pg.mouse.move(bx['x']+300,bx['y']+20); pg.mouse.move(bx['x']+310,bx['y']+25)
        hs=[]
        for i in range(10):
            hs.append(round(pg.locator('.acc-i').nth(3).locator('.acc-p').bounding_box()['height'])); pg.wait_for_timeout(90)
        print('heights',hs); print('open',pg.evaluate("[...document.querySelectorAll('.acc-i')].map(e=>e.classList.contains('open'))"))
        pg.wait_for_timeout(600); pg.locator('.faq').first.screenshot(path=S+'faq_light.png'); print(errs); b.close()
finally: srv.kill()
