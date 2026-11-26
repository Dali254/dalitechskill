# Responsive layout

Mobile first: write the phone layout as the default CSS, then **add** columns and chrome at wider sizes with
`min-width` media queries. Test at **320, 360, 390, 768, 1024, 1280, 1600** px (`scripts/overflow_check.py`
does all of these by default).

## Breakpoints

| Name | Min width | What changes |
|---|---|---|
| base | 0 | 1 column, sticky top bar, floating tab bar, menu = off-canvas drawer, sheets slide up |
| sm | 480 | small grids get 2 columns (tiles, presets) |
| md | 768 | stats 3-across, wallets 2-across, tiles 4-across, KPI row 4-across, tables become real tables, sheets become centred dialogs, auth pages get the brand panel |
| lg | 1024 | **side rail** appears (fixed floating sidebar), tab bar + burger hidden, main/side two-column layouts (`.sr-lg-main-side`), wallets 3-across, toasts move bottom-right |
| xl | 1280 | wider rail, balance card beside the stats (`.sr-dash-top`), 4-column grids |

Use the same numbers everywhere (CSS, JS `matchMedia('(min-width:1024px)')`, image `sizes`).

## The app shell

```
phone / tablet                       desktop ≥1024
┌ topbar: ☰ logo title 🔔 ☾ AM ┐      ┌ rail ─────┐ ┌ topbar: title 🔔 ☾ AM ┐
│ page content (1 col)          │      │ NOVAPAL   │ │ page content           │
│                               │      │ Home      │ │ (max 1180px, 2–4 cols) │
└ tabbar: Home Earn (W) Act Menu┘      │ …         │ │                        │
  drawer (☰ / Menu) = same rail        │ Sign out  │ │                        │
                                       └───────────┘ └────────────────────────┘
```

- **One navigation source** (`NAV` list) renders both the rail and the tab bar, so they can never disagree.
  The tab bar shows max 5 items; the raised centre one is the main money action (Withdraw).
- `body.sr-app{padding-left: calc(var(--rail-w) + 1.2rem)}` at lg; below lg the rail is `transform:translateX(-110%)`
  and slides in with `.sr-drawer-open` on `<body>`, plus a scrim. Close on scrim click, Esc, link click,
  and when the screen grows past 1024 px. Move focus into the drawer when it opens and back to the burger when it closes.
- Reserve space so content never hides under fixed bars: `padding-bottom: calc(6.5rem + env(safe-area-inset-bottom))`
  on phones, `scroll-padding-top` for the sticky top bar.
- `viewport-fit=cover` + `env(safe-area-inset-*)` for notched phones.

## Layout rules that prevent 90% of bugs

1. Every grid column is `minmax(0,1fr)`, never plain `1fr` (plain `1fr` = `minmax(auto,1fr)` lets long content,
   inputs and nowrap text push the page wider than the screen). Give grid/flex children `min-width:0`.
2. Long strings: `overflow-wrap:anywhere` for user text; `text-overflow:ellipsis` + `white-space:nowrap` +
   `min-width:0` for one-line rows; URLs in a `.sr-copy` box.
3. No fixed widths on content; use `max-width` and `min()` (`width:min(560px, calc(100% - 1.2rem))`).
4. Auto-fitting card grids: `grid-template-columns: repeat(auto-fill, minmax(min(100%, 15rem), 1fr))`.
5. **Container queries** for components that live in columns of different widths (colour cards):
   `.pz-c{container-type:inline-size}` and `@container (max-width:15rem){ … smaller amount, hide corner button … }`.
   The card adapts to its own width, not the screen.
6. Fluid type for headings: `font-size: clamp(1.35rem, 1.1rem + 1.2vw, 1.9rem)`. Body text stays 15–16px.
7. Inputs are **16px** on phones (smaller makes iOS zoom in).
8. Tap targets ≥ 44×44px; spacing between tappable items ≥ 8px.
9. Tables: on phones either stack rows into cards (`.sr-table--stack` + `data-label` on each `<td>`, one cell marked
   `.sr-td-main` as the row heading) or wrap in `.sr-scroll-x` for wide numeric tables.
10. Horizontal chip/tab rows scroll sideways (`overflow-x:auto`, hidden scrollbar) instead of wrapping into 3 lines.
11. Modals: bottom **sheet** on phones (thumb reach), centred **dialog** ≥768.
12. Images: `aspect-ratio` + `object-fit:cover`, `srcset`/`sizes` matching the breakpoints, `loading="lazy"`.
13. Hover effects only where hover exists: `@media (hover:none){ … no lift … }`.
14. Respect `prefers-reduced-motion` and add a `@media print` that hides the chrome.

## Page layouts per breakpoint (examples)

| Page | Phone | Tablet ≥768 | Desktop ≥1024/1280 |
|---|---|---|---|
| Dashboard | stacked cards | stats 3-across, wallets 2, tiles 4 | rail; xl: balance beside stats; activity + partner link side by side |
| Withdraw | balance → form → info | same, wider presets | form (main) + help + recent withdrawals (side) |
| Activity | KPI 2×2, chips, stacked rows | KPI 4-across, real table | rail + full table |
| Tasks | 1 card per row | auto-fill grid | grid (main) + progress/rules (side) |
| Auth | single form, centred | brand panel left, form right | same, larger panel |
| Admin | KPIs 2×2, table as cards, sticky save bar above tab bar | real table | table (main) + payouts (side), save bar at bottom |

## Checking

```
python3 scripts/overflow_check.py URL… --widths 320,360,768,1024,1280,1600
python3 scripts/shots.py URL… --widths 390,768,1280 --modes light,dark --montage
```
Look at the montage: nothing cut off, nothing overlapping, no huge empty areas, balance visible on the first
phone screen, rail and tab bar never both visible.
