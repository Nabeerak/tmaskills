# Testing & Verification

Verify generated themes and components work correctly.

## Table of Contents

1. [Visual Testing](#visual-testing)
2. [Functional Testing](#functional-testing)
3. [Accessibility Testing](#accessibility-testing)
4. [Code Quality](#code-quality)
5. [Cross-browser Compatibility](#cross-browser-compatibility)
6. [Quick Testing Checklist](#quick-testing-checklist)
7. [Automated Testing Commands](#automated-testing-commands)

---

## Visual Testing

### Browser Testing
Open generated HTML in multiple browsers:

```bash
# macOS
open index.html                    # Default browser
open -a "Google Chrome" index.html
open -a "Firefox" index.html
open -a "Safari" index.html

# Linux
xdg-open index.html
google-chrome index.html
firefox index.html

# Windows
start index.html
```

### Responsive Testing
Test at standard breakpoints:

| Breakpoint | Width | Device Type |
|------------|-------|-------------|
| Mobile | 320px | Small phones |
| Mobile | 375px | iPhone SE/8 |
| Mobile | 414px | iPhone Plus |
| Tablet | 768px | iPad portrait |
| Laptop | 1024px | iPad landscape / small laptop |
| Desktop | 1280px | Standard desktop |
| Large | 1440px | Large desktop |
| XL | 1920px | Full HD monitor |

**Chrome DevTools responsive mode:**
1. Open DevTools (F12)
2. Click device toolbar icon (Ctrl+Shift+M)
3. Select device or enter custom dimensions

### Dark Mode Testing
Toggle dark mode and verify colors remain accessible:

```css
/* Test with prefers-color-scheme media query */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: 220 20% 10%;
    --color-text: 0 0% 95%;
  }
}
```

**Browser testing:**
- Chrome: DevTools > Rendering > Emulate CSS media feature prefers-color-scheme
- Firefox: about:config > ui.systemUsesDarkTheme
- macOS: System Preferences > General > Appearance

### Color Contrast Testing
Verify 4.5:1 ratio for WCAG AA compliance:

**Tools:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Contrast Ratio](https://contrast-ratio.com/)
- Chrome DevTools: Inspect element > Styles > Click color swatch > Contrast ratio shown

### Font Rendering Testing
Verify fonts load correctly and fallbacks work:

1. Open Network tab in DevTools
2. Filter by "Font"
3. Verify font files load with 200 status
4. Test with fonts blocked (DevTools > Network > Block request URL)

---

## Functional Testing

### Interactive Elements
Test all buttons, forms, links for proper behavior:

| Element | Test |
|---------|------|
| Buttons | Click, hover, focus states work |
| Links | Navigate to correct destination |
| Forms | Submit, validation, error states |
| Dropdowns | Open, select, close properly |
| Modals | Open, close, escape key works |
| Mobile menu | Toggle, navigation works |

### Keyboard Navigation
Tab through interactive elements:

```
Tab          → Move to next focusable element
Shift+Tab    → Move to previous element
Enter/Space  → Activate buttons/links
Escape       → Close modals/dropdowns
Arrow keys   → Navigate within components
```

**Check:**
- [ ] All interactive elements reachable via Tab
- [ ] Focus order follows visual order
- [ ] Focus indicator clearly visible
- [ ] No keyboard traps

### Touch Targets
Verify minimum 44x44px on mobile:

```css
/* Ensure adequate touch targets */
button, a, input, select {
  min-height: 44px;
  min-width: 44px;
}

/* Add padding for small elements */
.icon-button {
  padding: 12px;
}
```

### Form Validation
Test inputs accept valid data and reject invalid:

| Input Type | Valid Test | Invalid Test |
|------------|------------|--------------|
| Email | user@example.com | not-an-email |
| Phone | +1-555-123-4567 | abc123 |
| Required | Any value | Empty |
| Number | 42 | forty-two |
| URL | https://example.com | not-a-url |

---

## Accessibility Testing

### Screen Reader Testing
Test with assistive technologies:

| OS | Screen Reader | Command |
|----|---------------|---------|
| Windows | NVDA | Free download from nvaccess.org |
| Windows | JAWS | Commercial |
| macOS | VoiceOver | Cmd+F5 to enable |
| Linux | Orca | Pre-installed on GNOME |
| iOS | VoiceOver | Settings > Accessibility |
| Android | TalkBack | Settings > Accessibility |

### Keyboard-Only Navigation
Navigate entire page using only keyboard:

1. Unplug mouse / disable trackpad
2. Navigate through all content with Tab
3. Verify all functionality accessible
4. Check focus never gets trapped

### ARIA Validation
Use automated tools to check ARIA implementation:

```bash
# axe DevTools (Chrome extension)
# Install from Chrome Web Store

# WAVE (Chrome extension)
# Install from Chrome Web Store

# CLI tools
npx axe-core index.html
npx pa11y index.html
```

### Semantic HTML Verification
Check proper heading hierarchy:

```
h1 (one per page)
├── h2
│   ├── h3
│   │   └── h4
│   └── h3
└── h2
    └── h3
```

**Tools:**
- HeadingsMap browser extension
- W3C HTML validator

### Alt Text Audit
Check all images have descriptive alt attributes:

```bash
# Find images without alt
grep -r "<img" . | grep -v "alt="

# Find empty alt (decorative images should use alt="")
grep -r 'alt=""' .
```

---

## Code Quality

### HTML Validation
Run through W3C HTML validator:

```bash
# Online validator
curl -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @index.html \
  https://validator.w3.org/nu/?out=text

# NPM package
npx html-validate index.html
```

### CSS Validation
Run through W3C CSS validator:

```bash
# Online validator
# Upload file to https://jigsaw.w3.org/css-validator/

# NPM package
npx stylelint "**/*.css"
```

### Lighthouse Audit
Run Chrome Lighthouse for comprehensive scores:

```bash
# CLI
npx lighthouse index.html --output html --output-path report.html

# Chrome DevTools
# 1. Open DevTools (F12)
# 2. Go to Lighthouse tab
# 3. Select categories and click "Analyze page load"
```

**Target Scores:**
| Category | Target |
|----------|--------|
| Performance | >90 |
| Accessibility | >90 |
| Best Practices | >90 |
| SEO | >90 |

### Console Errors
Check browser console for JavaScript/CSS errors:

1. Open DevTools Console (F12 > Console)
2. Filter by Errors
3. Fix any red error messages
4. Check for yellow warnings

### Broken Links
Verify no 404s for images, fonts, or assets:

```bash
# NPM package
npx broken-link-checker http://localhost:8000

# Python
python -m http.server 8000  # Serve files
# Then check network tab for 404s
```

---

## Cross-browser Compatibility

### Modern Browsers
Test on latest versions:

| Browser | Engine | Test Priority |
|---------|--------|---------------|
| Chrome | Blink | High |
| Firefox | Gecko | High |
| Safari | WebKit | High |
| Edge | Blink | Medium |

### Mobile Browsers
Test on mobile devices:

| Browser | Platform | Test Priority |
|---------|----------|---------------|
| Safari | iOS | High |
| Chrome | Android | High |
| Samsung Internet | Android | Medium |
| Firefox | Android | Low |

### Vendor Prefixes
Check CSS autoprefixer for older browser support:

```bash
# Check what prefixes are needed
npx autoprefixer --info

# Process CSS with autoprefixer
npx postcss style.css --use autoprefixer -o style.prefixed.css
```

---

## Quick Testing Checklist

### Before Delivery
- [ ] Opens correctly in Chrome, Firefox, Safari
- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] Dark mode colors accessible (if applicable)
- [ ] All buttons/links clickable
- [ ] Tab navigation works
- [ ] Focus states visible
- [ ] Touch targets ≥44px on mobile
- [ ] No console errors
- [ ] Images have alt text
- [ ] Contrast ratio ≥4.5:1
- [ ] HTML validates
- [ ] Lighthouse accessibility ≥90

---

## Automated Testing Commands

```bash
# Quick validation suite
# 1. Start local server
python3 -m http.server 8000 &

# 2. Run HTML validation
curl -s -H "Content-Type: text/html" \
  --data-binary @index.html \
  "https://validator.w3.org/nu/?out=text"

# 3. Run accessibility check
npx pa11y http://localhost:8000

# 4. Run Lighthouse
npx lighthouse http://localhost:8000 \
  --only-categories=accessibility,best-practices \
  --output=json --output-path=./lighthouse.json

# 5. Check for broken links
npx broken-link-checker http://localhost:8000 --recursive

# 6. Stop server
kill %1
```
