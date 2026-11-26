# Light and dark mode

## Switching
- `<html class="dark">` = dark. Save the member's choice (`localStorage` key, e.g. `sr-theme-v1 = {"mode":"dark"}`)
  and apply it **before first paint** with a tiny inline script in `<head>` to avoid a white flash.
- Default = the style's opening mode (from the registry), else the system (`prefers-color-scheme`).
- Moon / sun button in the top bar; it must be visible in both modes.

## Rules
1. Every skin defines both `@@TL` and `@@TD` tokens — a "dark style" still needs a real light version
   (e.g. light page + dark cards), because some members force light mode.
2. Set `color-scheme: light|dark` with the tokens so form controls and scrollbars match.
3. Text on brand colour: white only if the brand is dark enough; otherwise darken the button colour, not the text.
4. Brand-coloured text uses `--brand-fg`, which is darkened for light mode and lightened for dark mode.
5. Shadows in dark: deeper and more transparent (`0 8px 26px -16px #000b`); lines `#ffffff14–24`.
6. Pastels and very light cards must change in dark mode (tinted dark glass) — bright cards on a dark page glare.
7. Images/3D icons: add a subtle drop-shadow in dark so edges don't vanish.
8. Don't rely on opacity for secondary white text on colour cards (opacity .85 often fails AA); use full white
   and a smaller size/weight instead.

## Common dark-mode bugs to look for in screenshots
- Hard-coded `#fff` backgrounds (white boxes in dark), `color:#000` text (invisible).
- Gradient text (`background-clip:text`) that disappears — give a solid fallback colour.
- Inputs with light placeholder on light field, selects with white dropdowns.
- Badges / pills with light tint + light text.
- SVG icons with fixed `fill="#111"`; use `currentColor`.
- Third-party widgets (chat, payment iframes) — wrap in a surface card.

Always screenshot the same screens in both modes side by side before calling it done.
