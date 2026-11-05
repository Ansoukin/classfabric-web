import sys, time, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
page, theme, w = sys.argv[1], sys.argv[2], int(sys.argv[3]); seg=int(sys.argv[4]) if len(sys.argv)>4 else 2600
srv=subprocess.Popen(['python3','-m','http.server','8775'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto('http://localhost:8775/'+page); pg.add_style_tag(content='html{scroll-behavior:auto!important}.rv{opacity:1!important;transform:none!important}'); pg.evaluate('document.documentElement.dataset.theme="%s"'%theme)
        H=pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,500): pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(40)
        pg.evaluate('scrollTo(0,0)'); pg.wait_for_timeout(600)
        pg.screenshot(path=S+'full.png',full_page=True); b.close()
finally: srv.kill()
im=Image.open(S+'full.png'); n=0
for y in range(0,im.height,seg):
    c=im.crop((0,y,im.width,min(im.height,y+seg))); c=c.resize((c.width//2,c.height//2)); c.save(S+'seg%d.png'%n); n+=1
print(im.size,n)
