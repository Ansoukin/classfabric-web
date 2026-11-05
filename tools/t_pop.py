import sys, time, subprocess, json
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c7b6b142-8192-5443-8ece-e8846ebd1eed/scratchpad/'
widths=[int(x) for x in sys.argv[1:]] or [1440,768,390]
srv=subprocess.Popen(['python3','-m','http.server','8771'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
JS_OUT='''(sel)=>{const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect(); let a=e.parentElement; const bad=[];
 while(a&&a!==document.body){const cs=getComputedStyle(a); if(/(hidden|clip|auto|scroll)/.test(cs.overflow+cs.overflowX+cs.overflowY)){const q=a.getBoundingClientRect(); if(r.left<q.left-1||r.right>q.right+1||r.top<q.top-1||r.bottom>q.bottom+1) bad.push((a.className||a.tagName)+':'+[Math.round(r.left-q.left),Math.round(q.right-r.right),Math.round(r.top-q.top),Math.round(q.bottom-r.bottom)].join('/'))} a=a.parentElement}
 return {w:Math.round(r.width),h:Math.round(r.height),clip:bad}}'''
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); shots=[]
        for w in widths:
            pg=b.new_page(viewport={'width':w,'height':1000}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('http://localhost:8771/index.html'); pg.add_style_tag(content='html{scroll-behavior:auto!important}.rv{opacity:1!important;transform:none!important}'); pg.wait_for_timeout(500)
            # hero cursor tracking
            bad=0; xs=[]
            for i in range(24):
                pg.wait_for_timeout(700)
                r=pg.evaluate('''()=>{const c=document.querySelector('#hCur'),v=document.querySelector('.hero .vdk'); if(!c||!v) return null; const a=c.getBoundingClientRect(),q=v.getBoundingClientRect(); return [a.left-q.left,q.right-a.left,a.top-q.top,q.bottom-a.top,getComputedStyle(c).opacity]}''')
                if r and float(r[4])>0.05 and (min(r[:4])<-2): bad+=1; xs.append([round(x) for x in r[:4]])
            print(w,'hero cursor outside samples',bad,xs[:3])
            # swap dropdown
            sw=pg.locator('.vdk-swap').first; sw.scroll_into_view_if_needed(); pg.wait_for_timeout(700)
            sw.locator('.ls').first.click(); pg.wait_for_timeout(250); sw.locator('[data-m=replace]').click(); pg.wait_for_timeout(250)
            try: sw.locator('[data-c]').click(timeout=1500); pg.wait_for_timeout(300)
            except Exception as e: print('no combo',str(e)[:60])
            print(w,'swap fly',pg.evaluate(JS_OUT,'.vdk-swap .fly.open'))
            sw.screenshot(path=S+'p_sw_%d.png'%w); shots.append(S+'p_sw_%d.png'%w)
            # editor popups
            ed=pg.locator('.blk.full .edpanel').first; ed.scroll_into_view_if_needed(); pg.wait_for_timeout(700)
            ed.locator('.e2tabs span[data-v=sw]').click(); pg.wait_for_timeout(250)
            ed.locator('.vsw span[data-sv=cal]').click(); pg.wait_for_timeout(250)
            ed.locator('.cc .ci').nth(30).click(); pg.wait_for_timeout(250)
            ed.locator('.tr1').first.click(timeout=2000); pg.wait_for_timeout(200)
            print(w,'tpop',pg.evaluate(JS_OUT,'.edpanel .tpop'))
            ed.screenshot(path=S+'p_ed_%d.png'%w)
            print(w,'errs',errs); pg.close()
        b.close()
finally: srv.kill()
