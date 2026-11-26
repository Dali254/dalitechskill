#!/usr/bin/env python3
"""Pixel-accurate contrast audit of real pages (works on gradients, images, glass).

For every visible text node: read its colour, hide all text, screenshot, and compare with the real pixels
behind it. Uses the 10th-percentile worst ratio. Needs 4.5 (3.0 for ≥24px or ≥18.66px bold).

  python3 contrast_audit.py https://site/dashboard https://site/withdraw --modes light,dark [--json out.json]
Skips text inside elements matching --skip (default: nav bars, dialogs, hidden).
"""
import io, json, re
from PIL import Image
from playwright.sync_api import sync_playwright
from _common import parser, login, set_mode

p = parser(__doc__)
p.add_argument('--modes', default='light,dark'); p.add_argument('--json')
p.add_argument('--skip', default='script,style,[hidden],[aria-hidden=true],option,select,.sr-only')
a = p.parse_args()

COLLECT = '''skip=>{const out=[],seen=new Set(),W=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 while(W.nextNode()){const t=W.currentNode;if(!t.nodeValue.trim())continue;const e=t.parentElement;if(!e||seen.has(e))continue;seen.add(e);
  if(e.closest(skip))continue;const cs=getComputedStyle(e);if(cs.visibility!=='visible')continue;
  let o=1,x=e;while(x&&x!==document.body){o*=+getComputedStyle(x).opacity;x=x.parentElement}if(o<.05)continue;
  const r=document.createRange();r.selectNodeContents(t);const b=r.getBoundingClientRect();if(b.width<2||b.height<2)continue;
  const clip=cs.backgroundClip==='text'||cs.webkitBackgroundClip==='text';
  out.push({txt:t.nodeValue.trim().slice(0,40),c:(cs.webkitTextFillColor&&!/rgba\\(0, 0, 0, 0\\)/.test(cs.webkitTextFillColor))?cs.webkitTextFillColor:cs.color,
   clip,o,fs:parseFloat(cs.fontSize),fw:+cs.fontWeight||400,x:b.left+scrollX,y:b.top+scrollY,w:b.width,h:b.height})}
 return out}'''
HIDE = '*,*::before,*::after{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}input::placeholder{color:transparent!important}'

def lum(c):
    c = [x / 255 for x in c[:3]]; c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def cr(x, y): x, y = sorted((x, y), reverse=True); return (x + .05) / (y + .05)
def parse(c):
    m = [float(v) for v in re.findall(r'[\d.]+', c or '')]
    if len(m) < 3: return None
    rgb = [v * 255 for v in m[:3]] if c.startswith('color(') else m[:3]
    return rgb, (m[3] if len(m) > 3 else 1)

res = {}; total = 0
with sync_playwright() as pw:
    br = pw.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    login(pg, a)
    for u in a.urls:
        for m in a.modes.split(','):
            pg.goto(u); pg.wait_for_load_state('networkidle'); set_mode(pg, a, m)
            pg.evaluate("document.querySelectorAll('*').forEach(e=>{e.style.animation='none';e.style.transition='none'})"); pg.wait_for_timeout(a.wait)
            # fixed / sticky bars would cover other text in a full-page capture: skip their text and hide them
            pg.evaluate("""()=>document.querySelectorAll('body *').forEach(e=>{const p=getComputedStyle(e).position;
              if(p==='fixed'||p==='sticky')e.setAttribute('data-ca-float','')})""")
            nodes = pg.evaluate(COLLECT, a.skip + ',[data-ca-float]')
            pg.add_style_tag(content=HIDE + '[data-ca-float]{visibility:hidden!important}'); pg.wait_for_timeout(150)
            hgt = min(pg.evaluate('document.documentElement.scrollHeight'), 8000)
            img = Image.open(io.BytesIO(pg.screenshot(full_page=True, clip={'x': 0, 'y': 0, 'width': 390, 'height': hgt}))).convert('RGB')
            bad = []
            for n in nodes:
                if n['clip']: continue
                pc = parse(n['c'])
                if not pc: continue
                rgb, al = pc; al *= n['o']
                x0, y0 = int(n['x']), int(n['y'])
                if x0 >= img.width or y0 >= img.height or x0 + n['w'] <= 0: continue
                box = img.crop((max(0, x0), max(0, y0), min(img.width, x0 + int(n['w']) + 1), min(img.height, y0 + int(n['h']) + 1)))
                if box.width < 1 or box.height < 1: continue
                sm = box.resize((min(box.width, 40), min(box.height, 12)))
                px = list(sm.get_flattened_data() if hasattr(sm, 'get_flattened_data') else sm.getdata())
                rats = sorted(cr(lum([rgb[i] * al + q[i] * (1 - al) for i in range(3)]), lum(q)) for q in px)
                worst = rats[len(rats) // 10]
                need = 3.0 if (n['fs'] >= 24 or (n['fs'] >= 18.66 and n['fw'] >= 700)) else 4.5
                if worst < need - .05: bad.append({'text': n['txt'], 'ratio': round(worst, 2), 'need': need, 'color': n['c'], 'y': y0})
            res['%s|%s' % (m, u)] = bad; total += len(bad)
            print('%-5s %-60s failures %d' % (m, u[:60], len(bad)))
            for b in bad[:6]: print('      %.2f < %.1f  %s' % (b['ratio'], b['need'], b['text']))
    br.close()
if a.json: json.dump(res, open(a.json, 'w'), indent=1)
print('TOTAL failures', total)
