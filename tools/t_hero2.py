import sys, time, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
w=int(sys.argv[1]); theme=sys.argv[2]; times=[int(x) for x in sys.argv[3].split(',')]
srv=subprocess.Popen(['python3','-m','http.server','8768'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':1000}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8768/index.html'); pg.add_style_tag(content='html{scroll-behavior:auto!important}')
        pg.evaluate('document.documentElement.dataset.theme="%s"'%theme)
        pg.evaluate("document.querySelector('#heroDesk').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
        ims=[]; last=0
        for i,t in enumerate(times):
            pg.wait_for_timeout(t-last); last=t
            r=pg.evaluate("(()=>{var a=document.querySelector('.dctl').getBoundingClientRect(),d=document.querySelector('#heroDesk').getBoundingClientRect();return [a.top,d.bottom]})()")
            y=max(0,r[0]-6); pg.screenshot(path=S+'h2_%d.png'%i,clip={'x':0,'y':y,'width':w,'height':min(1000-y,r[1]-y+6)}); ims.append(Image.open(S+'h2_%d.png'%i))
        n=len(ims); cols=min(n,3); rows=(n+cols-1)//cols; cw=ims[0].width; ch=ims[0].height
        sh=Image.new('RGB',(cw*cols,ch*rows),'#000')
        for i,im in enumerate(ims): sh.paste(im,((i%cols)*cw,(i//cols)*ch))
        sh.save(S+'h2sheet.png'); print(sh.size,'errs',errs)
        pg.wait_for_timeout(500); pg.mouse.click(w/2, pg.evaluate("document.querySelector('#heroDesk').getBoundingClientRect().top")+60)
        pg.wait_for_timeout(700); print('replay hidden:',pg.evaluate("document.querySelector('#dreplay').hidden"), 'win op:',pg.evaluate("getComputedStyle(document.querySelector('.hwin')).opacity"))
        b.close()
finally: srv.kill()
