# Components

All live in `assets/starter/sunrise.css` and are shown together in `assets/starter/components.html`.
Every component uses tokens only, so it works in light, dark and every colour pattern.

| Component | Markup | Notes |
|---|---|---|
| Card | `<section class="sr-card">` · `.sr-card--flush` for edge-to-edge lists/tables · `.sr-card__head` | radius xl, 1px line, soft shadow |
| Section heading | `.sr-sec` > `.sr-eyebrow` + `h2` + `.sr-pill-link` | eyebrow UPPERCASE in `--brand-fg` |
| Page heading | `.sr-pagehead` > `h1` + `p` + actions | wraps on phones |
| Colour card | `.pz-c` > `.pz-label` `.pz-value` `.pz-hint` `.pz-btn` | colours from the pattern; inside `.sr-cycle` they rotate 1→4 |
| Button | `.sr-btn` + `--soft` `--ghost` `--danger` `--block` `--sm` | min-height 44px; `aria-busy="true"` shows a spinner; `disabled` = readable grey |
| Field | `.sr-field` > `label.sr-label` + `.sr-input` + `.sr-help` / `.sr-error` | `.is-invalid` + `aria-invalid` + `aria-describedby` |
| Input group | `.sr-inputgroup` > `.sr-inputgroup__addon` + `.sr-input` | currency, country code, search icon, show-password button |
| Select / textarea | `.sr-select` `.sr-textarea` | 16px text |
| Checkbox | `label.sr-check > input[type=checkbox]` | `accent-color` brand |
| Switch | `label.sr-switch > input + .sr-switch__track` | real checkbox underneath (keyboard + screen reader) |
| Segmented control | `.sr-seg > button[aria-pressed]` | period pickers |
| Chips | `.sr-chips > .sr-chip[aria-pressed]` | filters; scroll sideways |
| Amount presets | `.sr-presets[data-target=inputId] > button[data-amount]` | fills the amount input |
| Badge | `.sr-badge` + `--ok` `--warn` `--bad` `--info` `--brand` | status words, never colour alone |
| Alert | `.sr-alert` + `--ok` `--warn` `--bad` | icon + bold title + short text |
| List row | `ul.sr-list > li.sr-row` > icon + `.sr-row__main` (b + `.sr-row__sub`) + `.sr-amt` | `.sr-amt--in` green for money in |
| Table | `table.sr-table.sr-table--stack` + `td[data-label]` + `td.sr-td-main` | real table ≥768, cards below |
| Tabs | `.sr-tabs > [role=tab][aria-selected]` | underline style |
| Progress | `.sr-progress > span[style=width:x%]` with `role=progressbar` | |
| Steps | `ol.sr-steps > li.is-done / .is-now` | multi-step flows (withdraw, sign-up) |
| Copy box | `.sr-copy > code#id + button[data-copy][data-copy-from=#id]` | webhooks, referral links |
| Sheet / dialog | `.sr-sheet#id[role=dialog][aria-modal] > .sr-sheet__panel` · open: `[data-sheet-open=id]` · close: `[data-sheet-close]` | sheet on phones, dialog ≥768; Esc + backdrop close; focus returns |
| Toast | `SR.toast('Saved')` or `[data-toast="Saved"]` | `aria-live="polite"`; above the tab bar |
| Accordion | `.sr-acc > details > summary + div` | FAQ, help |
| Empty state | `.sr-empty` > 3D image + b + text + action | always offer the next step |
| Skeleton | `.sr-skel` | for loading lists; avoid spinners for whole pages |
| KPI | `.sr-kpis > .sr-kpi` > span + b + small | admin and activity summaries |
| Setting row | `.sr-setting` > text + control | admin/profile settings |
| Save bar | `.sr-savebar` (sticky) | always-visible Save on long admin forms |
| Profile header | `.sr-profilehead` | avatar + name + verified badge |
| Task card | `.sr-task` > `.sr-task__img` + `.sr-task__body` | photo with `srcset`, status badge on the image |

## Behaviour (sunrise.js)

- `data-mode-toggle` light/dark · `data-pattern-select` colour pattern · both saved to `localStorage`.
- `data-drawer-toggle` / `data-drawer-close` side menu on phones.
- `data-pass-toggle` show/hide password · `data-copy` copy to clipboard · `data-toast` message.
- Groups of `aria-pressed` buttons (`.sr-seg`, `.sr-chips`, `.sr-presets`) act as single-choice.
- Public API: `SR.toast(msg)`, `SR.sheet(id, open)`, `SR.drawer(open)`, `SR.setPattern(key)`.

## Accessibility checklist for every component
Visible focus ring · labels for every input (not placeholder only) · state not shown by colour alone ·
`aria-pressed` / `aria-selected` / `aria-current="page"` kept in sync · dialogs trap nothing but return focus ·
icons inside buttons are `aria-hidden` and the button has text or `aria-label`.
