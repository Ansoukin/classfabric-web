import sys,time,subprocess,json
from playwright.sync_api import sync_playwright
page=sys.argv[1]; W=int(sys.argv[2]) if len(sys.argv)>2 else 1440
srv=subprocess.Popen(['python3','-m','http.server','8772'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.7)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':900}); c=pg.context.new_cdp_session(pg); c.send('Performance.enable')
    pg.add_init_script("window.__lcp=0;new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});window.__lt=0;try{new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt+=e.duration}).observe({type:'longtask',buffered:true})}catch(e){}")
    reqs=[]; pg.on('response',lambda r:reqs.append((r.url.split('localhost:8772')[-1][:60],len(r.body()) if r.ok and 'localhost' in r.url else 0)))
    pg.goto('http://localhost:8772/'+page+'?view=pc'); pg.wait_for_load_state('load'); pg.wait_for_timeout(1500)
    m={x['name']:x['value'] for x in c.send('Performance.getMetrics')['metrics']}
    print(page,'nodes',pg.evaluate('document.getElementsByTagName("*").length'),'LCP',round(pg.evaluate('window.__lcp')),'longtask ms',round(pg.evaluate('window.__lt')),
      'script s',round(m['ScriptDuration'],3),'layout s',round(m['LayoutDuration'],3),'recalc s',round(m['RecalcStyleDuration'],3),'task s',round(m['TaskDuration'],3))
    tot=sum(x[1] for x in reqs); print('bytes',tot,'reqs',len(reqs)); 
    for u,sz in sorted(reqs,key=lambda x:-x[1])[:8]: print('  ',sz,u)
    # scroll through measure frame times
    ft=pg.evaluate("""async()=>{const H=document.body.scrollHeight;let last=performance.now(),max=0,sum=0,n=0;for(let y=0;y<H;y+=500){scrollTo(0,y);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const t=performance.now();const d=t-last;last=t;sum+=d;n++;if(d>max)max=d}return [Math.round(sum/n),Math.round(max),n]}""")
    print('scroll frame avg/max ms,n',ft)
    b.close()
finally: srv.kill()
