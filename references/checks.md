# Checks ("show me as you create")

## Screenshots
- Phone: 390×844 at device scale 3 (sharp, 1170 px wide). Desktop when relevant: 1280×900 @2x.
- For each change: light + dark, top of page + scroll steps. Build one labelled montage per comparison
  (`scripts/shots.py … --montage`), **look at it yourself first**, fix issues, then send it.
- When offering options, label them "1. Name … 5. Name" in the montage and ask the user to choose.
- Before/after: same viewport, same data, side by side.

## Contrast audit
`scripts/contrast_audit.py` hides all text, screenshots the page, and compares each text colour with the real
pixels behind it (works on gradients, images and glass, unlike most tools). 10th-percentile worst ratio is
used, need 4.5 (3.0 for large text). Fix failures by darkening the background or changing text colour —
never by shrinking the text check. Goal: **0 failures in light and dark**.

Quick pair check: `python3 scripts/contrast.py '#ffffff' '#cc4a08'` → 4.61 AA.

## Overflow / errors
`scripts/overflow_check.py` loads every page at 360 px and reports: horizontal scroll (`scrollWidth > 362`),
PHP "Warning/Notice/Fatal", JS page errors, HTTP 5xx. Goal: 0 problems on every style.

## Before saying done
- [ ] light + dark screenshots shown
- [ ] contrast 0 failures, overflow 0 problems, console clean
- [ ] speed measured when assets changed
- [ ] asset version bumped, changelog written, package has no `.env` / logs / caches
