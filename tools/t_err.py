import sys, time, subprocess
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(['python3','-m','http.server','8771'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':int(sys.argv[1]) if len(sys.argv)>1 else 1440,'height':900})
        pg.on('pageerror',lambda e:print('ERR',e.message,(e.stack or '')[:400]))
        for u in ['index.html','download.html','about.html']:
            pg.goto('http://localhost:8771/'+u); pg.wait_for_timeout(1500)
        b.close()
finally: srv.kill()
