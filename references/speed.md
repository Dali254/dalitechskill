# Fast pages on slow internet (3G, cheap Android phones)

Target: first paint < 4 s on Chrome "Slow 3G" (400 ms latency, 400 kbps), < 450 KB compressed per member page.
Measure before and after with `scripts/slow3g.py` and **block the service worker** while measuring
(otherwise you measure the offline cache, not the network).

## Biggest wins, in order

1. **Fewer files.** Every file is a round trip (0.3–0.6 s on 3G). Join back-to-back stylesheets and scripts
   (`assets/php/asset-bundle.php`: output buffer → regex joins runs of local `<link>`/`<script src>` → writes
   `assets/cache/b-<hash>.css|js` once, name = hash of file list + mtimes, so it rebuilds itself and can be cached
   forever). Only join *consecutive* tags so order never changes. Real result: 21 → 6 files.
2. **Subset icon fonts / icon sprites** to the icons the code actually uses. Scan code for `ph-<name>`,
   `ph-duotone-<name>` and quoted icon names (also from DB settings), then subset with fontTools:
   `pyftsubset Phosphor.woff2 --unicodes=<list> --flavor=woff2` (needs `brotli`), and cut the CSS/JS map to
   the same names. Keep originals as `*.full.*` and re-run after adding icons. Real result: 305 KB → 85 KB.
3. **Phone-sized images.** Serve 480 px to phones, 900 px to wider screens, quality ~60, AVIF/WebP
   (`assets/php/img-fit.php`: rewrites `w=`/`h=`/`q=` for Unsplash-style CDNs; `srcset` + `sizes`).
   Always `loading="lazy" decoding="async"` and fixed `width`/`height` (or `aspect-ratio`) to stop layout jumps.
4. **Compression + caching** (`.htaccess`):
   ```apache
   <IfModule mod_brotli.c>AddOutputFilterByType BROTLI_COMPRESS text/html text/css application/javascript application/json image/svg+xml</IfModule>
   <IfModule mod_deflate.c>AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml</IfModule>
   <IfModule mod_expires.c>ExpiresActive On
     ExpiresByType text/css "access plus 1 year"
     ExpiresByType application/javascript "access plus 1 year"
     ExpiresByType image/webp "access plus 1 year"
     ExpiresByType font/woff2 "access plus 1 year"</IfModule>
   ```
   Cache-bust with `?v=<ASSET_VER>` on every asset and bump the version on each release.
5. **Fonts:** self-hosted woff2, `font-display:swap`, ≤ 4 files. Preload only the one weight used above the fold.
6. **Scripts:** `defer` everything not needed for first paint; inline only the tiny theme bootstrap
   (dark-mode class) in `<head>`.
7. **CSS:** light minify in the bundler (strip comments, collapse spaces — keep spaces in `calc()` and in
   descendant selectors like `.a :hover`).
8. **Service worker:** cache-first for `/assets/`, network-first for pages, offline fallback page.

## Measuring

```
python3 scripts/slow3g.py https://site/dashboard https://site/withdraw --login https://site/login \
   --field phone=0712000111 --field password=secret --submit "form button[type=submit]"
```
Prints first contentful paint, load, file count, KB per page. Report a before → after table to the user.

If the test server does not compress like production, enable compression in the test server too,
otherwise the numbers are misleading.
