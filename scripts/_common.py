"""Shared options for the browser scripts (Playwright + Chromium).

  --login URL --field name=value [--field …] --submit "button[type=submit]"   sign in first
  --dark-js "JS"      how to switch dark mode on (default: add class "dark" to <html> + common storage keys)
  --wait MS           extra wait after load (default 800)
  --block-sw          block service workers (always on for speed tests)
"""
import argparse

DARK_JS = """m=>{const d=m==='dark';document.documentElement.classList.toggle('dark',d);
 try{localStorage.setItem('sr-theme-v1',JSON.stringify({mode:m}));localStorage.setItem('theme',m)}catch(e){}}"""

def parser(desc):
    p = argparse.ArgumentParser(description=desc)
    p.add_argument('urls', nargs='+')
    p.add_argument('--login'); p.add_argument('--field', action='append', default=[])
    p.add_argument('--submit', default='form button[type=submit]')
    p.add_argument('--dark-js', default=DARK_JS)
    p.add_argument('--wait', type=int, default=800)
    return p

def login(pg, a):
    if not a.login: return
    pg.goto(a.login)
    for f in a.field:
        k, v = f.split('=', 1); pg.fill('[name="%s"]' % k, v)
    pg.click(a.submit); pg.wait_for_load_state('networkidle')

def set_mode(pg, a, mode):
    pg.evaluate(a.dark_js, mode)
