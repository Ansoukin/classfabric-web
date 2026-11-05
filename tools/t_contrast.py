import sys, time, subprocess
from playwright.sync_api import sync_playwright
JS = r"""
() => {
 function parse(c){var m=c.match(/rgba?\(([^)]+)\)/);if(!m)return null;var p=m[1].split(',').map(parseFloat);return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}}
 function lum(c){function f(v){v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b)}
 function bgOf(el){var e=el;while(e&&e.nodeType==1){var cs=getComputedStyle(e);if(cs.backgroundImage&&cs.backgroundImage!='none')return null;var c=parse(cs.backgroundColor);if(c&&c.a>.85)return c;e=e.parentElement}return {r:255,g:255,b:255,a:1}}
 var out=[],seen={};
 var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 while(w.nextNode()){var n=w.currentNode;if(!n.textContent.trim())continue;var el=n.parentElement;if(!el||el.closest('.w,.app,.isl,.sapp,.ed2,svg,script,style,.mk,.cmpw'))continue;
  var cs=getComputedStyle(el);if(cs.visibility=='hidden'||cs.display=='none'||+cs.opacity==0)continue;var r=el.getBoundingClientRect();if(!r.width||!r.height)continue;
  var fg=parse(cs.color);var bg=bgOf(el);if(!bg||!fg)continue;
  var L1=lum(fg),L2=lum(bg);var ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
  if(ratio<3.2){var k=el.tagName+'.'+el.className+'|'+cs.color+'|'+n.textContent.trim().slice(0,14);if(seen[k])continue;seen[k]=1;out.push(ratio.toFixed(2)+' '+el.tagName+'.'+String(el.className).slice(0,30)+' '+cs.color+' on rgb('+bg.r+','+bg.g+','+bg.b+') "'+n.textContent.trim().slice(0,20)+'"')}}
 return out}
"""
page, theme, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
srv = subprocess.Popen(['python3','-m','http.server','8767'],cwd='/home/claude/classfabric-web',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto('http://localhost:8767/'+page); pg.evaluate('document.documentElement.dataset.theme="%s"'%theme); pg.wait_for_timeout(700)
        H=pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,500): pg.evaluate('scrollTo(0,%d)'%y); pg.wait_for_timeout(40)
        pg.wait_for_timeout(500)
        for l in pg.evaluate(JS): print(l)
        b.close()
finally: srv.kill()
