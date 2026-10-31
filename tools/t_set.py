import subprocess,time,sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (1440,820):
      pg=b.new_page(viewport={'width':w,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
      pg.goto('http://localhost:8765/');pg.wait_for_timeout(800)
      apps=pg.locator('[data-app="settings"]');print(w,apps.count(),errs)
      a=apps.nth(0);a.scroll_into_view_if_needed();pg.wait_for_timeout(500)
      a.locator('.prov').first.click();a.locator('.exp .eh').nth(0).click()
      pg.wait_for_timeout(300);a.screenshot(path=S+'r1_%d.png'%w)
      for i,k in enumerate(['widgets','appearance','window']):
        a.locator('.nv .it[data-go="%s"]'%k).click();pg.wait_for_timeout(200)
        if k=='widgets': a.locator('.li').nth(4).click()
        a.screenshot(path=S+'r_%s_%d.png'%(k,w))
      print(errs)
    b.close()
finally: srv.kill()
