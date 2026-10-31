import subprocess,time
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (1440,700):
      pg=b.new_page(viewport={'width':w,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
      pg.goto('http://localhost:8765/');pg.wait_for_timeout(800)
      a=pg.locator('.ed2');a.scroll_into_view_if_needed();pg.wait_for_timeout(400)
      a.locator('td.c[data-r="3"][data-d="6"]').click();a.locator('[data-sub="历史"]').click()
      a.screenshot(path=S+'e1_%d.png'%w)
      a.locator('.e2tabs span[data-v="tl"]').click();pg.wait_for_timeout(200)
      a.locator('.tb3[data-i="2"]').click()
      h=a.locator('.hd.b').bounding_box();pg.mouse.move(h['x']+20,h['y']+4);pg.mouse.down();pg.mouse.move(h['x']+20,h['y']+40,steps=6);pg.mouse.up()
      pg.wait_for_timeout(200);a.screenshot(path=S+'e2_%d.png'%w)
      print(w,errs,a.locator('[data-te]').input_value(),a.locator('[data-ts]').input_value())
      a.locator('.e2tabs span[data-v="sj"]').click();a.locator('.e2tabs span[data-v="sw"]').click();pg.wait_for_timeout(200)
      a.screenshot(path=S+'e3_%d.png'%w);print(errs)
    b.close()
finally: srv.kill()
