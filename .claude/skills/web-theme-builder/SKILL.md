---
name: web-theme-builder
description: |
  Build production-ready website themes with pre-configured color palettes, typography pairings, component libraries, and Tailwind CSS configurations for 8 aesthetic styles (Modern/Minimalist, Corporate, Creative, Dark/Tech, Warm, E-commerce, SaaS, Portfolio). This skill should be used when users ask to create website themes, design landing pages, build component libraries, configure Tailwind themes, or implement responsive design systems with specific aesthetic styles.
---

# Web Design Theme Builder

Build professional website themes quickly with pre-designed aesthetic systems.

## What This Skill Does

- Creates complete theme systems with color palettes, typography, and components
- Generates Tailwind CSS v4.0 configurations with @theme directive
- Provides 8 pre-designed aesthetic variations (Modern, Corporate, Creative, Dark, Warm, E-commerce, SaaS, Portfolio)
- Builds responsive HTML/CSS components (buttons, cards, forms, navigation, hero, CTA, footer)
- Implements accessible color systems (WCAG 4.5:1 contrast)
- Generates dark mode variants automatically
- Creates full page templates (landing, about, contact)

## What This Skill Does NOT Do

- Design custom brand identities from scratch (uses pre-defined aesthetic systems)
- Create backend functionality or dynamic content
- Handle CMS integration or content management
- Implement JavaScript frameworks (React, Vue, Angular)
- Deploy websites to hosting platforms

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing stylesheets, component patterns, build configuration |
| **Conversation** | User's aesthetic preferences, target audience, brand requirements |
| **Skill References** | Design principles, color theory, typography patterns from `references/` |
| **User Guidelines** | Brand colors, existing design system, accessibility requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER'S specific context:

1. **Theme Choice**: "Which aesthetic style?" (Modern/Minimalist, Corporate/Professional, Creative/Bold, Dark/Tech, Warm/Friendly, E-commerce, SaaS/Dashboard, Portfolio - see Theme Selection Guide below)
2. **Primary Use Case**: "What's the primary page type?" (Landing page, portfolio, e-commerce, dashboard, blog, documentation)
3. **Existing Constraints**: "Any brand colors or fonts to incorporate?" (Allows customization within theme framework)
4. **Components Needed**: "Which components?" (Buttons, cards, forms, navigation, hero, CTA, footer - or "all standard components")
5. **Framework Preference**: "Output format?" (Plain HTML/CSS, Tailwind classes, or export format)

**Question Pacing**: Ask 1-2 questions at a time. Infer from context where possible.

**If User Doesn't Answer**: Use Modern/Minimalist theme, standard component set, Tailwind CSS format, and mention assumptions.

## Optional Clarifications

Ask if context suggests need:

- **Dark Mode**: "Need dark mode variant?" (Generates dark mode color palette)
- **Custom Colors**: "Want to adjust any theme colors?" (Maintains accessibility)
- **Additional Components**: "Need specialized components?" (Pricing tables, testimonials, galleries)
- **Responsive Breakpoints**: "Custom breakpoints?" (Default: mobile-first 640/768/1024/1280px)

---

## Theme Selection Guide

Choose theme based on brand personality and target audience:

### 1. Modern/Minimalist
**When to use**: SaaS products, tech startups, design agencies
**Characteristics**: Maximum whitespace, monochromatic colors (blacks/whites/grays), clean typography, simple geometric shapes
**Examples**: Apple, Stripe, Linear
**Best for**: Products emphasizing simplicity, elegance, professionalism

### 2. Corporate/Professional
**When to use**: Enterprise software, financial services, consulting firms, B2B
**Characteristics**: Trust-building blues, structured layouts, conservative typography, high contrast
**Examples**: IBM, Microsoft, Salesforce
**Best for**: Establishing credibility, professional authority

###3. Creative/Bold
**When to use**: Creative agencies, art galleries, entertainment, events
**Characteristics**: Vibrant colors, experimental layouts, unique typography, high energy
**Examples**: Awwwards winners, Dribbble showcases
**Best for**: Standing out, expressing creativity, younger audiences

### 4. Dark/Tech
**When to use**: Developer tools, gaming, tech products, modern software
**Characteristics**: Dark backgrounds, neon accents, futuristic feel, high contrast
**Examples**: GitHub Dark, Vercel, Discord
**Best for**: Technical products, developer-focused tools, modern aesthetic

### 5. Warm/Friendly
**When to use**: Community platforms, education, wellness, lifestyle brands
**Characteristics**: Soft colors, rounded corners, inviting feel, approachable typography
**Examples**: Airbnb, Etsy, Mailchimp
**Best for**: Building trust, warmth, community feeling

### 6. E-commerce/Product
**When to use**: Online stores, product showcases, retail
**Characteristics**: Product-focused layouts, conversion-optimized, clear CTAs, trust signals
**Examples**: Shopify stores, Amazon product pages
**Best for**: Driving sales, showcasing products, clear user journeys

### 7. SaaS/Dashboard
**When to use**: Software dashboards, data applications, admin panels
**Characteristics**: Data visualization-friendly, clean interfaces, information hierarchy
**Examples**: Notion, Figma, Asana
**Best for**: Complex applications, data-heavy interfaces, productivity tools

### 8. Portfolio/Personal
**When to use**: Personal websites, designer portfolios, freelancers
**Characteristics**: Personality-driven, showcase work, unique layouts, storytelling
**Examples**: Designer portfolios, personal brands
**Best for**: Individual expression, showcasing creative work

See `references/theme-variations.md` for detailed color palettes and examples.

---

## Color System (HSL-Based)

Use HSL format for scalability and dark mode support:

**Semantic Color Naming**:
- `primary`: Main brand color (CTAs, links, emphasis)
- `secondary`: Supporting color (accents, highlights)
- `accent`: Attention color (alerts, notifications)
- `background`: Page background
- `surface`: Card/container backgrounds
- `text`: Body text color
- `text-muted`: Secondary text

**Accessibility**: All text/background combinations meet WCAG 4.5:1 contrast ratio.

**Dark Mode**: Automatically generated by inverting lightness values while maintaining hue and saturation.

Example HSL notation:
```css
--color-primary: 220 90% 56%; /* hsl(220, 90%, 56%) */
```

See `references/color-systems.md` for complete palette generation and accessibility guidelines.

---

## Typography System

Use two-font pairing system:

**Font 1 (Display)**: Headlines, subheadings, navigation, buttons
- Purpose: Carries personality and brand voice
- Characteristics: Distinctive, readable at large sizes

**Font 2 (Text)**: Body copy, captions, metadata
- Purpose: Maximum readability
- Characteristics: Neutral, optimized for extended reading

**Type Scale**:
- xs: 0.75rem (12px)
- sm: 0.875rem (14px)
- base: 1rem (16px)
- lg: 1.125rem (18px)
- xl: 1.25rem (20px)
- 2xl: 1.5rem (24px)
- 3xl: 1.875rem (30px)
- 4xl: 2.25rem (36px)
- 5xl: 3rem (48px)

**Font Weights**: 300 (light), 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

See `references/typography-guide.md` for font pairing principles and web font optimization.

---

## Component Library

Standard components included:

| Component | Variants | Purpose |
|-----------|----------|---------|
| **Button** | Primary, Secondary, Outline, Ghost | CTAs, actions, navigation |
| **Card** | Product, Blog, Pricing | Content containers, features |
| **Form** | Input, Dropdown, Checkbox, Radio | Data collection, user input |
| **Navigation** | Header, Sidebar, Mobile menu | Site navigation |
| **Hero** | Centered, Split, With image | Above-fold content |
| **CTA** | Inline, Full-width, Banner | Conversion points |
| **Footer** | Simple, Multi-column, Newsletter | Site footer |

Generate all components with:
- Responsive design (mobile-first)
- Accessibility features (WCAG AA)
- Customization via theme variables

See `references/component-library.md` for detailed HTML/Tailwind examples.

---

## Tailwind CSS v4.0 Configuration

Use @theme directive for design tokens:

```css
@theme {
  /* Colors (HSL format) */
  --color-primary: 220 90% 56%;
  --color-secondary: 280 70% 60%;
  --color-accent: 340 80% 58%;

  /* Typography */
  --font-display: 'Inter', system-ui, sans-serif;
  --font-text: 'Inter', system-ui, sans-serif;

  /* Spacing (based on 0.25rem = 4px) */
  --spacing-*: 0 | 1 | 2 | 4 | 6 | 8 | 10 | 12 | 16 | 20 | 24 | 32 | 40 | 48 | 64;

  /* Border radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;
}
```

See `references/tailwind-config.md` for complete configuration patterns and custom utilities.

---

## Responsive Design (Mobile-First)

Default breakpoints:
- sm: 640px (landscape phones)
- md: 768px (tablets)
- lg: 1024px (laptops)
- xl: 1280px (desktops)
- 2xl: 1536px (large desktops)

**Mobile-First Approach**: Design for mobile, enhance for larger screens.

**Touch Targets**: Minimum 44x44px for interactive elements.

**Flexible Layouts**: Use `flex` and `grid` with relative units.

See `references/responsive-patterns.md` for detailed patterns and best practices.

---

## Official Documentation

For latest patterns and updates, refer to:

| Resource | URL | Use For |
|----------|-----|---------|
| Tailwind CSS v4.0 | https://tailwindcss.com/blog/tailwindcss-v4 | @theme directive, design tokens |
| Tailwind Docs | https://tailwindcss.com/docs | Utility classes, configuration |
| WCAG Guidelines | https://www.w3.org/WAI/WCAG22/quickref/ | Accessibility standards |
| Google Fonts | https://fonts.google.com/ | Web font library |
| MDN Web Docs | https://developer.mozilla.org/en-US/docs/Web | HTML/CSS reference |

**For Unlisted Patterns**: When encountering design patterns or components not covered in these references, fetch the latest documentation from the URLs above.

---

## Standards to Follow

### Must Follow
- [ ] Use HSL color format for all theme colors
- [ ] Ensure 4.5:1 contrast ratio for all text (WCAG AA)
- [ ] Implement mobile-first responsive design
- [ ] Use semantic HTML elements (header, nav, main, footer)
- [ ] Include ARIA labels for interactive elements
- [ ] Provide dark mode variants for themes
- [ ] Use Tailwind utility classes (avoid custom CSS when possible)
- [ ] Include focus states for keyboard navigation
- [ ] Test on multiple screen sizes (mobile, tablet, desktop)
- [ ] Optimize font loading (font-display: swap)
- [ ] Include alt text for all images
- [ ] Use relative units (rem, em, %) over absolute (px)

### Must Avoid
- [ ] Don't use fixed pixel widths for containers
- [ ] Don't rely on color alone to convey information
- [ ] Don't create inaccessible color combinations
- [ ] Don't ignore keyboard navigation
- [ ] Don't use tiny touch targets (<44x44px)
- [ ] Don't load unnecessary font weights
- [ ] Don't use deprecated HTML elements
- [ ] Don't hardcode breakpoint values in components
- [ ] Don't create theme-specific CSS (use design tokens)
- [ ] Don't skip responsive testing

See `references/accessibility.md` for detailed accessibility guidelines.

---

## Security Considerations

When generating themes and components, follow these security practices:

### Input Sanitization
- **User-provided content**: Sanitize all user-provided text (names, descriptions, custom colors) before inserting into HTML
- **Color values**: Validate HSL/hex color input to prevent CSS injection (only accept numeric values and valid formats)
- **File names**: Sanitize file names and paths to prevent directory traversal attacks
- **Script parameters**: Validate all command-line arguments before processing

### XSS Prevention
- **Escape HTML entities**: When generating HTML with user content, escape `<`, `>`, `&`, `"`, and `'`
- **Avoid inline JavaScript**: Never generate inline JavaScript with user input
- **Content Security Policy**: Recommend CSP headers for generated sites
- **Alt text**: Sanitize image alt text attributes

### Safe Defaults
- **Content placeholders**: Use safe placeholder text in generated templates
- **External resources**: Use HTTPS for all external fonts and CDN resources
- **Font loading**: Use `font-display: swap` to prevent FOIT/FOUT attacks

### Generated Code Safety
- **No eval()**: Never generate JavaScript code using eval() or Function()
- **Validate URLs**: Check that links and image sources are valid URLs
- **ARIA attributes**: Validate ARIA attribute values to prevent injection

**Example: Safe color validation**
```python
import re

def validate_hsl_color(hsl_string):
    """Validate HSL color format to prevent injection."""
    pattern = r'^\d{1,3}\s+\d{1,3}%\s+\d{1,3}%$'
    if not re.match(pattern, hsl_string):
        raise ValueError("Invalid HSL format")

    h, s, l = map(lambda x: int(x.rstrip('%')), hsl_string.split())
    if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= l <= 100):
        raise ValueError("HSL values out of range")

    return True
```

---

## Error Handling

Handle common errors gracefully when generating themes:

### Script Execution Errors
- **Missing arguments**: Provide clear error messages with usage examples
- **Invalid input**: Validate inputs before processing and show specific error messages
- **File system errors**: Handle permission errors, disk full, invalid paths
- **Dependency errors**: Check for required tools/libraries and provide installation guidance

### Generation Failures
- **Invalid color combinations**: Check accessibility contrast before generating
- **Font loading failures**: Provide fallback fonts in generated CSS
- **Asset not found**: Verify template files exist before reading
- **Malformed templates**: Validate JSON/CSS syntax before writing files

### Recovery Strategies
- **Partial generation**: If one component fails, continue with others and report failure
- **Rollback**: Provide option to revert to previous working state
- **Validation**: Run validation checks before finalizing output
- **User feedback**: Show progress and clear error messages with resolution steps

### Common Edge Cases
- **Very long text**: Buttons/headings with 100+ characters → Use text truncation (text-ellipsis) or word-wrap
- **Missing fonts**: Font fails to load → Provide fallback fonts in font stack (e.g., Arial, sans-serif)
- **Extreme viewports**: Very narrow (<320px) or very wide (>2560px) → Test and add container max-widths
- **Tall viewports**: Very short heights (<400px) → Avoid vh units for critical content, use min-height
- **High contrast mode**: User OS forces colors → Use semantic HTML and test with Windows High Contrast
- **Font scaling**: Browser zoom >200% → Test with large font sizes (16px base minimum)
- **No JavaScript**: Users with JS disabled → Ensure core functionality works without JS
- **Slow connections**: Large images/fonts → Optimize assets, use font-display: swap

**Example: Edge handling in CSS**
```css
/* Handle long text gracefully */
.button {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Provide comprehensive font fallbacks */
:root {
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

**Example: Error handling in scripts**
```python
try:
    theme_css = generate_theme_css(theme_config, args.dark_mode)
    output_file.write_text(theme_css)
    print(f"✅ Created {output_file}")
except PermissionError:
    print(f"❌ Error: No write permission for {output_file}")
    print("   Solution: Check file permissions or choose different output directory")
    sys.exit(1)
except ValueError as e:
    print(f"❌ Error: Invalid theme configuration - {e}")
    print("   Solution: Check theme config values are valid")
    sys.exit(1)
```

---

## Testing & Verification

Verify generated themes and components work correctly:

### Visual Testing
- **Browser testing**: Open generated HTML in Chrome, Firefox, Safari
- **Responsive testing**: Test at breakpoints (320px, 768px, 1024px, 1440px)
- **Dark mode**: Toggle dark mode and verify colors remain accessible
- **Color contrast**: Use browser DevTools or WebAIM contrast checker to verify 4.5:1 ratio
- **Font rendering**: Verify fonts load correctly and fallbacks work

### Functional Testing
- **Interactive elements**: Test all buttons, forms, links for proper behavior
- **Keyboard navigation**: Tab through interactive elements, verify focus states visible
- **Touch targets**: Verify buttons/links are at least 44x44px on mobile
- **Form validation**: Test form inputs accept valid data and reject invalid data
- **Navigation**: Verify all navigation links work and mobile menu functions

### Accessibility Testing
- **Screen reader**: Test with NVDA/JAWS (Windows) or VoiceOver (Mac)
- **Keyboard only**: Navigate entire page using only keyboard
- **ARIA validation**: Use axe DevTools or WAVE to check ARIA implementation
- **Semantic HTML**: Verify proper heading hierarchy (h1 → h2 → h3)
- **Alt text**: Check all images have descriptive alt attributes

### Code Quality
- **HTML validation**: Run through W3C HTML validator
- **CSS validation**: Run through W3C CSS validator
- **Lighthouse audit**: Run Chrome Lighthouse for performance/accessibility scores
- **Console errors**: Check browser console for JavaScript/CSS errors
- **Broken links**: Verify no 404s for images, fonts, or other assets

### Cross-browser Compatibility
- **Modern browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile browsers**: iOS Safari, Chrome Mobile, Samsung Internet
- **Vendor prefixes**: Check CSS autoprefixer for older browser support

**Testing Checklist (Quick)**
```bash
# 1. Visual test in browser
open index.html

# 2. Validate HTML
curl -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @index.html \
  https://validator.w3.org/nu/?out=text

# 3. Check contrast (using npm package)
npx @cypress/accessibility-checker index.html

# 4. Lighthouse audit
npx lighthouse index.html --view
```

---

## Output Checklist

Before delivering, verify:

**Theme Configuration**
- [ ] Color palette defined with HSL values
- [ ] All colors meet accessibility contrast requirements
- [ ] Dark mode variant generated (if requested)
- [ ] Typography pairing selected and configured
- [ ] Tailwind @theme configuration created

**Components**
- [ ] All requested components generated
- [ ] Components use theme design tokens
- [ ] Responsive behavior implemented
- [ ] Accessibility attributes included (ARIA, roles)
- [ ] Focus states and hover effects defined

**Pages**
- [ ] Page templates created for requested types
- [ ] Mobile-first responsive layout
- [ ] Semantic HTML structure
- [ ] Meta tags and SEO basics included

**Code Quality**
- [ ] Tailwind utility classes used consistently
- [ ] No inline styles (use utilities or theme tokens)
- [ ] Clean, readable HTML structure
- [ ] Comments for complex sections

**Accessibility**
- [ ] WCAG AA contrast ratios verified
- [ ] Keyboard navigation tested
- [ ] Screen reader compatibility
- [ ] Alt text for images
- [ ] ARIA labels for interactive elements

**Documentation**
- [ ] Theme customization instructions included
- [ ] Component usage examples provided
- [ ] Responsive breakpoint guidance
- [ ] Font loading instructions

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/theme_generator.py` | Generate complete theme boilerplate with chosen aesthetic |
| `scripts/component_builder.py` | Create individual components in specified theme |
| `scripts/palette_generator.py` | Generate accessible color palettes with dark mode variants |

Run scripts with `--help` for usage instructions.

### Script Dependencies

**Required**:
- Python 3.7+ (standard library only, no external packages required)

**Optional** (for testing/validation):
- Node.js 14+ (for Lighthouse, HTML validator)
- Modern web browser (Chrome, Firefox, Safari)

All Python scripts use only standard library modules:
- `argparse` - Command-line argument parsing
- `json` - JSON configuration handling
- `pathlib` - Cross-platform file path operations
- `re` - Regular expression validation
- `sys` - System-specific parameters
- `typing` - Type hints

**Installation check**:
```bash
# Verify Python version
python3 --version  # Should be 3.7 or higher

# Test scripts run without errors
python3 scripts/theme_generator.py --help
python3 scripts/component_builder.py --help
python3 scripts/palette_generator.py --help
```

---

## Assets

| Directory | Contents |
|-----------|----------|
| `assets/theme-configs/` | JSON configuration files for all 8 themes |
| `assets/components/` | HTML/Tailwind templates for standard components |
| `assets/templates/` | Full page templates (landing, about, contact) |
| `assets/fonts/` | Font pairing recommendations with Google Fonts links |

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/theme-variations.md` | Detailed breakdown of all 8 themes with color palettes and examples |
| `references/color-systems.md` | Color theory, HSL system, accessibility, dark mode implementation |
| `references/typography-guide.md` | Font pairing principles, type scale, web font optimization |
| `references/component-library.md` | Detailed component patterns with HTML/Tailwind code examples |
| `references/tailwind-config.md` | Tailwind CSS v4.0 @theme patterns and design token examples |
| `references/responsive-patterns.md` | Mobile-first approach, breakpoints, flexible layouts |
| `references/accessibility.md` | WCAG guidelines, keyboard navigation, screen readers |
| `references/design-principles.md` | Design theory for each theme type, when to use what |

**Finding Specific Topics**: All reference files include table of contents. For quick searches, use these patterns:

```bash
# Color palette examples
grep -r "hsl(\|--color-" references/

# Component code
grep -r "<button\|<card\|<form" references/

# Accessibility patterns
grep -r "aria-\|role=\|contrast" references/

# Responsive patterns
grep -r "@media\|sm:\|md:\|lg:" references/

# Typography
grep -r "font-\|text-\|tracking-" references/
```
