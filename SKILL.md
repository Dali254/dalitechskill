---
name: sunrise-dashboard-ui
description: Build any website, dashboard, member area or admin panel in the Sunrise UI style (floating sidebar, gradient tiles, Phosphor icons, Sora/Inter, mobile tab bar) with admin-changeable theme colours and dark mode.
---

# Sunrise UI

A complete system for building **responsive** member websites — earning apps, wallets, task sites, sign-up flows,
profile pages and admin panels — that look premium on a 320 px phone and a 1600 px desktop, switch between
dashboard styles and colour patterns, work perfectly in **light and dark mode**, and **load fast on 3G**.
Distilled from the TrendGain / NovaPal "Sunrise" project.

Use it whenever you build or restyle any page of such a site: dashboard, sign in / register, withdraw,
activity, tasks, profile, notifications, team, admin overview / tables / settings, landing page — or when asked
for responsiveness, a new style or colour pattern, faster pages, or a link-preview picture.

## Golden rules

1. **Keep the structure.** One app shell on every page (side rail ≥1024 / drawer + tab bar below), one `NAV` list,
   one stylesheet of tokens and components. Reuse class names from `references/components.md`. If a project
   exists, read its structure first and stay consistent.
2. **Mobile first, then wider.** Default CSS is the phone; add columns with `min-width` queries at 480/768/1024/1280.
   Grid columns are always `minmax(0,1fr)`. No horizontal scrolling at 320–1600 px. (`references/responsive.md`)
3. **Light AND dark for everything**, WCAG AA contrast (4.5:1; 3:1 for large text), checked on real pixels.
4. **Show as you create.** After each visible change: screenshots at 390 / 768 / 1280 px, light + dark, look at
   them yourself, fix, then show the user. Offer options as one labelled montage and let the user choose.
5. **Honest UI.** No fake stats, counters, referrals or reviews. Label AI / demo content.
6. **Fast on slow internet.** Few files, subset icons, phone-sized images, swap fonts, long caching. Measure.
7. **Admin controls, not code edits.** Settings pages with clear labels and a visible (sticky) **Save**.
8. **Accessible by default.** Labels, focus rings, 44 px targets, `aria-current` / `aria-pressed`, Esc closes overlays.

## Workflow

1. **Understand** — pages, data, existing style; study any reference screenshot (order, colours, radius, font, icons).
2. **Shell + page skeleton** — start from `assets/starter/` (copy `sunrise.css`, `sunrise.js`, `sr-boot.js` and the
   closest page). Recipes for every page type: `references/pages.md`.
3. **Compose with components** — `references/components.md`; gallery in `assets/starter/components.html`.
4. **Style** — tokens (`references/design-system.md`), switchable skins (`references/dashboard-styles.md`),
   colour patterns (`references/color-patterns.md`), light/dark rules (`references/light-dark.md`).
5. **Make it responsive** — arrange for tablet and desktop (`references/responsive.md`).
6. **Check** — `scripts/shots.py --widths 390,768,1280 --modes light,dark --montage`,
   `scripts/overflow_check.py` (320–1600 px), `scripts/contrast_audit.py`, console errors (`references/checks.md`).
7. **Speed + sharing** — `references/speed.md`, `references/link-preview.md`.
8. **Ship** — bump the asset version, changelog line, package without `.env` / logs / caches.

## Quick reference

| Need | Go to |
|---|---|
| Breakpoints, app shell, layout rules, per-page arrangements | `references/responsive.md` |
| Every component with markup + behaviour | `references/components.md` |
| Page recipes (dashboard, auth, withdraw, activity, tasks, profile, admin, more) | `references/pages.md` |
| Tokens, typography, icons, navigation, motion, dashboard anatomy | `references/design-system.md` |
| Switchable dashboard styles (skins), file format, previews | `references/dashboard-styles.md` |
| Profiz 3 + 5 colour patterns with exact colours and icon-behind-card styles | `references/color-patterns.md` |
| Light / dark rules and common dark-mode bugs | `references/light-dark.md` |
| Forms and admin details (register rules, save buttons, copy boxes, money rules) | `references/forms-and-admin.md` |
| Fast pages on 3G | `references/speed.md` |
| Favicon + WhatsApp / Facebook preview picture | `references/link-preview.md` |
| Screenshot, contrast and overflow checks; definition of done | `references/checks.md` |

## Starter (open `assets/starter/index.html`; `?p=<pattern>&mode=dark`)

`index` dashboard · `login` · `register` · `withdraw` (confirm sheet) · `transactions` (responsive table) ·
`tasks` (photo grid + filters sheet) · `profile` (forms, switches, accordion) · `admin` (KPIs, table, payouts,
sticky save bar) · `components` (gallery). Shared: `sunrise.css` (tokens → shell → components → breakpoints),
`sunrise.js` (shell from `NAV`, theme, drawer, sheets, toasts, chips, copy), `sr-boot.js` (theme before paint).
Patterns: `profiz tropic jewel pastel sunset neon`.

## Scripts (Python 3 + Playwright: `pip install playwright pillow && playwright install chromium`)

- `shots.py URL… --widths 390,768,1280 --modes light,dark [--full] [--montage --labels a,b]` — HD screenshots + montage.
- `overflow_check.py URL… [--widths 320,360,768,1024,1280,1600]` — overflow, JS errors, PHP warnings, 5xx.
- `contrast_audit.py URL… [--modes light,dark]` — pixel-accurate contrast (gradients, glass, images).
- `slow3g.py URL…` — first paint, load, files, KB on Slow 3G.
- `gen_skin.py SKINS OUT` — build skins · `patterns.py --css|--json|--list` · `contrast.py fg bg…`.
- Sign in first with `--login URL --field name=value … --submit SELECTOR`; custom dark switch with `--dark-js`.

## PHP helpers (`assets/php/`)

`asset-bundle.php` (join CSS/JS: ~21 → 6 files) · `img-fit.php` (phone-sized photos + srcset) ·
`share-head.php` (favicon + Open Graph tags + generated 1200×630 share picture).

## Done means

Screenshots at 390/768/1280 in light and dark shown to the user · overflow 0 problems at 320–1600 px ·
contrast 0 failures in both modes · no console errors · speed measured when assets changed · changelog written.
