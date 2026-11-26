# Forms (register / login) and admin pages

## Register / login
- One column: every field on its own row (don't put country and phone side by side).
- Minimum fields. Hide what isn't needed: no referral code field when a `?ref=` link already carries it
  (keep it in a hidden input), no long marketing copy.
- Country: default to the main market (e.g. Kenya). If only one country is enabled, hide the field and fill it in.
- "I agree to the terms" checkbox is an admin setting (on/off).
- Big tap targets (≥48 px inputs), visible labels (not placeholder-only), show/hide password eye,
  `inputmode="tel"` for phones, `autocomplete` attributes.
- Errors next to the field, in words a member understands.
- Compact: no tall empty header; the submit button visible without scrolling on a 390×844 phone.

## Admin pages
- Every setting page has a clear **Save** button — sticky at the bottom on mobile — and a success message.
- Group settings in cards with a short explanation of what each does and its default.
- Toggles for features (maintenance mode, unlock modes, fees, "use my theme colours").
- Copyable values (webhook / callback URLs, API endpoints): read-only field + Copy button, with the full URL visible.
- Reorderable lists (side menu order) with up/down buttons that work on phones (not only drag).
- Previews next to visual settings (style picker thumbnails, share picture preview).
- Maintenance mode: admins still get in; members see a friendly page; test it while logged out.
- Money rules (fees, minimums, wallet splits) must be enforced on the server, not only shown in the UI —
  test the real flow after changing a rule.
