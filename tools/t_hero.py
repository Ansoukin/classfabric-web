import sys, time, subprocess
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
w=int(sys.argv[1]); theme=sys.argv[2]
srv=subprocess.Popen(['python3','-m','http.server','8767'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':1000}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8767/index.html'); pg.add_style_tag(content='html{scroll-behavior:auto!important}')
        pg.evaluate('document.documentElement.dataset.theme="%s"'%theme)
        pg.evaluate("document.querySelector('#heroDesk').scrollIntoView({block:'center'})"); pg.wait_for_timeout(600)
        desk=pg.locator('#heroDesk'); wrap=pg.locator('.dctl')
        for i,t in enumerate([1200,3200,3600,4200,5200,9000,6500]):
            pg.wait_for_timeout(t)
            box=desk.bounding_box(); cb=wrap.bounding_box()
            pg.screenshot(path=S+'hero%d.png'%i,clip={'x':0,'y':max(0,cb['y']-10),'width':w,'height':min(1000-max(0,cb['y']-10),box['y']+box['height']-cb['y']+20)})
        print('errs',errs)
        b.close()
finally: srv.kill()
