# Color Systems Reference Guide

## Table of Contents

1. [Color Theory Basics](#color-theory-basics)
2. [HSL Color System](#hsl-color-system)
3. [Palette Generation Strategy](#palette-generation-strategy)
4. [Accessibility Standards (WCAG)](#accessibility-standards-wcag)
5. [Dark Mode Implementation](#dark-mode-implementation)
6. [Tailwind CSS v4.0 Integration](#tailwind-css-v40-integration)
7. [References](#references)

---

## Color Theory Basics

### HSL vs RGB/Hex: Why HSL for Design Systems

**RGB/Hex Format:**
- Represents colors through Red, Green, Blue channels (0-255)
- Example: `#3B82F6` or `rgb(59, 130, 246)`
- Difficult to create color variations programmatically
- Not intuitive for human color manipulation

**HSL Format:**
- Represents colors through Hue (0-360°), Saturation (0-100%), Lightness (0-100%)
- Example: `hsl(217, 91%, 60%)`
- **Advantages for design systems:**
  - Easy to generate consistent color scales
  - Intuitive adjustments (darker/lighter = change lightness)
  - Maintains color harmony when creating variations
  - Simplifies theme switching and dark mode

### Color Psychology for Web Design

According to Loungelizard's color trends research, colors evoke specific psychological responses:

- **Blue**: Trust, professionalism, security (finance, tech)
- **Green**: Growth, health, sustainability (eco, health)
- **Red**: Energy, urgency, passion (sales, food)
- **Purple**: Luxury, creativity, wisdom (beauty, creative)
- **Orange**: Friendliness, enthusiasm, warmth (social, entertainment)
- **Yellow**: Optimism, clarity, caution (education, warning states)

### Semantic Color Naming Conventions

Use purpose-driven names instead of literal colors:

```css
/* Good - Semantic */
--color-primary
--color-success
--color-danger
--color-warning
--color-neutral

/* Avoid - Literal */
--color-blue
--color-green
--color-red
```

---

## HSL Color System

### How HSL Works

**Hue (0-360°)**: Position on the color wheel
- 0° / 360° = Red
- 120° = Green
- 240° = Blue

**Saturation (0-100%)**: Color intensity
- 0% = Grayscale
- 100% = Full color vibrancy

**Lightness (0-100%)**: Brightness
- 0% = Black
- 50% = Pure color
- 100% = White

### Benefits for Scalability and Theming

1. **Consistent color scales**: Adjust only lightness to create shades
2. **Easy theme variations**: Change hue while maintaining structure
3. **Mathematical predictability**: Algorithmic color generation
4. **Dark mode support**: Invert lightness values systematically

### Converting Between Formats

```javascript
// Hex to HSL conversion
function hexToHSL(hex) {
  let r = parseInt(hex.slice(1, 3), 16) / 255;
  let g = parseInt(hex.slice(3, 5), 16) / 255;
  let b = parseInt(hex.slice(5, 7), 16) / 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h, s, l = (max + min) / 2;

  if (max === min) {
    h = s = 0; // achromatic
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
      case g: h = ((b - r) / d + 2) / 6; break;
      case b: h = ((r - g) / d + 4) / 6; break;
    }
  }

  return [h * 360, s * 100, l * 100];
}
```

---

## Palette Generation Strategy

### Primary Color Selection

Choose a primary color that:
- Aligns with brand identity and psychology
- Has sufficient contrast potential for accessibility
- Works in both light and dark modes
- Example: `hsl(217, 91%, 60%)` - Trust-evoking blue

### Generating Secondary and Accent Colors

**Analogous colors** (30-60° apart):
```javascript
const primary = { h: 217, s: 91, l: 60 };
const secondary = { h: 187, s: 85, l: 55 }; // 30° shift
const accent = { h: 277, s: 70, l: 65 }; // Complementary
```

**Complementary colors** (180° opposite):
- Creates visual tension and emphasis
- Use sparingly for CTAs and highlights

### Shade Generation (50-900 Scale)

Following Material Design and Tailwind conventions:

```javascript
const shadeScale = {
  50: { l: 97, s: 80 },   // Lightest
  100: { l: 94, s: 85 },
  200: { l: 86, s: 88 },
  300: { l: 76, s: 90 },
  400: { l: 65, s: 91 },
  500: { l: 60, s: 91 },  // Base color
  600: { l: 52, s: 92 },
  700: { l: 44, s: 88 },
  800: { l: 36, s: 84 },
  900: { l: 28, s: 80 },  // Darkest
};

// Generate full palette
function generatePalette(baseHue) {
  const palette = {};
  for (const [shade, { l, s }] of Object.entries(shadeScale)) {
    palette[shade] = `hsl(${baseHue}, ${s}%, ${l}%)`;
  }
  return palette;
}
```

### Maintaining Harmony

- Keep hue constant across shades for consistency
- Slightly adjust saturation (±5-10%) for visual balance
- Lighter shades: reduce saturation to avoid neon appearance
- Darker shades: reduce saturation to maintain richness

**Examples:**

```css
/* ✅ Good: Consistent hue, adjusted saturation */
--color-primary-50: hsl(220, 70%, 97%);   /* Reduced saturation for light shade */
--color-primary-500: hsl(220, 90%, 56%);  /* Base color */
--color-primary-900: hsl(220, 80%, 20%);  /* Slightly reduced for dark shade */

/* ❌ Bad: Random hue changes break visual harmony */
--color-primary-50: hsl(200, 70%, 97%);   /* Different hue - looks inconsistent */
--color-primary-500: hsl(220, 90%, 56%);
--color-primary-900: hsl(240, 80%, 20%);  /* Different hue - breaks system */

/* ✅ Good: Sufficient contrast for accessibility */
--color-background: hsl(0, 0%, 100%);
--color-text: hsl(0, 0%, 10%);            /* 18.4:1 contrast ratio */

/* ❌ Bad: Poor contrast fails WCAG */
--color-background: hsl(0, 0%, 100%);
--color-text: hsl(0, 0%, 70%);            /* 2.4:1 contrast - fails AA */
```

---

## Accessibility Standards (WCAG)

### Contrast Ratio Requirements

**WCAG 2.1 Level AA Standards:**
- **Normal text** (< 18pt): 4.5:1 minimum contrast ratio
- **Large text** (≥ 18pt or 14pt bold): 3:1 minimum contrast ratio
- **UI components**: 3:1 for interactive elements

**WCAG AAA Standards** (recommended):
- Normal text: 7:1
- Large text: 4.5:1

### Calculating Contrast Ratios

```javascript
function getContrastRatio(color1, color2) {
  const l1 = getLuminance(color1);
  const l2 = getLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Ensure text meets WCAG AA
function meetsWCAG_AA(textColor, bgColor, isLargeText = false) {
  const ratio = getContrastRatio(textColor, bgColor);
  return isLargeText ? ratio >= 3 : ratio >= 4.5;
}
```

### Tools for Checking Contrast

- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Contrast Ratio**: https://contrast-ratio.com/
- **Browser DevTools**: Built-in contrast checkers (Chrome, Firefox)
- **Figma/Design Tools**: Stark, Contrast plugins

### Color-Blind Considerations

**8% of males and 0.5% of females** have color vision deficiencies:

- **Deuteranopia/Protanopia** (red-green): Most common
- **Tritanopia** (blue-yellow): Less common

**Best practices:**
- Never rely on color alone to convey information
- Use patterns, icons, or text labels alongside color
- Test with color-blind simulation tools (Chrome DevTools, Color Oracle)
- Avoid red-green combinations for success/error states

---

## Dark Mode Implementation

### Inverting Lightness Values

**Light mode to dark mode transformation:**

```javascript
function invertForDarkMode(lightness) {
  // Invert around 50% midpoint
  return 100 - lightness;
}

// Example: Light mode primary-500 (l: 60%)
// Dark mode: 100 - 60 = 40% (too dark)
// Better approach: Use adjusted scale
const darkModeAdjustment = {
  50: 900,   // Lightest becomes darkest
  100: 800,
  200: 700,
  300: 600,
  400: 500,
  500: 400,
  600: 300,
  700: 200,
  800: 100,
  900: 50,   // Darkest becomes lightest
};
```

### Maintaining Saturation

- **Reduce saturation** in dark mode by 10-20% to prevent eye strain
- Fully saturated colors appear too vibrant on dark backgrounds
- Example: Light mode `hsl(217, 91%, 60%)` → Dark mode `hsl(217, 75%, 65%)`

### Avoiding Pure Black

According to Material Design and Medium's design systems:

- **Don't use** `#000000` (pure black) for backgrounds
- **Use** `hsl(0, 0%, 8-12%)` for primary dark background
- **Reason**: Pure black creates harsh contrast and eye fatigue
- Elevated surfaces should be lighter (12-16%) to show depth

```css
/* Dark mode color scheme */
:root[data-theme="dark"] {
  --bg-primary: hsl(0, 0%, 10%);
  --bg-secondary: hsl(0, 0%, 14%);
  --bg-elevated: hsl(0, 0%, 18%);
  --text-primary: hsl(0, 0%, 95%);
  --text-secondary: hsl(0, 0%, 70%);
}
```

### Testing Dark Mode Colors

1. **Use real devices**: OLED vs LCD displays render differently
2. **Test in low-light environments**: Simulates actual usage
3. **Check at different brightness levels**
4. **Verify contrast ratios** still meet WCAG standards
5. **Use system preferences**: Test auto theme switching

---

## Tailwind CSS v4.0 Integration

### Using @theme with HSL

Tailwind CSS v4.0 introduces the `@theme` directive for design tokens:

```css
@theme {
  /* Primary color palette */
  --color-primary-50: hsl(217, 80%, 97%);
  --color-primary-100: hsl(217, 85%, 94%);
  --color-primary-200: hsl(217, 88%, 86%);
  --color-primary-300: hsl(217, 90%, 76%);
  --color-primary-400: hsl(217, 91%, 65%);
  --color-primary-500: hsl(217, 91%, 60%);
  --color-primary-600: hsl(217, 92%, 52%);
  --color-primary-700: hsl(217, 88%, 44%);
  --color-primary-800: hsl(217, 84%, 36%);
  --color-primary-900: hsl(217, 80%, 28%);

  /* Semantic colors */
  --color-success: hsl(142, 71%, 45%);
  --color-warning: hsl(38, 92%, 50%);
  --color-danger: hsl(0, 84%, 60%);
  --color-info: hsl(199, 89%, 48%);
}
```

### Design Token Examples

```css
@theme {
  /* Light mode (default) */
  --color-background: hsl(0, 0%, 100%);
  --color-foreground: hsl(0, 0%, 10%);
  --color-muted: hsl(0, 0%, 96%);
  --color-border: hsl(0, 0%, 90%);
}

/* Dark mode override */
@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: hsl(0, 0%, 10%);
    --color-foreground: hsl(0, 0%, 95%);
    --color-muted: hsl(0, 0%, 14%);
    --color-border: hsl(0, 0%, 20%);
  }
}
```

### CSS Variable Patterns

```css
/* Using CSS variables for dynamic theming */
:root {
  /* Define HSL channels separately for transparency */
  --primary-h: 217;
  --primary-s: 91%;
  --primary-l: 60%;

  /* Compose full color */
  --color-primary: hsl(var(--primary-h), var(--primary-s), var(--primary-l));

  /* Easy transparency */
  --color-primary-alpha: hsla(var(--primary-h), var(--primary-s), var(--primary-l), 0.5);
}

/* Tailwind utility classes */
.bg-primary {
  background-color: var(--color-primary);
}

.text-primary-600 {
  color: var(--color-primary-600);
}
```

---

## References

1. **Loungelizard** - "Color Trends in Web Design"
   Insights on color psychology and modern web design trends
   https://www.loungelizard.com/

2. **Elementor** - "Color Theory for Web Design"
   Comprehensive guide to applying color theory in digital design
   https://elementor.com/blog/color-theory/

3. **Medium Design Systems** - "Building a Color System"
   Article on scalable color systems and design token architecture
   https://medium.com/

4. **WCAG 2.1 Guidelines** - Web Content Accessibility Guidelines
   Official standards for color contrast and accessibility
   https://www.w3.org/WAI/WCAG21/

5. **Material Design** - Color System
   Google's approach to color in design systems
   https://m3.material.io/styles/color/

6. **Tailwind CSS v4.0 Documentation** - Theme Configuration
   Official documentation for the new @theme directive
   https://tailwindcss.com/
