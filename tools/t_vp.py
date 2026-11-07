import sys,time,subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
SP=sys.argv[1]; page=sys.argv[2]; th=sys.argv[3]; W=int(sys.argv[4]); H=int(sys.argv[5]); out=sys.argv[6]; ys=[int(x) for x in sys.argv[7:]]
srv=subprocess.Popen(['python3','-m','http.server','8774'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.7)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8774/'+page+('&' if '?' in page else '?')+'view=pc'); pg.add_style_tag(content='html{scroll-behavior:auto!important}')
    pg.evaluate('document.documentElement.dataset.theme="%s"'%th); pg.wait_for_timeout(1200)
    ims=[]
    for i,y in enumerate(ys):
        pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(900); f='%s/_v%d.png'%(SP,i); pg.screenshot(path=f); ims.append(Image.open(f))
    w=ims[0].width//2; h=ims[0].height//2; cols=2; rows=(len(ims)+1)//2
    s=Image.new('RGB',(cols*(w+8),rows*(h+8)),(40,40,40))
    for i,im in enumerate(ims): s.paste(im.resize((w,h)),((i%cols)*(w+8),(i//cols)*(h+8)))
    s.save('%s/%s.png'%(SP,out)); print(errs,pg.evaluate('document.body.scrollHeight')); b.close()
finally: srv.kill()
