#!/usr/bin/env python3
"""Profiz 3 colour patterns (balance, today, withdrawn, lifetime) + the icon-behind-card style of each.

  python3 patterns.py --list          names and keys
  python3 patterns.py --json          data (used by the starter template)
  python3 patterns.py --css           CSS custom-property blocks:  [data-pattern="<key>"]{--c1a:…}

kind:  solid  = coloured gradient cards, white text
       pastel = light cards with dark text (turn into tinted dark glass in dark mode)
       glass  = dark glass cards with a neon edge (opens in dark)
ghost: outline | 3d | frost | gold | tint | neon
"""
import json, sys

PATTERNS = {
    'profiz': dict(name='Profiz 3', kind='solid', ghost='outline', mode='light',
                   cards=[['#1a8259', '#066947'], ['#3466ec', '#1e4fd6'], ['#e3264f', '#b3123c'], ['#8a3cf0', '#5b21b6']]),
    'tropic': dict(name='Tropical Pop', kind='solid', ghost='3d', mode='light',
                   cards=[['#0b8378', '#0a6b62'], ['#cc4a08', '#a83c07'], ['#c81e6c', '#9d1754'], ['#4f46e5', '#3730a3']]),
    'jewel':  dict(name='Royal Jewel', kind='solid', ghost='gold', mode='light', edge='#f5c45166',
                   cards=[['#047857', '#053d2e'], ['#1d4ed8', '#172a6b'], ['#be123c', '#6f0d26'], ['#7e22ce', '#4a136f']]),
    'pastel': dict(name='Pastel Cream', kind='pastel', ghost='tint', mode='light', text='#16121f',
                   cards=[['#d1fae5', '#a7f3d0', '#047857'], ['#dbeafe', '#bfdbfe', '#1d4ed8'],
                          ['#ffe4e6', '#fecdd3', '#be123c'], ['#ede9fe', '#ddd6fe', '#6d28d9']]),
    'sunset': dict(name='Sunset Ramp', kind='solid', ghost='frost', mode='light',
                   cards=[['#c2410c', '#9a3412'], ['#e11d48', '#9f1239'], ['#be185d', '#831843'], ['#86198f', '#581c87']]),
    'neon':   dict(name='Neon Ocean', kind='glass', ghost='neon', mode='dark',
                   cards=[['#22d3ee', '#0e7490'], ['#a78bfa', '#6d28d9'], ['#fbbf24', '#b45309'], ['#4ade80', '#15803d']]),
}

def css():
    out = []
    for k, p in PATTERNS.items():
        v = []
        for i, c in enumerate(p['cards'], 1):
            v.append('--c%da:%s;--c%db:%s' % (i, c[0], i, c[1]))
            if len(c) > 2: v.append('--c%dd:%s' % (i, c[2]))
        if p.get('edge'): v.append('--edge:%s' % p['edge'])
        if p.get('text'): v.append('--card-text:%s' % p['text'])
        out.append('[data-pattern="%s"]{%s}' % (k, ';'.join(v)))
    return '\n'.join(out)

if __name__ == '__main__':
    a = sys.argv[1] if len(sys.argv) > 1 else '--list'
    if a == '--json': print(json.dumps(PATTERNS, indent=1))
    elif a == '--css': print(css())
    else:
        for k, p in PATTERNS.items(): print('%-7s %-14s %-6s ghost=%-7s opens=%s' % (k, p['name'], p['kind'], p['ghost'], p['mode']))
