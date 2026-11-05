import sys, time, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
page, theme, w, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv)>5 else 5
srv = subprocess.Popen(['python3','-m','http.server','8768'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto('http://localhost:8768/'+page); pg.evaluate('document.documentElement.dataset.theme="%s"'%theme); pg.wait_for_timeout(700)
        H=pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,400): pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(40)
        pg.evaluate('scrollTo(0,0)'); pg.wait_for_timeout(400)
        pg.screenshot(path=S+'_full.png', full_page=True); b.close()
finally: srv.kill()
im = Image.open(S+'_full.png'); sc = 420/w; im = im.resize((420,int(im.height*sc)))
ch = (im.height+cols-1)//cols
sheet = Image.new('RGB',(cols*430,ch),(40,40,40))
for i in range(cols): sheet.paste(im.crop((0,i*ch,420,min(im.height,(i+1)*ch))),(i*430,0))
sheet.save(S+out+'.png'); print(sheet.size, im.height/sc)
