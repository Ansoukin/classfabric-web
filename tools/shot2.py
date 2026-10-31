import subprocess,sys,time
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
    page=sys.argv[1];themes=sys.argv[2].split(',');w=int(sys.argv[3]) if len(sys.argv)>3 else 1440
    with sync_playwright() as p:
        b=p.chromium.launch()
        for th in themes:
            pg=b.new_page(viewport={'width':w,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('http://localhost:8765/'+page);pg.evaluate('document.documentElement.dataset.theme="%s"'%th);pg.wait_for_timeout(1000)
            H=pg.evaluate('document.body.scrollHeight')
            for y in range(0,H,500): pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(40)
            pg.evaluate('scrollTo(0,0)');pg.wait_for_timeout(400)
            pg.screenshot(path=S+'s_%s.png'%th,full_page=True);print(th,errs,H)
        b.close()
finally: srv.kill()
