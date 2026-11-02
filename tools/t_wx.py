import time, subprocess
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv = subprocess.Popen(['python3','-m','http.server','8769'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: m.type=='error' and 'Failed to load' not in m.text and errs.append(m.text))
        pg.goto('http://localhost:8769/index.html'); pg.wait_for_timeout(600)
        H=pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,500): pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(25)
        app=pg.locator('[data-start="widgets"] .sapp').first; app.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
        app.screenshot(path=S+'wx1.png')
        li=app.locator('.wxpane .li[data-w="文本"]'); b0=li.bounding_box(); row=app.locator('.wxrow').first.bounding_box()
        pg.mouse.move(b0['x']+40,b0['y']+30); pg.mouse.down(); pg.mouse.move(b0['x']+120,b0['y']-30,steps=4); pg.wait_for_timeout(100)
        app.screenshot(path=S+'wx2.png')
        pg.mouse.move(row['x']+row['width']/2,row['y']+20,steps=6); pg.mouse.up(); pg.wait_for_timeout(300)
        app.locator('.wxc').first.hover(); pg.wait_for_timeout(200); app.screenshot(path=S+'wx3.png')
        app.locator('.wxm').first.click(); pg.wait_for_timeout(200); app.screenshot(path=S+'wx4.png')
        app.locator('[data-wx="m-wrap"]').click(); pg.wait_for_timeout(200); app.screenshot(path=S+'wx5.png')
        app.locator('.wxmi[data-wx="wrap-轮播容器"]').click(); pg.wait_for_timeout(200)
        app.locator('[data-wx="tab-adv"]').click(); pg.wait_for_timeout(200); app.screenshot(path=S+'wx6.png')
        print(errs)
        b.close()
finally: srv.kill()
