# Favicon + link preview picture (WhatsApp, Facebook, Telegram, X)

When a member shares a link, apps read Open Graph tags from the page `<head>`. Put these on **every public
page** (home, register with `?ref=`, login), not only the home page.

```html
<link rel="icon" type="image/png" sizes="32x32" href="/pwa/icon.php?s=32">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon.ico">
<link rel="apple-touch-icon" href="/pwa/icon.php?s=180">
<meta name="description" content="Earn online with simple tasks and cash out straight to M-Pesa.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NovaPal">
<meta property="og:title" content="NovaPal">
<meta property="og:description" content="Earn online with simple tasks and cash out straight to M-Pesa.">
<meta property="og:url" content="https://site.com/auth/register?ref=ABC">
<meta property="og:image" content="https://site.com/og-image.png?v=N5.8.2">
<meta property="og:image:secure_url" content="https://site.com/og-image.png?v=N5.8.2">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="NovaPal">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://site.com/og-image.png?v=N5.8.2">
```

Rules
- `og:image` must be an **absolute https URL**, PNG/JPG, 1200×630, < 300 KB. WhatsApp ignores SVG/WebP.
- Change the `?v=` when the picture changes — apps cache previews for days.
- Generate the picture on the server from the app icon, name, brand gradient and share text
  (`assets/php/share-head.php` shows the GD approach) and cache it as a file.
- Admin settings: share title, share description, partner share text — with a live preview of the card.
- Serve `/favicon.ico` (browsers ask for it even without a tag) — a rewrite to the PNG icon is fine.
- Test with the Facebook Sharing Debugger / by sending the link in WhatsApp to yourself.
