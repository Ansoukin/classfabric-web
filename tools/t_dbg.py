import subprocess,time
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1440,'height':900});pg.goto('http://localhost:8765/');pg.wait_for_timeout(500)
    print(pg.evaluate("[...document.querySelectorAll('.mtxt .mw')].slice(12,18).map(e=>{var r=e.getBoundingClientRect();var c=getComputedStyle(e);return [e.textContent,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height),c.fontSize,c.display,c.position]})"))
    b.close()
finally: srv.kill()
