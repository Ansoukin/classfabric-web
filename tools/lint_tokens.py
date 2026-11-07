import re, sys, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ['assets/css/home2.css', 'assets/css/modal.css', 'assets/css/materials.css']
bad = []
for f in FILES:
    p = os.path.join(R, f)
    if not os.path.exists(p):
        continue
    s = re.sub(r'/\*.*?\*/', '', open(p, encoding='utf8').read(), flags=re.S)
    for n, line in enumerate(s.split('\n'), 1):
        if 'mask' in line:
            continue
        if re.search(r'#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(', line):
            bad.append((f, n, '颜色字面量', line.strip()[:90]))
        for m in re.finditer(r'border-radius:([^;}]+)', line):
            if re.search(r'(?<![\w.-])[1-9]\d*(\.\d+)?px', m.group(1)) and 'var(' not in m.group(1) and '999px' not in m.group(1):
                bad.append((f, n, '圆角字面量', m.group(0)))
        for m in re.finditer(r'font-size:([^;}]+)', line):
            if re.search(r'\d+(\.\d+)?px', m.group(1)) and 'var(' not in m.group(1):
                bad.append((f, n, '字号字面量', m.group(0)))
        for m in re.finditer(r'box-shadow:([^;}]+)', line):
            v = m.group(1).strip()
            if v != 'none' and not v.startswith('var('):
                bad.append((f, n, '阴影字面量', m.group(0)))
for b in bad:
    print('%s:%d %s  %s' % b)
print('OK' if not bad else '%d 处违规' % len(bad))
sys.exit(1 if bad else 0)
