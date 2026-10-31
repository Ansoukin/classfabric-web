import subprocess,time
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1440,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://localhost:8765/');pg.wait_for_timeout(500)
    H=pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0,H,500): pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(25)
    shots=[]
    def snap(js,name):
        pg.evaluate(js);pg.wait_for_timeout(800);f=S+name;pg.screenshot(path=f);shots.append(Image.open(f).convert('RGB'))
    snap("document.querySelector('.syncfig').scrollIntoView({block:'center'})",'v15a.png')
    snap("(()=>{var s=document.getElementById('story');scrollTo(0,s.getBoundingClientRect().top+scrollY+80)})()",'v15b.png')
    snap("(()=>{var s=document.getElementById('story');scrollTo(0,s.getBoundingClientRect().top+scrollY+s.offsetHeight*0.55)})()",'v15c.png')
    snap("document.querySelector('.swapblk').scrollIntoView({block:'center'})",'v15d.png')
    snap("document.querySelector('.wbento').scrollIntoView({block:'center'})",'v15e.png')
    snap("document.querySelector('.themes3').scrollIntoView({block:'center'})",'v15f.png')
    sh=Image.new('RGB',(3*666,2*420),'#333')
    for i,im in enumerate(shots): sh.paste(im.resize((660,412)),((i%3)*666,(i//3)*420))
    sh.save(S+'sheet_v15.png');print(errs)
    b.close()
finally: srv.kill()
