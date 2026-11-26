---
name: sunrise-dashboard-ui
description: Build any website, dashboard, member area or admin panel in the Sunrise UI style (floating sidebar, gradient tiles, Phosphor icons, Sora/Inter, mobile tab bar) with admin-changeable theme colours and dark mode.
---

# Sunrise Dashboard UI

A system for building mobile-first member websites (earning apps, wallets, task sites, admin panels) that look
premium, switch between many **dashboard styles**, work perfectly in **light and dark mode**, and **load fast on
slow phones and 3G**. Distilled from the TrendGain / NovaPal "Sunrise" project.

Use this skill whenever you build or restyle: a member dashboard, wallet / balance screens, a register / login
page, a side menu or tab bar, an admin settings page, a "dashboard style" or theme, or when asked to make pages
faster or to add a link-preview picture.

## Golden rules (never break these)

1. **Keep the structure.** Reuse the class anatomy in `references/design-system.md` (`.sr-greet`, `.sr-balance`,
   `.sr-stats > .sr-stat`, `.sr5-wcard`, `.sr-tabbar`, `.sr-tab--cta` …). New styles change *skins*, never markup.
   If a project already exists, read its structure first and stay consistent with it.
2. **Every style has a full light AND dark version.** Test both. Text must pass WCAG AA (4.5:1 normal text,
   3:1 for ≥24px or ≥18.66px bold). White text on colour cards needs dark-enough card colours
   (check with `scripts/contrast.py`).
3. **Show as you create.** After every visible change take HD phone screenshots (390×844 @3x) in light and dark
   (`scripts/shots.py`), look at them yourself, fix what is off, then show the user. Do not wait until the end.
4. **Honest UI.** No fake stats, fake counters, fake referrals or fake reviews. Label AI / demo content as such.
5. **Fast on slow internet.** Few files, small files, phone-sized images, fonts with `font-display:swap`
   (see `references/speed.md`). Measure before and after with `scripts/slow3g.py`.
6. **Admin controls, not code edits.** Anything a site owner may want to change (colours, style, menu order,
   toggles, texts, fees) is a setting with a clear admin page and a visible **Save** button.
7. **Mobile first.** Design at 360–390px wide first. No horizontal scrolling (`scripts/overflow_check.py`).

## Workflow

1. **Understand** — what pages, what data, which existing style. If there is a reference screenshot, study it:
   card order, colours, radius, font, icon style, spacing.
2. **Structure** — build or reuse markup from `assets/starter/index.html` (the canonical dashboard anatomy:
   top bar → greeting card → balance + stat colour cards → wallets → partner link with share buttons →
   recent activity → floating tab bar with a raised centre action).
3. **Style** — use design tokens (`--paper --surface --line --heading --text --muted --brand --brand-2 --r-xl` …).
   For a switchable look, write a *skin* (`references/dashboard-styles.md`) and build it with
   `scripts/gen_skin.py`. For card colour sets use the six ready patterns in `references/color-patterns.md`
   (`scripts/patterns.py` prints them as CSS or JSON).
4. **Check** — screenshots light + dark, contrast audit, overflow check, JS console errors. Fix, re-shoot.
5. **Speed** — bundle CSS/JS, subset icon fonts, resize images, cache headers. Re-measure.
6. **Ship** — bump the asset version (cache-busting), write a short changelog entry, package without secrets
   (never ship `.env`, logs, caches).

## Quick reference

| Need | Go to |
|---|---|
| Layout anatomy, tokens, typography, tab bar, side menu | `references/design-system.md` |
| Many switchable dashboard styles, skin file format, previews | `references/dashboard-styles.md` |
| Profiz 3 + 5 colour patterns (exact hex values, icon-behind-card styles) | `references/color-patterns.md` |
| Light / dark rules and common dark-mode bugs | `references/light-dark.md` |
| Make pages load fast on 3G | `references/speed.md` |
| Favicon + WhatsApp / Facebook link preview picture | `references/link-preview.md` |
| Screenshot, contrast and overflow checks | `references/checks.md` |
| Register / login / admin form patterns | `references/forms-and-admin.md` |

## Scripts

All scripts are plain Python 3 (Playwright for browser checks: `pip install playwright pillow && playwright install chromium`).

- `scripts/gen_skin.py SKINS_DIR OUT_DIR` — build skins written in the `@@T/@@TL/@@TD/@@B/@@C/@@CL/@@CD` format.
- `scripts/patterns.py [--css|--json|--list]` — the six Profiz 3 colour patterns.
- `scripts/contrast.py '#fff' '#0b8378'` — contrast ratio of two colours (and AA pass/fail).
- `scripts/shots.py URL [--dark] [--scroll N] [--out DIR]` — HD phone screenshots, light/dark, scroll steps, montage.
- `scripts/contrast_audit.py URL [URL…] [--modes light,dark]` — pixel-accurate contrast audit of real pages.
- `scripts/overflow_check.py URL [URL…]` — horizontal overflow, JS errors, PHP warnings, 5xx at 360px.
- `scripts/slow3g.py URL [URL…]` — first paint, load time, files and KB under slow-3G throttling.

Browser scripts accept `--login URL --field name=value … --submit SELECTOR` to sign in first, and
`--dark-js` to customise how dark mode is switched on (default: adds the `dark` class to `<html>`).

## PHP helpers (drop-in)

- `assets/php/asset-bundle.php` — joins back-to-back local `<link rel=stylesheet>` / `<script src>` tags into one
  cached file each (21 → 6 files per page in practice), light CSS minify, auto-rebuild when sources change.
- `assets/php/img-fit.php` — `img_fit($url, 480)` / `img_srcset($url)` for phone-sized photos.
- `assets/php/share-head.php` — favicon + Open Graph / Twitter tags + a generated 1200×630 share picture.

## Done means

Light and dark screenshots shown to the user, contrast audit 0 failures, overflow check 0 problems,
no console errors, speed measured, and a changelog line written.
