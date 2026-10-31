import subprocess,time
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
sel=['.hero','.scene-over','.blk.ctr','.band .copy','.flow']
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (1024,390):
      pg=b.new_page(viewport={'width':w,'height':900});pg.goto('http://localhost:8765/');pg.wait_for_timeout(500)
      H=pg.evaluate('document.body.scrollHeight')
      for y in range(0,H,600): pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(30)
      ims=[]
      for s in sel:
        el=pg.locator(s).first
        if el.count()==0: continue
        el.scroll_into_view_if_needed();pg.wait_for_timeout(300)
        f=S+'sec_%d_%d.png'%(w,len(ims));el.screenshot(path=f);ims.append(f)
      W=sum(Image.open(f).size[0] for f in ims)
      hmax=max(Image.open(f).size[1] for f in ims)
      sh=Image.new('RGB',(W+10*len(ims),hmax),'#444');x=0
      for f in ims:
        im=Image.open(f);sh.paste(im,(x,0));x+=im.size[0]+10
      sc=min(1,2000/sh.size[0]);sh=sh.resize((int(sh.size[0]*sc),int(sh.size[1]*sc)));sh.save(S+'secs_%d.png'%w);print(w,sh.size)
    b.close()
finally: srv.kill()
