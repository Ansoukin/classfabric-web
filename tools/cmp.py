import sys,os
sys.path.insert(0,'/home/claude/cf-web/tools')
import ui
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/c795c74b-c6b4-50da-bfd3-372ff0092d48/scratchpad/'
page,real,dw,dh=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
html='<meta charset=utf-8><link rel=stylesheet href="/assets/css/site.css"><body style="margin:0;background:#000"><div style="width:%dpx">%s</div>'%(dw,ui.settings_window(page,dw,dh))
open('/home/claude/cf-web/_t.html','w').write(html)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':dw,'height':dh});pg.goto('http://localhost:8765/_t.html');pg.wait_for_timeout(400);pg.screenshot(path=S+'mine.png');b.close()
a=Image.open(real).convert('RGB').crop((0,0,dw,dh));m=Image.open(S+'mine.png').convert('RGB')
o=Image.new('RGB',(dw,dh*2+6),(255,0,0));o.paste(a,(0,0));o.paste(m,(0,dh+6));o.save(S+'cmp.png')
