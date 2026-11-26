#!/usr/bin/env python3
"""Measure pages on Chrome "Slow 3G" (400 ms latency, 400 kbps), cache and service worker off.
  python3 slow3g.py URL [URL…] [login options] [--latency 400 --kbps 400]
Prints first contentful paint, load event, number of files and transferred KB per page."""
from playwright.sync_api import sync_playwright
from _common import parser, login

p = parser(__doc__); p.add_argument('--latency', type=int, default=400); p.add_argument('--kbps', type=int, default=400)
a = p.parse_args()
with sync_playwright() as pw:
    br = pw.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    login(pg, a)
    cdp = ctx.new_cdp_session(pg); cdp.send('Network.enable'); cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
    bps = a.kbps * 1024 / 8
    cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': a.latency, 'downloadThroughput': bps, 'uploadThroughput': bps})
    print('%-50s %8s %8s %6s %8s' % ('page', 'FCP s', 'load s', 'files', 'KB'))
    for u in a.urls:
        pg.goto(u, wait_until='load', timeout=240000)
        t = pg.evaluate("""()=>{const n=performance.getEntriesByType('navigation')[0],f=performance.getEntriesByName('first-contentful-paint')[0],
          r=performance.getEntriesByType('resource');return {fcp:f?f.startTime:0,load:n.loadEventEnd,files:r.length+1,
          kb:(r.reduce((a,x)=>a+(x.transferSize||0),0)+(n.transferSize||0))/1024}}""")
        print('%-50s %8.1f %8.1f %6d %8.0f' % (u[-50:], t['fcp'] / 1000, t['load'] / 1000, t['files'], t['kb']))
    br.close()
