import sys, time, subprocess, json
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
names=[]
for arch in ('x64','x86','arm64'):
    names+=['ClassFabric_windows_%s_selfContained_installer.exe'%arch,'ClassFabric_app_windows_%s_selfContained_folder.zip'%arch,'ClassFabric_app_windows_%s_full_folder.zip'%arch,'ClassFabric_app_windows_%s_full_singleFile.exe'%arch]
names+=['ClassFabric_app_linux_x64_full_folder.zip','ClassFabric_app_macos_arm64_full_folder.zip','checksums.sha256','Source code (zip)']
mk=lambda tag,pre:{"tag_name":tag,"name":tag,"draft":False,"prerelease":pre,"published_at":"2026-09-08T00:00:00Z","html_url":"https://github.com/Ansoukin/ClassFabric/releases/tag/"+tag,"assets":[{"name":n,"size":60000000+i*3000000,"browser_download_url":"https://x/"+n} for i,n in enumerate(names)]}
REL=[mk('2.1.0.1',False),mk('2.1.0.0',False)]
SC=[('win64','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36',1280),
    ('winarm','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36',1280),
    ('android','Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36',390),
    ('mac','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36',1280)]
page=sys.argv[1] if len(sys.argv)>1 else 'download.html'
srv=subprocess.Popen(['python3','-m','http.server','8769'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); ims=[]
        for n,ua,w in SC:
            ctx=b.new_context(user_agent=ua,viewport={'width':w,'height':900},has_touch=(n=='android'),is_mobile=(n=='android'))
            if n=='winarm': ctx.add_init_script("Object.defineProperty(navigator,'userAgentData',{value:{getHighEntropyValues:()=>Promise.resolve({architecture:'arm',bitness:'64'})}})")
            pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.route('https://api.github.com/**',lambda r:r.fulfill(status=200,content_type='application/json',body=json.dumps(REL)))
            pg.goto('http://localhost:8769/'+page); pg.wait_for_timeout(1100)
            pg.screenshot(path=S+'d_%s.png'%n,full_page=True); print(n,'errs',errs); ims.append(Image.open(S+'d_%s.png'%n))
        sc=.45; ims=[i.resize((int(i.width*sc),int(i.height*sc))) for i in ims]; H=min(max(i.height for i in ims),1500)
        out=Image.new('RGB',(sum(i.width for i in ims)+8*3,H),(128,128,128)); x=0
        for i in ims: out.paste(i.crop((0,0,i.width,H)),(x,0)); x+=i.width+8
        out.save(S+'dsheet.png'); print(out.size)
finally: srv.kill()
