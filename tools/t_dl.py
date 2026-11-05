import sys, time, subprocess, json
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
w=int(sys.argv[1]); theme=sys.argv[2]
REL=[{"tag_name":"2.1.0.1","draft":False,"prerelease":False,"published_at":"2026-09-08T00:00:00Z","html_url":"https://github.com/Ansoukin/ClassFabric/releases/tag/2.1.0.1","assets":[
 {"name":"ClassFabric_app_windows_x64_full_folder.zip","size":64800000,"browser_download_url":"https://x/a"},
 {"name":"ClassFabric_app_windows_x64_selfContained_folder.zip","size":128900000,"browser_download_url":"https://x/b"},
 {"name":"ClassFabric_windows_x64_selfContained_installer.exe.exe","size":97300000,"browser_download_url":"https://x/c"}]}]
srv=subprocess.Popen(['python3','-m','http.server','8769'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':900})
        pg.route('https://api.github.com/**',lambda r:r.fulfill(status=200,content_type='application/json',body=json.dumps(REL)))
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8769/download.html'); pg.evaluate('document.documentElement.dataset.theme="%s"'%theme); pg.wait_for_timeout(900)
        pg.screenshot(path=S+'dl_%s_%d.png'%(theme,w),full_page=True); print('errs',errs)
        b.close()
finally: srv.kill()
