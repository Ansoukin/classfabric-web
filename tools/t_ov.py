import subprocess,time,sys,json
from playwright.sync_api import sync_playwright
JS="""(()=>{const vw=innerWidth,out=[];
function clipped(e){for(let p=e.parentElement;p&&p!==document.body;p=p.parentElement){const o=getComputedStyle(p);if(/(hidden|auto|scroll|clip)/.test(o.overflowX)||/(hidden|auto|scroll|clip)/.test(o.overflow))return p;}return null}
for(const e of document.querySelectorAll('main *, footer *, header *, nav *')){
 if(!e.childNodes.length)continue; let hasText=[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()); if(!hasText)continue;
 const r=e.getBoundingClientRect(); if(!r.width)continue;
 const c=clipped(e);
 if(c){ // 被裁切的容器里：检查是否被容器裁掉文字(容器非滚动/传送带)
   const cr=c.getBoundingClientRect(); const cs=getComputedStyle(c);
   if(/hidden|clip/.test(cs.overflowX)&&!c.closest('.marq,.bigmq,.pmq,.fitbox,.app,.w,.panel,.gframe,.vid,.isl-stack,svg')&&(r.right>cr.right+2||r.left<cr.left-2)&&r.right>cr.left)out.push(['CLIP',e.className||e.tagName,e.textContent.trim().slice(0,24),Math.round(r.right-cr.right)]);
   continue;}
 if(r.right>vw+1||r.left<-1)out.push(['VP',e.className||e.tagName,e.textContent.trim().slice(0,24),Math.round(r.right-vw)]);
 if(e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).display!=='inline')out.push(['SW',e.className||e.tagName,e.textContent.trim().slice(0,24),e.scrollWidth-e.clientWidth]);
}
return [document.documentElement.scrollWidth-vw,out.slice(0,25)]})()"""
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for pgn in sys.argv[1:] or ['index.html']:
      for w in (360,390,768,1024,1440):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto('http://localhost:8765/'+pgn);pg.wait_for_timeout(500)
        H=pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,700): pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(30)
        pg.wait_for_timeout(300)
        r=pg.evaluate(JS);print(pgn,w,'docOverflow',r[0]);[print('   ',x) for x in r[1]]
    b.close()
finally: srv.kill()
