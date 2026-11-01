import subprocess,time,sys
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1440,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://localhost:8765/');pg.wait_for_timeout(500)
    H=pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0,H,500): pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(20)
    sh=[]
    for sel,th in (('#cApp','dark'),('.swapblk','dark'),('#sync','dark'),('#feat','light')):
        pg.evaluate("document.documentElement.dataset.theme='%s'"%th)
        pg.evaluate("(()=>{var e=document.querySelector('%s');scrollTo({top:e.getBoundingClientRect().top+scrollY-%d,behavior:'instant'})})()"%(sel,120 if sel!='#cApp' else 300));pg.wait_for_timeout(900)
        f=S+'v16_%d.png'%len(sh);pg.screenshot(path=f);sh.append(Image.open(f).convert('RGB'))
    out=Image.new('RGB',(2*666,2*420),'#333')
    for i,im in enumerate(sh): out.paste(im.resize((660,412)),((i%2)*666,(i//2)*420))
    out.save(S+'sheet_v16.png');print(errs)
    b.close()
finally: srv.kill()
