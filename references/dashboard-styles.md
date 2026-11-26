# Switchable dashboard styles ("skins")

One markup, many looks. The admin picks a style; members can preview with `?ds=<key>` (sticky in the session,
`?ds=off` clears it). The `<html>` element carries `data-ds="<key>"` and `class="dark"` in dark mode.

## Registry (PHP example)

```php
function ds_list(): array {           // key => [name, short tag, opens in light|dark, description, [paper, brand, accent]]
    return [
      'profiz'       => ['Profiz 3', 'Profiz 3 dashboard', 'light', 'White greeting card, full-width colour cards, pink brand.', ['#f6f5fb','#e0098f','#1a8259']],
      'profizneon'   => ['Profiz 3 Neon Ocean', 'Profiz 3, neon night', 'dark', 'Dark glass cards with glowing edges.', ['#0f0d16','#22d3ee','#a78bfa']],
      // …
    ];
}
function ds_layouts(): array {       // key => [tasks layout, stats layout, wallets layout]
    return ['profiz' => ['list','cards','cards'], /* … */];
}
function ds_current(): string {      // ?ds= preview → session → setting; unknown keys fall back; renamed keys alias
    $v = $_SESSION['ds_preview'] ?? get_setting('dash_style', 'sunrise');
    $v = ['profizglow' => 'profizsunset', 'profiznight' => 'profizneon'][$v] ?? $v;
    return isset(ds_list()[$v]) ? $v : 'sunrise';
}
```

When you **rename or remove** a style, add an alias so sites that chose it move to the closest new one.

Load order in `<head>`: base CSS → shared `ds-base.css` → `assets/ds/<key>.css`.

## Skin source format (build with `scripts/gen_skin.py`)

```
@@head        raw CSS placed first (e.g. @import of a font)
@@T           tokens for both modes
@@TL          light-mode tokens
@@TD          dark-mode tokens
@@B           brand colours (skipped when the admin chose "use my own theme colours")
@@C           rules for both modes   — start each selector with "P " (the scope prefix)
@@CL          light-only rules
@@CD          dark-only rules
```

The generator turns `P .sr-stat{…}` into `html[data-ds="key"]:not(#ds-a):not(#ds-b) .sr-stat{…}`.
The two `:not(#id)` raise specificity so skins beat theme palettes and older bridge rules without needing
`!important` everywhere. If a shared rule still wins (e.g. a `display:none!important` with 3 ids), add more
`:not(#x)` to that one selector — do not fight with more `!important`.

## Making a new style — checklist

1. Write `skins/<key>.css` (tokens for TL **and** TD, brand, rules).
2. Register it in `ds_list()`, `ds_layouts()`, greeting style map.
3. Build: `python3 scripts/gen_skin.py skins assets/ds`.
4. Screenshot light + dark (`scripts/shots.py URL?ds=<key>` and `--dark`), look, fix.
5. Previews for the admin picker: `assets/ds/prev/<key>_{light,dark}.webp` (240×532, crop of the 390-wide
   screenshot). The picker shows the preview for the style's opening mode.
6. Contrast audit both modes + overflow check on every member page.
7. Bump the asset version so browsers fetch the new CSS.

## Variants that must look different

When the user asks for "other versions of the same design", keep layout, radius, fonts and anatomy, and change
**colour pattern + icon-behind-card style + finish**. Variants that only differ in shadow strength look identical
to users — avoid that. Offer 5 options as one labelled montage and let the user choose before wiring them in.
