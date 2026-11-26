<?php
/*
 * Favicon + link-preview tags + a generated 1200×630 share picture (PHP GD).
 *
 * 1) In every public page <head>:   <?= share_head(['name'=>'NovaPal','title'=>'NovaPal',
 *        'description'=>'Earn online with simple tasks…','base'=>'https://site.com','version'=>'1.0']) ?>
 * 2) Route /og-image.png to a script that calls share_image_png([...same options..., 'icon'=>'/path/icon-512.png',
 *        'colors'=>['#e0098f','#7e22ce']]) and sends it with  header('Content-Type: image/png').
 * 3) Route /favicon.ico to your 48px PNG icon.
 */

function share_head(array $o): string {
    $e = static fn($s) => htmlspecialchars((string)$s, ENT_QUOTES);
    $base = rtrim($o['base'], '/');
    $img  = $base . '/og-image.png?v=' . rawurlencode($o['version'] ?? '1');
    $url  = $base . strtok($_SERVER['REQUEST_URI'] ?? '/', '#');          // keeps ?ref= so shared links keep the referrer
    $t = $e($o['title'] ?? $o['name']); $d = $e($o['description'] ?? '');
    return implode("\n", [
        '<link rel="icon" type="image/png" sizes="32x32" href="' . $e($o['icon32'] ?? '/icon-32.png') . '">',
        '<link rel="apple-touch-icon" href="' . $e($o['icon180'] ?? '/icon-180.png') . '">',
        '<meta name="description" content="' . $d . '">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="' . $e($o['name']) . '">',
        '<meta property="og:title" content="' . $t . '">',
        '<meta property="og:description" content="' . $d . '">',
        '<meta property="og:url" content="' . $e($url) . '">',
        '<meta property="og:image" content="' . $e($img) . '">',
        '<meta property="og:image:secure_url" content="' . $e($img) . '">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="' . $t . '">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="' . $t . '">',
        '<meta name="twitter:description" content="' . $d . '">',
        '<meta name="twitter:image" content="' . $e($img) . '">',
    ]) . "\n";
}

/** Draw the share picture: brand gradient, icon on a white rounded tile, name, description. Cached on disk. */
function share_image_png(array $o): string {
    $cache = ($o['cache_dir'] ?? sys_get_temp_dir()) . '/og-' . md5(json_encode($o)) . '.png';
    if (is_file($cache)) return (string)file_get_contents($cache);
    [$c1, $c2] = $o['colors'] ?? ['#e0098f', '#7e22ce'];
    $rgb = static fn($h) => sscanf(ltrim($h, '#'), '%02x%02x%02x');
    [$r1, $g1, $b1] = $rgb($c1); [$r2, $g2, $b2] = $rgb($c2);
    $W = 1200; $H = 630; $im = imagecreatetruecolor($W, $H);
    for ($x = 0; $x < $W; $x++) {                                         // diagonal-ish gradient
        $t = $x / ($W - 1);
        $col = imagecolorallocate($im, (int)($r1 + ($r2 - $r1) * $t), (int)($g1 + ($g2 - $g1) * $t), (int)($b1 + ($b2 - $b1) * $t));
        imageline($im, $x, 0, $x, $H, $col);
    }
    $white = imagecolorallocate($im, 255, 255, 255);
    imagefilledrectangle($im, 110, 175, 390, 455, $white);               // icon tile (square; round it with an image mask if you like)
    if (!empty($o['icon']) && is_file($o['icon']) && ($ic = @imagecreatefrompng($o['icon']))) {
        imagecopyresampled($im, $ic, 130, 195, 0, 0, 240, 240, imagesx($ic), imagesy($ic));
    }
    $font = $o['font'] ?? '';                                            // path to a .ttf (e.g. Poppins-Bold.ttf)
    if ($font && is_file($font)) {
        imagettftext($im, 64, 0, 450, 300, $white, $font, (string)$o['name']);
        $words = explode(' ', (string)($o['description'] ?? '')); $line = ''; $y = 370;
        foreach ($words as $w) {                                         // simple word wrap
            $try = trim($line . ' ' . $w); $box = imagettfbbox(30, 0, $font, $try);
            if ($box[2] > 680 && $line !== '') { imagettftext($im, 30, 0, 450, $y, $white, $font, $line); $y += 46; $line = $w; }
            else $line = $try;
        }
        if ($line !== '') imagettftext($im, 30, 0, 450, $y, $white, $font, $line);
    } else {
        imagestring($im, 5, 450, 300, (string)$o['name'], $white);
    }
    ob_start(); imagepng($im, null, 7); $png = (string)ob_get_clean(); imagedestroy($im);
    @file_put_contents($cache, $png);
    return $png;
}
