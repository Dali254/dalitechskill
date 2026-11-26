# Page recipes

Each recipe lists the blocks in order (phone) and how they rearrange on desktop. Starter files are in
`assets/starter/`. Keep the same shell, tokens and components on every page.

## Dashboard — `index.html`
Greeting → balance card → Today/Withdrawn/Lifetime → My wallets → Ways to earn → Recent activity + Partner link.
Desktop: xl balance beside the stats; activity (main) + partner link (side).

## Sign in / Create account — `login.html`, `register.html`
No app shell. Phone: brand row (logo + dark-mode button), h1, one-line lead, single-column form, primary button,
link to the other page. ≥768: brand panel (gradient + 3D image + one honest promise) on the left, form on the right.
Register: username, phone with country code addon, optional email, password with show/hide, hidden `ref`
(from `?ref=`), terms checkbox only if the admin enabled it. No referral-code field when the link carries it.

## Withdraw — `withdraw.html`
Steps (Amount → Confirm → Done) → balance card (hint = minimum) → form: amount with KES addon, presets
(200/500/1,000/All), M-Pesa number, fee + "you receive" (`dl.sr-kv`) → Continue opens a **confirm sheet** that
repeats every number → toast on success. Side (desktop): "paid within minutes" alert + recent withdrawals.
Show the fee **before** confirming; the server must apply the same rule.

## Activity / transactions — `transactions.html`
Page head + period segmented control → KPI row → filter chips → table (stacked on phones, each row headed by
what happened and where it came from) → "Load more" with `aria-busy`.

## Ways to earn / tasks — `tasks.html`
Tabs per task type → search + Filters (sheet) → auto-fill grid of task cards (photo, status badge, rating,
reward, one clear action: Unlock / Write review) → side: today's progress + honesty rule.
Label AI-generated people/content as AI. Never show fake "X people earning now" counters.

## Profile & settings — `profile.html`
Profile header (avatar, name, member since, verified badge) → personal details form (2 columns ≥768) with inline
validation → preferences (dark mode, notifications switch, colour pattern) → FAQ accordion → Sign out.

## Admin overview — `admin.html` (`data-nav="admin"`)
Separate nav set. Page head + Export → KPI row → members table (search in the card head; stacked on phones)
+ withdrawals waiting (approve buttons, copyable callback URL) → settings form with switches and a sticky
**save bar**. Every money rule shown here must be enforced on the server.

## Components gallery — `components.html`
One of everything, with the pattern switcher. Use it to check a new skin quickly in light and dark.

## Other pages you will often need
| Page | Recipe |
|---|---|
| Notifications | list rows with unread dot, grouped by day, "Mark all read" in the page head |
| Team / referrals | partner link copy box + share buttons → level tabs → member rows (name, joined, earned for you) |
| Task detail | photo (16:10) → title, rating, reward → instructions → form (rating + textarea with counter) → sticky submit |
| Chat / practice | message bubbles (`max-width:80%`), composer fixed above tab bar, "AI practice partner" label in header |
| Maintenance | full-screen centred card, logo, one sentence, expected time; admins bypass |
| 404 / error | empty state with a 3D image, plain words, button home |
| Landing / pricing | hero with one promise and one button, 3 benefit tiles, honest FAQ, sticky CTA on phones |

## New page checklist
Shell (`body.sr-app[data-page][data-title]`, `.sr-main > main.sr-page`) · page head · mobile layout first ·
desktop arrangement with `.sr-lg-main-side` / `.sr-lg-2` / `.sr-auto` · empty + loading + error states ·
light/dark screenshots at 390/768/1280 · overflow + contrast checks.
