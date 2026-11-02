import sys, time, subprocess
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
w=int(sys.argv[1]); theme=sys.argv[2]
srv=subprocess.Popen(['python3','-m','http.server','8770'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':1000}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8770/index.html'); pg.add_style_tag(content='html{scroll-behavior:auto!important}')
        pg.evaluate('document.documentElement.dataset.theme="%s"'%theme); pg.wait_for_timeout(600)
        ed=pg.locator('.blk.full .edpanel').first
        ed.scroll_into_view_if_needed(); pg.wait_for_timeout(900)
        ed.screenshot(path=S+'e_grid.png')
        ed.locator('.e2tabs span[data-v=sw]').click(); pg.wait_for_timeout(300); ed.screenshot(path=S+'e_sw.png')
        ed.locator('.vsw span[data-sv=cal]').click(); pg.wait_for_timeout(300)
        ed.locator('.cc .ci').nth(8).hover(); pg.wait_for_timeout(700); ed.screenshot(path=S+'e_tip.png')
        ed.locator('.cc .ci').nth(8).click(); pg.wait_for_timeout(300)
        ed.locator('.tr1').first.click(); pg.wait_for_timeout(200); ed.screenshot(path=S+'e_pop.png')
        ed.locator('[data-tok]').click(); pg.wait_for_timeout(200)
        ed.locator('.vsw span[data-sv=grid]').click(); pg.wait_for_timeout(200)
        ed.locator('[data-a=swapc]').click(); pg.wait_for_timeout(500); ed.screenshot(path=S+'e_swd.png')
        ed.locator('.e2tabs span[data-v=tl]').click(); pg.wait_for_timeout(300); ed.screenshot(path=S+'e_tl.png')
        ed.locator('.e2tabs span[data-v=sj]').click(); pg.wait_for_timeout(300); ed.screenshot(path=S+'e_sj.png')
        print('errs',errs); b.close()
finally: srv.kill()
