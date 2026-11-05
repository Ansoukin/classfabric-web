import sys, json, time, subprocess
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
page, theme, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
srv = subprocess.Popen(['python3','-m','http.server','8766'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width':w,'height':900}); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8766/'+page); pg.add_style_tag(content='html{scroll-behavior:auto!important}'); pg.evaluate('document.documentElement.dataset.theme="%s"'%theme); pg.wait_for_timeout(900)
        H = pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,400): pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(30)
        pg.evaluate('scrollTo(0,0)'); pg.wait_for_timeout(300)
        for a in sys.argv[4:]:
            name, sel = a.split('=',1)
            if sel.startswith('VP'):
                y = int(sel[2:] or 0); pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(500); pg.screenshot(path=S+name+'.png')
            else:
                if sel.startswith('@'):
                    sel = sel[1:]; pg.locator(sel).first.evaluate('e=>{e.scrollIntoView();window.scrollBy(0,-70)}'); pg.wait_for_timeout(900); pg.screenshot(path=S+name+'.png')
                else:
                    el = pg.locator(sel).first; el.scroll_into_view_if_needed(); pg.wait_for_timeout(700); el.screenshot(path=S+name+'.png')
        print('errs',errs,'H',H)
        b.close()
finally: srv.kill()
