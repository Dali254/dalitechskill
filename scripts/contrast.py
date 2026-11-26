#!/usr/bin/env python3
"""Contrast ratio of two colours (WCAG 2.x).  python3 contrast.py '#ffffff' '#cc4a08' ['#…' …]
With 3+ colours the first is the text colour and each other one is a background."""
import sys
def lum(h):
    h = h.lstrip('#'); h = ''.join(c * 2 for c in h) if len(h) == 3 else h[:6]
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def ratio(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x + .05) / (y + .05)
if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    fg = sys.argv[1]
    for bg in sys.argv[2:]:
        r = ratio(fg, bg)
        print('%s on %s: %.2f  %s' % (fg, bg, r, 'AA' if r >= 4.5 else ('AA large only' if r >= 3 else 'FAIL')))
