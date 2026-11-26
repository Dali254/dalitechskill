# Design system

## 1. Page anatomy (member dashboard, mobile first)

```
┌ .sr-topbar ───────────────────────────────┐  brand logo + name · bell · currency · moon · avatar
│ .ds-burger (animated, opens .sr-drawer)    │
├ .sr-greet ────────────────────────────────┤  white card: avatar + "Good afternoon, <b>name</b>"
├ .sr-notice (dismissable, optional)        ┤  e.g. "No new team members today"  ✕
├ .sr-balance ──────────────────────────────┤  AVAILABLE BALANCE · KES 1,120.00 · corner button ↗
├ .sr-stats > .sr-stat × 3 ─────────────────┤  TODAY · WITHDRAWN · LIFETIME (label, value, hint •)
├ section "My wallets" ─────────────────────┤  .sr5-wcard × n (bonus / royalty wallets)
├ "Ways to earn" (.sr-tile grid)            ┤
├ .sr5-partner (partner link + .sr5-share)  ┤  copy link + WhatsApp / Facebook / Telegram / X / SMS
├ Recent activity (.sr5-src = where money   ┤  came from: "Level 1 · amina.k · Hotel unlock")
└ .sr-tabbar ── Home · Earn · (Withdraw) · Activity · Menu ┘   centre .sr-tab--cta is raised
```

Order matters to members: **money first** (balance, wallets), then **how to earn more**, then **sharing**,
then **history**. Do not put Invite / Withdraw buttons at the very top; Withdraw lives in the raised tab.

### Colour card anatomy (`.sr-balance`, `.sr-stat`, `.sr5-wcard`)

- Label: UPPERCASE, letter-spacing .14–.16em, 0.78rem, weight 700, white (or dark on pastel).
- Value: weight 800, ~1.75rem; currency prefix `<small>KES</small>` smaller.
- Hint: bottom-left, a small dot `•` + short text ("Start a task", "Paid out", "All earnings").
- Corner button: top-right 2.4rem square, radius .65rem, 1.5px white-45% border, white-12% fill, icon inside.
- Icon behind the card: bottom-right, ~5–6rem, decorative only (`pointer-events:none`, `aria-hidden`).
- Full width, stacked, gap .85rem, radius 1.15rem, soft coloured shadow.

## 2. Tokens

Always style with tokens; skins only change token values + a few rules.

| Token | Use | Light example | Dark example |
|---|---|---|---|
| `--paper` | page background | `#f6f5fb` | `#0f0d16` |
| `--surface` / `--surface-2` | cards / raised areas | `#fff` / `#fbfaff` | `#1a1724` / `#211d2e` |
| `--sunken` | inputs, wells | `#f1eff7` | `#14121c` |
| `--line` / `--line-strong` | borders | `#ebe7f2` / `#ddd7e8` | `#2c2740` / `#3a3452` |
| `--heading` `--text` `--muted` `--faint` | text levels | `#15131c #3d3a48 #5d5a6b #8a8699` | `#f5f3fa #d6d2e2 #aaa4bd #7f7994` |
| `--brand` `--brand-2` `--brand-3` | brand colours (admin-changeable) | `#e0098f` … | same or lighter |
| `--brand-fg` | brand-coloured **text** (darkened in light, lightened in dark) | mix 80% brand + black | mix 55% brand + white |
| `--r-xs … --r-xl`, `--r-pill` | radius scale (`--radius-scale` multiplies) | .375 … 1.375rem | |
| `--sh-sm` `--sh-hover` `--sh-float` `--sh-brand` | shadows | | |
| `--font-display` / `--font-sans` | headings / body | Sora / Inter (Profiz: Poppins) | |
| `--ease` | motion | `cubic-bezier(.22,1,.36,1)` | |

Never use `--brand` directly for small text on white — use `--brand-fg` (contrast).

## 3. Typography

- Display: **Sora** (Sunrise) or **Poppins** (Profiz family), weights 600–800, letter-spacing −.01em.
- Body: **Inter** 400/500/600/700. Keep to ≤4 font files; `font-display:swap`; self-host woff2.
- Numbers: `font-variant-numeric: tabular-nums` in tables and balances.

## 4. Icons

- **Phosphor** (regular + duotone) or **Fluent** icons via an inline SVG sprite / JS map. Subset them to the
  icons actually used (see speed.md).
- Optional **glossy 3D icons** (webp, transparent, ~256px) for hero spots: wallet, sparkle/star, coins, trophy,
  gift, team, chart, shield. Generate with an image model using `background: transparent`, keep a consistent
  light direction (top-left), and store as `assets/ds/i3d/<name>.webp`.
- Icon buttons: min 40×40px tap area, visible focus ring.

## 5. Navigation

- **Tab bar** (`.sr-tabbar`): floating, white/surface, radius xl, 5 tabs, active tab gets a soft brand pill,
  centre `.sr-tab--cta` raised circle with brand gradient and a 5px ring in `--surface` colour.
- **Side menu / drawer** (`.sr-drawer`): order is admin-controlled (setting `nav_order`); "Ways to earn" right
  after Home. Hidden tasks are removed from the menu, not just greyed.
- **Burger** (`.ds-burger`): three bars, animated into ✕, clearly visible on every style, ≥44px.

## 6. Spacing & layout

- Mobile padding 1rem; card padding 1.1–1.2rem; section gap 1.25–1.5rem; list gap .85rem.
- Max content width ~1100px on desktop with a floating left rail (`--rail-w:15rem`).
- Avoid tall empty hero areas; compact first screen (balance visible without scrolling).

## 7. Motion

- Reveal on scroll (`[data-sr-reveal]` → `.is-in`) 300–450ms, translateY 8px + fade.
- One-time sheen on hero cards at most; respect `prefers-reduced-motion` (disable all decorative motion).
