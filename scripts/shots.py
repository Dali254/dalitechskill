#!/usr/bin/env python3
"""HD phone screenshots (390×844 @3x) in light and/or dark, with scroll steps and an optional montage.

  python3 shots.py https://site/dashboard?ds=profiz --modes light,dark --scroll 2 --out shots --montage
Files: OUT/<n>_<mode>_<step>.png  and  OUT/montage.png (all URLs × modes, first step).
"""
import os, re
from playwright.sync_api import sync_playwright
from _common import parser, login, set_mode

p = parser(__doc__)
p.add_argument('--modes', default='light,dark'); p.add_argument('--scroll', type=int, default=0)
p.add_argument('--out', default='shots'); p.add_argument('--montage', action='store_true')
p.add_argument('--width', type=int, default=390); p.add_argument('--height', type=int, default=844)
p.add_argument('--scale', type=float, default=3)
a = p.parse_args(); os.makedirs(a.out, exist_ok=True); made = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={'width': a.width, 'height': a.height}, device_scale_factor=a.scale, service_workers='block')
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    login(pg, a)
    for i, u in enumerate(a.urls, 1):
        for m in a.modes.split(','):
            pg.goto(u); pg.wait_for_load_state('networkidle'); set_mode(pg, a, m); pg.wait_for_timeout(a.wait)
            for s in range(a.scroll + 1):
                if s: pg.evaluate('window.scrollBy(0,%d)' % int(a.height * .9)); pg.wait_for_timeout(500)
                f = os.path.join(a.out, '%d_%s_%d.png' % (i, m, s)); pg.screenshot(path=f)
                if s == 0: made.append((f, '%d %s' % (i, m)))
                print(f)
    br.close()
if errs: print('JS errors:', errs[:5])
if a.montage and made:
    from PIL import Image, ImageDraw
    ims = [Image.open(f) for f, _ in made]; w, h = ims[0].size; pad = 24
    c = Image.new('RGB', (len(ims) * (w + pad) - pad, h + 90), 'white'); d = ImageDraw.Draw(c)
    for k, (im, (_, lab)) in enumerate(zip(ims, made)):
        c.paste(im, (k * (w + pad), 90)); d.text((k * (w + pad) + 12, 20), lab, fill='#16121f', font_size=48)
    c.save(os.path.join(a.out, 'montage.png')); print(os.path.join(a.out, 'montage.png'))
