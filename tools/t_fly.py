import time, subprocess
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8773'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':1000}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8773/index.html'); pg.add_style_tag(content='html{scroll-behavior:auto!important}'); pg.wait_for_timeout(500)
        app=pg.locator('[data-start="auto"] .sapp').first; app.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
        app.locator('[data-fk="act"]').click(); pg.wait_for_timeout(300)
        app.locator('[data-fly="act"] .mi').nth(1).hover(); pg.wait_for_timeout(100)
        app.locator('[data-fly="act"] .mi').last.click(); pg.wait_for_timeout(400)
        app.screenshot(path=S+'fly.png'); print(errs); b.close()
finally: srv.kill()
