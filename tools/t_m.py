import sys, time, subprocess, json
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
page=sys.argv[1]; theme=sys.argv[2]; cols=int(sys.argv[3]); sc=float(sys.argv[4]); w=int(sys.argv[5]) if len(sys.argv)>5 else 390
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
srv=subprocess.Popen(['python3','-m','http.server','8773'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx=b.new_context(user_agent=UA,viewport={'width':w,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append('C:'+m.text) if m.type=='error' else None)
        pg.route('https://api.github.com/**',lambda r:r.fulfill(status=200,content_type='application/json',headers={'access-control-allow-origin':'*'},body=json.dumps([{"tag_name":"2.1.0.1","name":"2.1.0.1","draft":False,"prerelease":False,"published_at":"2026-09-08T00:00:00Z","html_url":"https://x","assets":[{"name":"ClassFabric_windows_x64_selfContained_installer.exe","size":97000000,"browser_download_url":"https://x/a"},{"name":"ClassFabric_app_windows_x64_full_folder.zip","size":64000000,"browser_download_url":"https://x/b"},{"name":"ClassFabric_app_windows_x86_full_folder.zip","size":60000000,"browser_download_url":"https://x/c"}]}])))
        pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
        pg.goto('http://localhost:8773/'+page,wait_until='load'); pg.wait_for_timeout(500); print('url',pg.url)
        pg.add_style_tag(content='html{scroll-behavior:auto!important}.mr{opacity:1!important;transform:none!important}'); pg.evaluate('document.documentElement.dataset.theme="%s"'%theme)
        H=pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0,H,600): pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(30)
        pg.evaluate('scrollTo(0,0)'); pg.wait_for_timeout(900)
        print('docW',pg.evaluate('document.documentElement.scrollWidth'),'H',H)
        pg.evaluate('scrollTo(0,0)'); pg.wait_for_timeout(300)
        tiles=[]
        for y in range(0,H,844):
            pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(120)
            sy=pg.evaluate('scrollY'); pg.screenshot(path=S+'_t.png'); t=Image.open(S+'_t.png').copy(); tiles.append((sy,t))
        full=Image.new('RGB',(tiles[0][1].width,int(H*2)),(0,0,0))
        for sy,t in tiles: full.paste(t,(0,int(sy*2)))
        full.save(S+'m_full.png'); print('errs',[e for e in errs if 'ERR_FAILED' not in e][:5]); b.close()
finally: srv.kill()
im=Image.open(S+'m_full.png'); im=im.resize((int(im.width*sc/2),int(im.height*sc/2))); ch=-(-im.height//cols)
out=Image.new('RGB',(im.width*cols+8*(cols-1),ch),(128,128,128))
for i in range(cols): out.paste(im.crop((0,i*ch,im.width,min(im.height,(i+1)*ch))),(i*(im.width+8),0))
out.save(S+'m_sheet.png'); print(out.size)
