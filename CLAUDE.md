# CLAUDE.md — CleanAI Design System Rules

> Reference doc for integrating Figma designs into this codebase via MCP.

---

## Project Structure

This is a **single-file vanilla HTML/CSS project** — no framework, no bundler, no node_modules.

```
claude-code-figma/
└── index.html   ← everything lives here (HTML + CSS in <style> block)
```

All styles are **inline in a `<style>` block** inside `<head>`. When applying Figma designs, edit CSS there — do not create separate `.css` files unless the user explicitly asks to split them out.

---

## 1. Design Tokens

All tokens are defined as **CSS custom properties on `:root`** at the top of the `<style>` block (`index.html:13–25`).

```css
:root {
  /* Brand colors */
  --green:   #23D18B;   /* primary CTA, success, logo glow */
  --yellow:  #FFE566;   /* accent highlight, warm emphasis */
  --pink:    #FF6B9D;   /* secondary accent */
  --blue:    #5865F2;   /* Discord-style indigo, secondary CTAs */
  --purple:  #B96EFF;   /* tertiary accent */

  /* Backgrounds */
  --bg:      #111214;   /* page background */
  --surface: #1E1F22;   /* card/section surfaces */
  --surface2:#2B2D31;   /* elevated surface (plan cards, steps) */

  /* Text */
  --text:    #FFFFFF;   /* primary text */
  --muted:   #B5BAC1;   /* secondary/descriptive text */

  /* Utility */
  --border:  rgba(255,255,255,0.08);  /* all subtle dividers and card borders */
}
```

**Rule:** Always use `var(--token)` — never hardcode hex values in new styles. If a Figma design introduces a new color, add it as a new token to `:root` first.

---

## 2. Typography

Two Google Fonts are loaded (`index.html:7–8`):

| Font | Weight(s) | Usage |
|------|-----------|-------|
| `Space Grotesk` | 400, 500, 700, 800 | Body, headings, buttons — default font |
| `Press Start 2P` | 400 | Logo, step labels (`STEP_01`), badges — pixel/retro accent only |

```css
/* Applied via body */
body { font-family: 'Space Grotesk', sans-serif; }

/* Pixel font utility class */
.pixel { font-family: 'Press Start 2P', monospace; }

/* Also applied inline on specific elements */
font-family: 'Press Start 2P', monospace;
```

### Type Scale

```css
/* Hero H1 */      font-size: clamp(3rem, 7vw, 6rem);  font-weight: 800; letter-spacing: -3px;
/* Section H2 */   font-size: clamp(2rem, 4vw, 3rem);  font-weight: 800; letter-spacing: -1.5px;
/* Card H3 */      font-size: 1.1–1.25rem;              font-weight: 800; letter-spacing: -0.5px;
/* Body */         font-size: 0.875–1rem;               font-weight: 400–500;
/* Small/meta */   font-size: 0.75–0.85rem;
/* Pixel labels */ font-size: 0.45–0.65rem (Press Start 2P)
```

**Rule:** When translating Figma type styles, map to this scale. Use `clamp()` for headings that need fluid sizing. `letter-spacing` is consistently negative for headings — preserve this.

---

## 3. Spacing

No spacing token system — spacing is done with `rem` and `%` directly. Common patterns:

```css
/* Section vertical padding */  padding: 7rem 5%;
/* Section horizontal gutter */ padding: X 5%;      /* 5% is the standard page margin */
/* Card padding */              padding: 2rem;
/* Gap between grid items */    gap: 1.25rem–2rem;
/* Border radius — cards */     border-radius: 12–16px;
/* Border radius — pills */     border-radius: 999px;
/* Border radius — buttons */   border-radius: 6–8px;
```

---

## 4. Component Patterns

There is no component framework — components are **BEM-style CSS classes** applied to plain HTML elements.

### Buttons

Three variants, one size modifier, one layout modifier:

```html
<!-- Primary green CTA -->
<a href="#" class="btn btn-green">get started →</a>

<!-- Ghost / secondary -->
<a href="#" class="btn btn-ghost">log in</a>

<!-- Blue variant -->
<a href="#" class="btn btn-blue">connect</a>

<!-- Large size modifier -->
<a href="#" class="btn btn-green btn-lg">start cleaning free 🧹</a>

<!-- Full width (inside cards) -->
<a href="#" class="btn btn-green btn-full">get pro →</a>
```

**Button glow rule:** `btn-green` and `btn-blue` have a matching `box-shadow` glow. Always include it when adding new color variants.

### Cards

```html
<!-- Standard feature card -->
<div class="feat-card">...</div>

<!-- Wide card (spans 2 grid columns) -->
<div class="feat-card big">...</div>

<!-- Colored border glow variants -->
<div class="feat-card pink-glow">...</div>
<div class="feat-card purple-glow">...</div>
```

### Section Eyebrow Labels

```html
<div class="section-eyebrow">// section name</div>
```
Uses `Press Start 2P` at `0.55rem`, colored `var(--green)`, prefixed with `//`.

### Pill / Tag Badges

```html
<div class="feat-tag tag-green">🔍 AI detection</div>
<div class="feat-tag tag-pink">🔗 dedup</div>
<div class="feat-tag tag-blue">⚡ real-time</div>
<div class="feat-tag tag-purple">📐 normalize</div>
<div class="feat-tag tag-yellow">🛡️ compliance</div>
```

Each `tag-*` uses a 15% opacity background of its color + full-opacity text.

### Glow Blobs (decorative)

```html
<!-- Background ambient blobs -->
<div class="blob blob-1"></div>

<!-- Card internal glow (positioned absolute, top-right) -->
<div class="feat-glow" style="background:var(--green)"></div>
```

---

## 5. Layout

All layouts use **CSS Grid**. No flexbox for multi-column content.

```css
/* Features grid: 2 columns, big card spans both */
.features-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.feat-card.big   { grid-column: span 2; grid-template-columns: 1fr 1fr; }

/* 3-column grids (steps, testimonials) */
.steps     { display: grid; grid-template-columns: repeat(3,1fr); gap: 2rem; }
.cards-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.25rem; }
.plans     { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.25rem; }
```

Flexbox is used only for **single-axis alignment** (nav, buttons, stat rows, footers).

---

## 6. Styling Approach

- **Methodology:** Flat BEM-like class names. No nesting (plain CSS, no preprocessor).
- **No CSS Modules, no Tailwind, no Styled Components.**
- **Global styles** are in the single `<style>` block, organized by component with `/* ── SECTION NAME ── */` comments as dividers.
- **Inline styles** are used sparingly for one-off color overrides (e.g., `style="color:var(--green)"`). Keep this pattern — don't create single-use classes.

### Responsive Design

Single breakpoint at `768px` via a media query at the bottom of the style block:

```css
@media (max-width: 768px) {
  .nav-links { display: none; }
  .features-layout { grid-template-columns: 1fr; }
  .feat-card.big { grid-column: span 1; grid-template-columns: 1fr; }
  .steps, .cards-row, .plans { grid-template-columns: 1fr; }
}
```

**Rule:** All new multi-column grid sections must include a mobile override in this block.

---

## 7. Visual Effects

These recurring effects must be preserved when translating Figma designs:

| Effect | Implementation |
|--------|---------------|
| Glow on text | `text-shadow: 0 0 Xpx rgba(color, opacity)` |
| Glow on elements | `box-shadow: 0 0 Xpx rgba(color, opacity)` |
| Ambient blobs | Absolute `div`, `border-radius:50%`, `filter:blur(80px)`, low opacity |
| Hover lift | `transform: translateY(-2px to -4px)` on `:hover` |
| Floating stickers | `animation: float` keyframe with `translateY` + `rotate` |
| Marquee scroll | `animation: marquee` on duplicated content track |
| Noise overlay | SVG `feTurbulence` filter via `body::before` |
| Blink dot | `animation: blink` on status indicators |
| Backdrop blur nav | `backdrop-filter: blur(16px)` + semi-transparent `background` |

---

## 8. Figma → Code Integration Rules

### When receiving a Figma design via MCP:

1. **Map Figma color styles → CSS tokens.** If a Figma color matches an existing `--token`, use the variable. Only add new `:root` tokens for truly new colors.
2. **Preserve the Gen Z / Discord / Minecraft tone.** Informal copy, pixel font for labels, glow effects, floating emoji stickers.
3. **Match section structure:** New sections follow the `section-eyebrow → section-title → section-sub → content` hierarchy.
4. **Cards use `var(--surface)` or `var(--surface2)` backgrounds**, `1px solid var(--border)`, `border-radius: 16px`.
5. **All new buttons must follow the `.btn` base + variant modifier pattern.**
6. **Do not introduce new fonts.** Use Space Grotesk for body/headings, Press Start 2P for pixel accents only.
7. **Figma components → HTML sections/divs with CSS classes.** No JS framework needed.

### Pushing to Figma:

- The Figma capture script is already injected: `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>` (`index.html:9`)
- A local server on port `8080` (python3 http.server) is used for capture
- Existing Figma file: `https://www.figma.com/design/3dTLjsPCvzYYinkSBkasnj` (Witt's Team)
- **Do not remove the capture script tag.**

---

## 9. Assets & Icons

- **No image files.** All visuals are CSS (blobs, glows, gradients) or emoji.
- **Icons** are emoji characters rendered inline — no icon library, no SVG sprite.
- **No CDN** for assets. Only external dependencies are Google Fonts and the Figma capture script.

---

## 10. Page Sections (in order)

| Section | Selector | Background |
|---------|----------|------------|
| Nav | `nav` | `rgba(17,18,20,0.9)` + blur |
| Hero | `.hero` | `var(--bg)` |
| Marquee | `.marquee-wrap` | `var(--surface)` |
| Features | `.features` | `var(--bg)` |
| How It Works | `.how` | `var(--surface)` |
| Social Proof | `.social` | `var(--bg)` |
| Pricing | `.pricing` | `var(--surface)` |
| CTA Banner | `.cta-section` | `var(--bg)` |
| Footer | `footer` | `var(--bg)` |

Sections alternate between `var(--bg)` and `var(--surface)` for visual rhythm. Maintain this pattern.
