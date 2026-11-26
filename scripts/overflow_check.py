#!/usr/bin/env python3
"""Load pages at each --widths (default 360,768,1280; alternating light/dark) and report horizontal overflow, JS errors,
PHP warnings in the page text and HTTP 5xx.   python3 overflow_check.py URL [URL…] [login options]"""
from playwright.sync_api import sync_playwright
from _common import parser, login, set_mode

pa = parser(__doc__); pa.add_argument('--widths', default='360,768,1280'); a = pa.parse_args(); bad = n = 0
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for W in [int(x) for x in a.widths.split(',')]:
     ctx = br.new_context(viewport={'width': W, 'height': 800}, service_workers='block'); pg = ctx.new_page(); errs = []
     pg.on('pageerror', lambda e: errs.append(str(e)[:100]))
     login(pg, a)
     for i, u in enumerate(a.urls):
        m = 'dark' if (i + W) % 2 else 'light'; errs.clear()
        try:
            r = pg.goto(u); pg.wait_for_load_state('networkidle'); set_mode(pg, a, m); pg.wait_for_timeout(300); n += 1
            sw = pg.evaluate('document.documentElement.scrollWidth'); body = pg.inner_text('body')[:30000]
        except Exception as ex:
            print('skip', u, str(ex)[:80]); continue
        php = [w for w in ('Fatal error', 'Warning:', 'Notice:', 'Deprecated:', 'Parse error') if w in body]
        if sw > W + 2 or php or errs or (r and r.status >= 500):
            bad += 1; print('PROBLEM', W, u, m, 'scrollWidth', sw, php, 'status', r.status if r else '', errs[:2])
    br.close()
print('checked', n, 'problems', bad)
