"""移除 site.css 中选择器引用了「全站任何位置都不存在的 class/id」的规则。用法: python3 tools/prune_css.py [--write]"""
import re, sys, glob, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
corpus = ''
for pat in ('*.html', 'm/*.html', 'assets/js/*.js', 'tools/*.py'):
    for f in glob.glob(os.path.join(R, pat)):
        if f.endswith('prune_css.py'): continue
        corpus += open(f, encoding='utf8', errors='ignore').read() + '\n'
cache = {}
def used(n):
    if n in cache: return cache[n]
    ok = re.search(r'(?<![\w-])' + re.escape(n) + r'(?![\w-])', corpus) is not None
    if not ok:
        m = re.match(r'^(.*?)\d+$', n)
        if m and m.group(1): ok = re.search(r'(?<![\w-])' + re.escape(m.group(1)), corpus) is not None
    if not ok and '-' in n:  # 动态拼接的前缀，如 'tag-' + x
        ok = re.search(r"['\"]" + re.escape(n.rsplit('-', 1)[0]) + r"-['\"]\s*\+", corpus) is not None
    cache[n] = ok; return ok
def strip_fn(s):
    prev = None
    while prev != s:
        prev = s; s = re.sub(r':(?:not|is|where|has|nth-child|nth-of-type|lang|dir|host)\([^()]*\)', '', s)
    return s
def dead_sel(sel):
    s = strip_fn(sel)
    s = re.sub(r'\[[^\]]*\]', '', s)
    for n in re.findall(r'\.(-?[A-Za-z_][\w-]*)', s):
        if not used(n): return True
    for n in re.findall(r'#([A-Za-z_][\w-]*)', s):
        if not used(n): return True
    return False
def split_sel(p):
    out, d, cur = [], 0, ''
    for ch in p:
        if ch in '([': d += 1
        elif ch in ')]': d -= 1
        if ch == ',' and d == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur); return out
def block_end(css, i):
    d = 0; n = len(css)
    while i < n:
        c = css[i]
        if c == '/' and css[i:i+2] == '/*': i = css.index('*/', i) + 2; continue
        if c in '"\'':
            q = c; i += 1
            while css[i] != q:
                if css[i] == '\\': i += 1
                i += 1
        elif c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: return i
        i += 1
    raise ValueError
def process(css):
    out = ''; i = 0; n = len(css); removed = 0
    while i < n:
        m = re.compile(r'\s*').match(css, i); out += m.group(0); i = m.end()
        if i >= n: break
        if css.startswith('/*', i):
            j = css.index('*/', i) + 2; out += css[i:j]; i = j; continue
        j = css.index('{', i) if '{' in css[i:] else n
        semi = css.find(';', i)
        if semi != -1 and semi < j:  # @import / @charset
            out += css[i:semi+1]; i = semi + 1; continue
        pre = css[i:j]; e = block_end(css, j); body = css[j+1:e]
        if pre.lstrip().startswith('@'):
            if re.match(r'\s*@(media|supports|container|layer)', pre):
                inner, r2 = process(body); removed += r2
                if inner.strip(): out += pre + '{' + inner + '}'
                else: removed += e + 1 - i
            else: out += css[i:e+1]
        else:
            sels = split_sel(pre); keep = [s for s in sels if not dead_sel(s)]
            if len(keep) == len(sels): out += css[i:e+1]
            elif keep: out += ','.join(s.strip() if k else s for k, s in enumerate(keep)) + '{' + body + '}'; removed += len(pre) - sum(len(s) + 1 for s in keep)
            else: removed += e + 1 - i
        i = e + 1
    return out, removed
if __name__ == '__main__':
    p = os.path.join(R, 'assets/css/site.css'); css = open(p, encoding='utf8').read()
    new, r = process(css)
    print('before', len(css), 'after', len(new), 'saved', len(css) - len(new))
    if '--write' in sys.argv: open(p, 'w', encoding='utf8').write(new.rstrip() + '\n'); print('written')
