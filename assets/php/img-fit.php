<?php
/*
 * Phone-sized photos. For image CDNs that take w/h/q in the query string (Unsplash, imgix):
 * ask for the width the screen needs at quality 60 in AVIF/WebP. Other URLs are returned unchanged.
 *   <img src="<?= h(img_fit($url)) ?>"<?= img_srcset($url) ?> loading="lazy" decoding="async" width="480" height="341" alt="">
 */

function img_fit(string $url, int $w = 480): string {
    if ($url === '' || !preg_match('~images\.unsplash\.com|imgix\.net~i', $url)) return $url;
    $p = parse_url($url); parse_str($p['query'] ?? '', $q);
    $h = isset($q['h'], $q['w']) && (int)$q['w'] > 0 ? (int)round((int)$q['h'] * $w / (int)$q['w']) : null;
    $q['w'] = $w; if ($h) $q['h'] = $h; $q['q'] = 60; $q['auto'] = 'format'; $q['fit'] = $q['fit'] ?? 'crop';
    return ($p['scheme'] ?? 'https') . '://' . $p['host'] . ($p['path'] ?? '') . '?' . http_build_query($q);
}

function img_srcset(string $url, string $sizes = '(max-width: 600px) 92vw, 420px'): string {
    if (img_fit($url) === $url) return '';
    $e = static fn($s) => htmlspecialchars($s, ENT_QUOTES);
    return ' srcset="' . $e(img_fit($url, 480)) . ' 480w, ' . $e(img_fit($url, 900)) . ' 900w" sizes="' . $e($sizes) . '"';
}
