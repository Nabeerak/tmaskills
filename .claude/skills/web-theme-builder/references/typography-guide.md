# Typography Guide: Font Pairing and Principles

## Table of Contents

1. [Font Pairing Principles](#font-pairing-principles)
2. [Type Scale](#type-scale)
3. [Font Weights](#font-weights)
4. [Variable Fonts](#variable-fonts)
5. [Web Font Optimization](#web-font-optimization)
6. [Popular Pairings by Theme](#popular-pairings-by-theme)
7. [References](#references)

---

## Font Pairing Principles

### Contrast Principle (Serif vs Sans-Serif)

The fundamental principle of font pairing is creating visual contrast while maintaining harmony. The most reliable approach combines serif and sans-serif typefaces:

- **Serif fonts** (e.g., Georgia, Playfair Display) convey tradition, elegance, and readability in long-form text
- **Sans-serif fonts** (e.g., Inter, Helvetica) offer modernity, clarity, and work well for UI elements
- **Pairing strategy**: Use serif for headlines with sans-serif body text, or vice versa

### Two-Font System Explained

A two-font system provides sufficient variety while maintaining consistency:

1. **Primary font**: Used for headings (h1-h3) and key UI elements
2. **Secondary font**: Used for body text, captions, and supporting content

**Benefits**:
- Reduces cognitive load for readers
- Faster page load times (fewer font files)
- Easier to maintain design consistency
- Better performance on mobile devices

### When to Use One Font Family vs Two

**Single Font Family**:
- Modern web applications with clean aesthetics
- When using a versatile typeface (e.g., Inter, Roboto) with multiple weights
- Minimalist designs prioritizing simplicity
- Examples: GitHub, Stripe, Linear

**Two Font Families**:
- Content-heavy sites (blogs, magazines, documentation)
- When creating distinct visual hierarchy
- Brand differentiation through typography
- Examples: Medium, The New York Times, Shopify

---

## Type Scale

### Modular Scale Explanation

A modular scale creates harmonious typography by multiplying a base size by a consistent ratio. Common ratios:

- **1.125 (Major Second)**: Subtle, conservative progression
- **1.200 (Minor Third)**: Balanced, versatile for most designs
- **1.250 (Major Third)**: Noticeable contrast, popular for web
- **1.333 (Perfect Fourth)**: Strong hierarchy, editorial designs
- **1.618 (Golden Ratio)**: Maximum contrast, dramatic designs

### Standard Sizes (XS through 5XL)

Based on a 16px base with 1.250 ratio:

| Size  | Scale | Pixels | REM   | Use Case                    |
|-------|-------|--------|-------|-----------------------------|
| xs    | 0.64  | 10px   | 0.625 | Fine print, captions        |
| sm    | 0.8   | 13px   | 0.813 | Small labels, metadata      |
| base  | 1.0   | 16px   | 1.0   | Body text, paragraphs       |
| lg    | 1.25  | 20px   | 1.25  | Lead paragraphs, subheads   |
| xl    | 1.563 | 25px   | 1.563 | h4, card titles             |
| 2xl   | 1.953 | 31px   | 1.953 | h3, section headings        |
| 3xl   | 2.441 | 39px   | 2.441 | h2, page subtitles          |
| 4xl   | 3.052 | 49px   | 3.052 | h1, hero headings           |
| 5xl   | 3.815 | 61px   | 3.815 | Display, marketing headers  |

### Line Height Recommendations

Line height (leading) affects readability and visual rhythm:

- **Headings (h1-h3)**: 1.1 - 1.3 (tighter spacing)
- **Body text**: 1.5 - 1.7 (optimal readability)
- **Small text**: 1.4 - 1.5 (slightly tighter)
- **Wide columns (>80ch)**: 1.7 - 1.8 (more breathing room)
- **Narrow columns (<60ch)**: 1.5 - 1.6 (standard)

**Formula**: Line height typically = 1.5 × font size for body text

### Letter Spacing Guidelines

Letter spacing (tracking) fine-tunes typographic texture:

- **Headings**: -0.02em to -0.05em (tighter, more cohesive)
- **Body text**: 0em (default, no adjustment needed)
- **Small text (<14px)**: +0.01em to +0.02em (improves legibility)
- **All caps**: +0.05em to +0.1em (essential for readability)
- **Monospace code**: -0.01em (prevents excessive width)

---

## Font Weights

### When to Use Each Weight (300-700)

| Weight | Name       | Use Case                                    |
|--------|------------|---------------------------------------------|
| 300    | Light      | Large headings, elegant designs, quotes     |
| 400    | Regular    | Body text, default for paragraphs           |
| 500    | Medium     | Emphasized text, subheadings, navigation    |
| 600    | Semi-Bold  | Buttons, labels, strong emphasis            |
| 700    | Bold       | Headlines, important CTAs, highlights       |

**Avoid**:
- Weights below 300 (poor readability on screens)
- Weights above 700 (overwhelming, reduces readability)

### Creating Hierarchy with Weights

Combine size and weight for effective hierarchy:

```css
h1 { font-size: 3rem; font-weight: 700; }
h2 { font-size: 2.5rem; font-weight: 600; }
h3 { font-size: 2rem; font-weight: 600; }
h4 { font-size: 1.5rem; font-weight: 500; }
body { font-size: 1rem; font-weight: 400; }
.emphasis { font-size: 1rem; font-weight: 600; }
```

### Performance Considerations

Each font weight requires a separate file download:

- **Limit to 3-4 weights** per project (e.g., 400, 500, 600, 700)
- Use variable fonts for unlimited weights with single file
- Remove unused weights from Google Fonts URLs
- Consider system fonts to eliminate HTTP requests entirely

---

## Variable Fonts

### Benefits of Variable Fonts

Variable fonts contain multiple variations in a single file:

- **Performance**: One file vs multiple weight/style files (60-80% size reduction)
- **Flexibility**: Infinite weight/width/slant values between defined axes
- **Animation**: Smooth transitions between weights and styles
- **Responsive typography**: Adjust weights based on viewport size

**Axes**:
- `wght` (weight): 100-900
- `wdth` (width): 75-125%
- `slnt` (slant): -10 to 0 degrees
- `ital` (italic): 0 or 1

### Browser Support

Variable fonts are widely supported (95%+ browsers as of 2024):

- Chrome 66+ (2018)
- Firefox 62+ (2018)
- Safari 11.1+ (2018)
- Edge 17+ (2018)

**Fallback strategy**:
```css
@supports (font-variation-settings: normal) {
  font-family: 'InterVariable', sans-serif;
}
```

### Implementation Examples

```css
/* Using variable font */
@font-face {
  font-family: 'InterVariable';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}

body {
  font-family: 'InterVariable', system-ui, sans-serif;
  font-weight: 400;
}

h1 {
  font-weight: 700;
  /* Or use custom values */
  font-variation-settings: 'wght' 750;
}

/* Responsive weight adjustment */
@media (min-width: 768px) {
  h1 { font-variation-settings: 'wght' 800; }
}
```

---

## Web Font Optimization

### font-display: swap

Controls how fonts are displayed during loading:

```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately, swap when loaded */
}
```

**Options**:
- `swap`: Best for readability (show text immediately)
- `optional`: Use custom font only if cached (best performance)
- `fallback`: 100ms block, 3s swap period (balanced approach)

### Subset Fonts

Reduce file size by including only needed characters:

- **Google Fonts**: `?text=Hello` parameter for specific characters
- **Subset tools**: glyphhanger, fonttools (pyftsubset)
- **Common subsets**: Latin, Latin-Extended, Cyrillic

**Example**:
```html
<!-- Only Latin characters -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&subset=latin" rel="stylesheet">
```

### Preloading Strategies

Prioritize critical fonts for faster rendering:

```html
<!-- Preload primary font -->
<link rel="preload" href="/fonts/Inter-Variable.woff2" as="font" type="font/woff2" crossorigin>

<!-- Preconnect to Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

### Self-Hosting vs CDN

**Self-Hosting**:
- Pros: Full control, no external dependencies, privacy, HTTP/2 push
- Cons: Requires server management, no global CDN benefits

**CDN (Google Fonts)**:
- Pros: Automatic optimization, likely cached, updates handled
- Cons: External dependency, privacy concerns, GDPR considerations

**Recommendation**: Self-host for production apps, use CDN for prototyping

---

## Popular Pairings by Theme

### Modern

**Inter + Inter** (Single family)
- Headings: Inter 600-700
- Body: Inter 400
- Used by: GitHub, Vercel, Linear
- Why: Versatile, excellent screen rendering, 9 weights

**SF Pro Display + SF Pro Text**
- Headings: SF Pro Display 600
- Body: SF Pro Text 400
- Used by: Apple ecosystem
- Why: Optimized for different sizes, native Apple feel

### Corporate

**IBM Plex Sans + IBM Plex Serif**
- Headings: IBM Plex Serif 600
- Body: IBM Plex Sans 400
- Used by: IBM, enterprise applications
- Why: Professional, comprehensive family, excellent legibility

**Roboto + Roboto Slab**
- Headings: Roboto Slab 700
- Body: Roboto 400
- Used by: Google Material Design
- Why: Highly readable, geometric, pairs perfectly

### Creative

**Playfair Display + Source Sans Pro**
- Headings: Playfair Display 700
- Body: Source Sans Pro 400
- Used by: Medium, editorial sites
- Why: Classic elegance meets modern clarity

**Montserrat + Merriweather**
- Headings: Montserrat 700
- Body: Merriweather 400
- Used by: Creative agencies, portfolios
- Why: Geometric sans with warm serif, high contrast

### Technical

**JetBrains Mono** (Monospace)
- Code: JetBrains Mono 400
- Used by: IDEs, developer tools
- Why: Designed for developers, excellent ligatures

**Space Grotesk + Space Mono**
- Headings: Space Grotesk 700
- Code: Space Mono 400
- Used by: Tech startups, developer sites
- Why: Modern geometric with matching monospace

---

## References

1. **Elementor Font Pairing Chart**: Comprehensive visual guide to pairing 50+ Google Fonts with examples and use cases
   - https://elementor.com/blog/font-pairing/

2. **Elegant Themes Typography Principles**: Deep dive into contrast, hierarchy, and pairing strategies
   - https://www.elegantthemes.com/blog/design/font-pairing

3. **Figma Font Pairings Community**: Curated collection of font combinations with live previews
   - https://www.figma.com/community/search?resource_type=files&q=font%20pairings

4. **Google Fonts Knowledge**: Typography best practices and technical guidance
   - https://fonts.google.com/knowledge

5. **Typewolf**: Real-world font pairing examples from top websites
   - https://www.typewolf.com/

6. **Variable Fonts Guide** by MDN: Technical implementation and browser support
   - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Fonts/Variable_Fonts_Guide

7. **Web Font Loading Best Practices** by Zach Leatherman
   - https://www.zachleat.com/web/comprehensive-webfonts/
