import subprocess,time
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
def run(w,h,n,th,sheetname,cols,tw):
  with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':w,'height':h});pg.goto('http://localhost:8765/');pg.evaluate("document.documentElement.dataset.theme='%s'"%th);pg.wait_for_timeout(600)
    H=pg.evaluate('document.documentElement.scrollHeight');ims=[]
    ys=[int(i*(H-h)/(n-1)) for i in range(n)]
    for y in range(0,H,500): pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(25)
    for i,y in enumerate(ys):
      pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(500);f=S+'sc_%s_%d.png'%(sheetname,i);pg.screenshot(path=f);ims.append(Image.open(f).convert('RGB'))
    th_=int(tw*h/w);rows=(n+cols-1)//cols
    sh=Image.new('RGB',(cols*(tw+6),rows*(th_+6)),'#333')
    for i,im in enumerate(ims): sh.paste(im.resize((tw,th_),Image.LANCZOS),((i%cols)*(tw+6),(i//cols)*(th_+6)))
    sh.save(S+'sheet_%s.png'%sheetname);print(sheetname,H,sh.size);b.close()
try:
  run(1440,900,10,'dark','dk',3,660)
  run(390,844,10,'dark','mb',5,390)
finally: srv.kill()
