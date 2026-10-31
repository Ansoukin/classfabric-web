import subprocess,time
from playwright.sync_api import sync_playwright
JS="""(()=>{const out=[];
for(const e of document.querySelectorAll('main *')){
 const cs=getComputedStyle(e); if(!/hidden|clip/.test(cs.overflowX))continue;
 if(e.closest('.marq,.bigmq,.pmq,.vid,svg,.isl-stack,.fitbox'))continue;
 if(cs.textOverflow==='ellipsis')continue;
 if(e.scrollWidth>e.clientWidth+2&&e.clientWidth>0){
   // 有文字子孙被裁
   const er=e.getBoundingClientRect();
   for(const t of e.querySelectorAll('*')){ if(![...t.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()))continue; const r=t.getBoundingClientRect(); if(r.width&&r.right>er.right+2&&r.left<er.right){out.push([e.className||e.tagName,'->',t.className||t.tagName,t.textContent.trim().slice(0,20),Math.round(r.right-er.right)]);break;}}
 }}
return out.slice(0,30)})()"""
srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd='/home/claude/cf-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (390,820,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto('http://localhost:8765/');pg.wait_for_timeout(500)
        H=pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,700): pg.evaluate('scrollTo(0,%d)'%y);pg.wait_for_timeout(30)
        pg.wait_for_timeout(300)
        print(w);[print('  ',x) for x in pg.evaluate(JS)]
    b.close()
finally: srv.kill()
