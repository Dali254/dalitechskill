# Profiz 3 colour patterns

Card order: **balance, today, withdrawn, lifetime**. Wallet cards cycle the same four colours.
Every gradient is `linear-gradient(160deg, A, B)`. All white-text pairs below pass AA (≥4.5:1 at A).
`scripts/patterns.py --css` prints ready CSS for the starter template; `--json` prints the data.

## 0. Profiz 3 (original)
Brand pink `#e0098f` (text), gradient CTA `#e0098f → #c8087f`. Font Poppins.

| Card | A | B |
|---|---|---|
| Balance (green) | `#1a8259` | `#066947` |
| Today (blue) | `#3466ec` | `#1e4fd6` |
| Withdrawn (red) | `#e3264f` | `#b3123c` |
| Lifetime (purple) | `#8a3cf0` | `#5b21b6` |

Icon behind card: white outline icon (wallet, bolt, arrow-out, trophy), opacity .16.

## 1. Tropical Pop — glossy 3D icons
| `#0b8378 → #0a6b62` | `#cc4a08 → #a83c07` | `#c81e6c → #9d1754` | `#4f46e5 → #3730a3` |
Icon behind: full-colour 3D webp (wallet, sparkle, coins, trophy), 5.6rem, rotate(−12deg), drop-shadow, peeking
from the bottom-right corner (`inset:auto -.7rem -1.5rem auto`).

## 2. Royal Jewel — gold
| `#047857 → #053d2e` | `#1d4ed8 → #172a6b` | `#be123c → #6f0d26` | `#7e22ce → #4a136f` |
Thin gold edge `box-shadow: 0 0 0 1px #f5c45166`. Icon behind: gold `#f5c451` outline, opacity .42.

## 3. Pastel Cream — dark text
Light mode cards (text `#16121f`):
| `#d1fae5 → #a7f3d0` (deep `#047857`) | `#dbeafe → #bfdbfe` (`#1d4ed8`) | `#ffe4e6 → #fecdd3` (`#be123c`) | `#ede9fe → #ddd6fe` (`#6d28d9`) |
Icon behind: outline tinted with the card's deep colour, opacity .22. Corner button: `#ffffff99` fill, dark arrow.
**Dark mode:** pastels become tinted dark glass:
`linear-gradient(160deg, color-mix(in srgb, DEEP 46%, #141120), color-mix(in srgb, DEEP 24%, #141120))`,
1px edge in the pastel colour, text `#f6f4fb`, icon in the pastel colour at .32.

## 4. Sunset Ramp — frosted 3D
| `#c2410c → #9a3412` | `#e11d48 → #9f1239` | `#be185d → #831843` | `#86198f → #581c87` |
Icon behind: the 3D webp turned white and frosted —
`filter: grayscale(1) brightness(2.2) blur(.5px); mix-blend-mode: screen; opacity:.38`, 7.4rem.

## 5. Neon Ocean — glowing edges (opens in dark)
Card background: `radial-gradient(120% 100% at 100% 0%, NEON33, transparent 55%), linear-gradient(160deg, #111a33, #0a1022)`
Edge: `box-shadow: 0 0 0 1.5px NEON99, 0 16px 34px -18px NEON`.
| NEON: `#22d3ee` | `#a78bfa` | `#fbbf24` | `#4ade80` |
Amounts are coloured in the card's neon; labels `#e8ecff`. Icon behind: neon outline with
`filter: drop-shadow(0 0 6px NEON)`, opacity .7.

## Icon-behind-card CSS (outline type)

```css
.sr-stat::after{content:"";position:absolute;right:-.3rem;bottom:-.5rem;width:5.2rem;height:5.2rem;
  background:#fff;opacity:.16;pointer-events:none;
  -webkit-mask:var(--ghost) center/contain no-repeat;mask:var(--ghost) center/contain no-repeat}
.sr-stat:nth-child(1){--ghost:url(ghost-bolt.svg)}   /* etc. */
```
The card needs `position:relative; overflow:hidden`, and its text `position:relative; z-index:1`.

## Shared across all patterns
Brand pink tab CTA + greeting name, white greeting card, Poppins, radius 1.15rem, same spacing.
Light page tokens: paper `#f6f5fb`, surface `#fff`; dark: paper `#0f0d16`, surface `#1a1724`.
