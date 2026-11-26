#!/usr/bin/env python3
"""HD screenshots in light and/or dark, at one or more screen widths, with scroll steps and a montage.

  python3 shots.py URL [URL…] --modes light,dark --widths 390,768,1280 --out shots --montage
  python3 shots.py URL --full            # full-page capture instead of the first screen

Widths → (width, height, scale): phone 390×844 @3, tablet 768×1024 @2, desktop ≥1024 → W×800 @2.
Files: OUT/<n>_<width>_<mode>_<step>.png ; montage: OUT/montage.png (one row per URL+mode, widths side by side,
scaled to the same height, labelled).
"""
import os
from playwright.sync_api import sync_playwright
from _common import parser, login, set_mode

p = parser(__doc__)
p.add_argument('--modes', default='light,dark'); p.add_argument('--widths', default='390')
p.add_argument('--scroll', type=int, default=0); p.add_argument('--full', action='store_true')
p.add_argument('--out', default='shots'); p.add_argument('--montage', action='store_true')
p.add_argument('--labels', default='', help='comma list of names for the URLs (montage)')
a = p.parse_args(); os.makedirs(a.out, exist_ok=True)

def dims(w):
    w = int(w)
    if w < 600: return w, 844, 3
    if w < 1024: return w, 1024, 2
    return w, 800, 2

made = {}   # (url index, mode) -> [(width, file)]
errs = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for w in a.widths.split(','):
        W, H, S = dims(w)
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=S, service_workers='block')
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        login(pg, a)
        for i, u in enumerate(a.urls, 1):
            for m in a.modes.split(','):
                pg.goto(u); pg.wait_for_load_state('networkidle'); set_mode(pg, a, m); pg.wait_for_timeout(a.wait)
                for s in range(a.scroll + 1):
                    if s: pg.evaluate('window.scrollBy(0,%d)' % int(H * .85)); pg.wait_for_timeout(450)
                    f = os.path.join(a.out, '%d_%d_%s_%d.png' % (i, W, m, s)); pg.screenshot(path=f, full_page=a.full)
                    if s == 0: made.setdefault((i, m), []).append((W, f))
                    print(f)
        ctx.close()
    br.close()
if errs: print('JS errors:', sorted(set(errs))[:5])

if a.montage and made:
    from PIL import Image, ImageDraw
    labels = a.labels.split(',') if a.labels else []
    rows = []
    for (i, m), items in sorted(made.items()):
        ims = [Image.open(f) for _, f in items]; th = 900
        ims = [im.resize((int(im.width * th / im.height), th), Image.LANCZOS) for im in ims]
        rw = sum(im.width for im in ims) + 30 * (len(ims) - 1)
        name = labels[i - 1] if i - 1 < len(labels) else 'page %d' % i
        rw = max(rw, 900)
        row = Image.new('RGB', (rw, th + 120), 'white'); d = ImageDraw.Draw(row); x = 0
        d.text((6, 8), '%s · %s' % (name, m), fill='#16121f', font_size=40)
        for (W, _), im in zip(items, ims):
            row.paste(im, (x, 120)); d.text((x + 6, 70), '%dpx' % W, fill='#5d5a6b', font_size=30); x += im.width + 30
        rows.append(row)
    mw = max(r.width for r in rows); c = Image.new('RGB', (mw, sum(r.height + 30 for r in rows)), 'white'); y = 0
    for r in rows: c.paste(r, (0, y)); y += r.height + 30
    out = os.path.join(a.out, 'montage.png'); c.save(out); print(out)
