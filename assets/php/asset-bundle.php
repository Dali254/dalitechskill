<?php
// =============================================================================
// ASSET BUNDLING — fewer downloads on slow internet.
// Member pages loaded ~14 stylesheets and ~7 scripts; on 3G every extra file
// costs a round trip (0.3–0.6 s). asset_bundle_html() runs over the finished
// page and joins each run of back-to-back local <link rel="stylesheet"> tags
// into one file, and each run of plain local <script src> tags into one file.
// Order is kept exactly (only consecutive tags are joined, nothing moves past
// an inline <style> or <script>). Bundles are written once to /assets/cache/
// and rebuilt automatically when any source file changes (name = hash of the
// file list + their modification times). If the folder is not writable the
// page is sent unchanged. Turn off: define('ASSET_BUNDLING', false) or a setting.
//
// USE: require this file, then call asset_bundle_start() at the very top of your
// page header (before any output). Set ASSET_BUNDLE_ROOT if your web root is not
// the parent of this file's folder.
// =============================================================================

function asset_bundling_on(): bool {
    static $on = null;
    if ($on !== null) return $on;
    if (defined('ASSET_BUNDLING')) return $on = (bool)ASSET_BUNDLING;
    try { $on = function_exists('get_setting') ? (string)get_setting('asset_bundling', '1') === '1' : true; } catch (Throwable $e) { $on = false; }
    return $on;
}

/** Start buffering the page so its <link>/<script> tags can be joined at the end. */
function asset_bundle_start(): void {
    static $started = false;
    if ($started || PHP_SAPI === 'cli' || !asset_bundling_on()) return;
    $started = true;
    ob_start('asset_bundle_html');
}

function asset_bundle_html(string $html): string {
    if (stripos($html, '<html') === false) return $html;                    // not a full page
    try {
        $root = defined('ASSET_BUNDLE_ROOT') ? ASSET_BUNDLE_ROOT : dirname(__DIR__);
        $dir  = $root . '/assets/cache';
        if (!is_dir($dir) && !@mkdir($dir, 0755, true)) return $html;
        if (!is_writable($dir)) return $html;
        $local = '/assets/[^"\'?#\s]+';
        // runs of local stylesheets (only whitespace between them)
        $css = '~(?:<link rel="stylesheet" href="(' . $local . '\.css)(?:\?[^"]*)?"\s*/?>\s*){2,}~';
        $html = preg_replace_callback($css, static function ($m) use ($root, $dir) {
            preg_match_all('#href="(/assets/[^"?]+\.css)#', $m[0], $mm);
            $out = asset_bundle_write($mm[1], 'css', $root, $dir);
            return $out ? '<link rel="stylesheet" href="' . $out . '">' . "\n" : $m[0];
        }, $html) ?? $html;
        // runs of plain local scripts: <script src="/assets/….js?v=…"></script> (no other attributes)
        $js = '~(?:<script src="(' . $local . '\.js)(?:\?[^"]*)?"></script>\s*){2,}~';
        $html = preg_replace_callback($js, static function ($m) use ($root, $dir) {
            preg_match_all('#src="(/assets/[^"?]+\.js)#', $m[0], $mm);
            $out = asset_bundle_write($mm[1], 'js', $root, $dir);
            return $out ? '<script src="' . $out . '"></script>' . "\n" : $m[0];
        }, $html) ?? $html;
    } catch (Throwable $e) { error_log('[asset_bundle] ' . $e->getMessage()); }
    return $html;
}

/** Write (once) the joined file and return its address, or '' to keep the original tags. */
function asset_bundle_write(array $files, string $ext, string $root, string $dir): string {
    $sig = '';
    foreach ($files as $f) {
        $p = $root . $f;
        if (!is_file($p)) return '';                                       // unknown file: leave the tags alone
        $sig .= $f . ':' . filemtime($p) . ':' . filesize($p) . '|';
    }
    $name = 'b-' . substr(md5($sig), 0, 16) . '.' . $ext;
    $path = $dir . '/' . $name;
    if (!is_file($path)) {
        $buf = '';
        foreach ($files as $f) {
            $src = (string)file_get_contents($root . $f);
            if ($ext === 'css') {
                $base = dirname($f);
                // url(x) relative to the source file → absolute, so fonts / images still load
                $src = preg_replace_callback('#url\(\s*([\'"]?)(?!data:|https?:|//|/|\#)([^\'")]+)\1\s*\)#i', static function ($u) use ($base) {
                    $parts = [];
                    foreach (explode('/', $base . '/' . $u[2]) as $seg) {
                        if ($seg === '' || $seg === '.') continue;
                        if ($seg === '..') { array_pop($parts); continue; }
                        $parts[] = $seg;
                    }
                    return 'url("/' . implode('/', $parts) . '")';
                }, $src);
                $src = preg_replace('#@charset\s+"[^"]*";#i', '', $src);
                $buf .= "/*" . $f . "*/\n" . asset_min_css($src) . "\n";
            } else {
                $buf .= "/* " . $f . " */\n" . rtrim($src) . "\n;\n";
            }
        }
        $tmp = $path . '.' . getmypid() . '.tmp';
        if (@file_put_contents($tmp, $buf) === false || !@rename($tmp, $path)) { @unlink($tmp); return ''; }
        foreach (glob($dir . '/b-*.' . $ext) ?: [] as $old) {             // tidy: drop bundles unused for a week
            if ($old !== $path && filemtime($old) < time() - 7 * 86400) @unlink($old);
        }
    }
    return '/assets/cache/' . $name;
}

/**
 * Light, safe CSS shrink: drops comments and extra spaces. Spaces that change meaning
 * (descendant selectors such as ".a :hover", calc() operators) are kept.
 */
function asset_min_css(string $css): string {
    $out = preg_replace('#/\*(?!!)[\s\S]*?\*/#', '', $css);                 // comments (keep /*! licences */)
    if ($out === null) return $css;
    $out = preg_replace('/\s+/', ' ', $out) ?? $out;                          // runs of spaces / new lines
    $out = preg_replace('/\s*([{};,])\s*/', '$1', $out) ?? $out;              // around { } ; ,
    $out = preg_replace('/:\s+/', ':', $out) ?? $out;                          // "color: red" → "color:red"
    $out = str_replace(';}', '}', $out);
    return trim($out);
}
