# Accessibility Reference (WCAG 2.2)

Complete guide to building accessible web themes that meet WCAG AA standards.

## Table of Contents

1. [WCAG Overview](#wcag-overview)
2. [Color and Contrast](#color-and-contrast)
3. [Keyboard Navigation](#keyboard-navigation)
4. [Screen Readers](#screen-readers)
5. [Focus Management](#focus-management)
6. [Semantic HTML](#semantic-html)
7. [ARIA Labels and Roles](#aria-labels-and-roles)
8. [Forms](#forms)
9. [Images](#images)
10. [Interactive Elements](#interactive-elements)
11. [Testing](#testing)

---

## WCAG Overview

### Conformance Levels

- **Level A**: Minimum accessibility (basic requirements)
- **Level AA**: Standard accessibility (recommended target)
- **Level AAA**: Enhanced accessibility (ideal but not always achievable)

**Target for web themes**: WCAG 2.2 Level AA

### Four Principles (POUR)

1. **Perceivable**: Information must be presentable to users in ways they can perceive
2. **Operable**: User interface components must be operable
3. **Understandable**: Information and UI operation must be understandable
4. **Robust**: Content must be robust enough for interpretation by assistive technologies

---

## Color and Contrast

### Contrast Ratios

**WCAG AA Requirements:**
- Normal text (< 18pt or < 14pt bold): **4.5:1** minimum
- Large text (≥ 18pt or ≥ 14pt bold): **3:1** minimum
- UI components and graphics: **3:1** minimum

**WCAG AAA Requirements:**
- Normal text: **7:1** minimum
- Large text: **4.5:1** minimum

### Calculating Contrast

Use tools like:
- WebAIM Contrast Checker
- Chrome DevTools Color Picker
- WCAG Color Contrast Checker browser extension

### Color Examples

```css
/* ✅ Good: 4.65:1 ratio (passes AA) */
--color-text: hsl(0, 0%, 10%);        /* #1a1a1a */
--color-background: hsl(0, 0%, 100%); /* #ffffff */

/* ✅ Good: 7.0:1 ratio (passes AAA) */
--color-text: hsl(0, 0%, 0%);         /* #000000 */
--color-background: hsl(0, 0%, 100%); /* #ffffff */

/* ❌ Bad: 2.5:1 ratio (fails AA) */
--color-text: hsl(0, 0%, 60%);        /* #999999 */
--color-background: hsl(0, 0%, 100%); /* #ffffff */

/* ✅ Good: Primary button contrast */
--color-primary: hsl(220, 90%, 45%);  /* Dark enough for white text */
/* White text on this background = 4.8:1 ratio */

/* ❌ Bad: Primary button contrast */
--color-primary: hsl(220, 90%, 70%);  /* Too light for white text */
/* White text on this background = 2.1:1 ratio (fails) */
```

### Don't Rely on Color Alone

```html
<!-- ❌ Bad: Color-only indication -->
<p style="color: red;">Error: Invalid input</p>

<!-- ✅ Good: Color + icon + text -->
<p class="text-red-600 flex items-center gap-2">
  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
  </svg>
  <span><strong>Error:</strong> Invalid input</span>
</p>
```

### Link Color Contrast

Links must have:
- 4.5:1 contrast with background
- 3:1 contrast with surrounding text (if not underlined)

```html
<!-- ✅ Good: Underlined link (no contrast requirement with surrounding text) -->
<p class="text-gray-900">
  Read our <a href="#" class="text-blue-600 underline">privacy policy</a> for details.
</p>

<!-- ✅ Good: Non-underlined link with sufficient contrast -->
<p class="text-gray-700">
  Read our <a href="#" class="text-blue-900 hover:underline">privacy policy</a> for details.
</p>
<!-- Blue-900 vs Gray-700 = 3.5:1 ratio (passes) -->
```

---

## Keyboard Navigation

### Tab Order

Ensure logical tab order matches visual flow:

```html
<!-- ✅ Good: Logical tab order -->
<form>
  <input type="text" name="name" tabindex="1">
  <input type="email" name="email" tabindex="2">
  <button type="submit" tabindex="3">Submit</button>
</form>

<!-- ⚠️ Better: Let browser handle tab order naturally -->
<form>
  <input type="text" name="name">
  <input type="email" name="email">
  <button type="submit">Submit</button>
</form>
```

**Avoid**: `tabindex` > 0 (disrupts natural tab order)

### Skip Links

Allow users to skip repetitive content:

```html
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-white focus:rounded">
  Skip to main content
</a>

<header>
  <!-- Navigation -->
</header>

<main id="main-content">
  <!-- Main content -->
</main>
```

CSS for screen-reader-only (sr-only):
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.focus\:not-sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: 0.5rem 1rem;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Keyboard Shortcuts

Document and ensure keyboard accessibility:

- **Tab**: Move focus forward
- **Shift + Tab**: Move focus backward
- **Enter**: Activate buttons and links
- **Space**: Activate buttons, checkboxes
- **Arrow keys**: Navigate within components (dropdowns, tabs)
- **Escape**: Close modals, dropdowns

### Interactive Element Keyboard Support

```html
<!-- Button: Enter and Space should activate -->
<button type="button" onclick="handleClick()">
  Click Me
</button>

<!-- Custom interactive div (avoid, use button instead) -->
<div
  role="button"
  tabindex="0"
  onclick="handleClick()"
  onkeydown="if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); handleClick(); }"
  class="cursor-pointer"
>
  Click Me
</div>
```

**Best Practice**: Use semantic HTML (`<button>`, `<a>`) instead of div with role.

---

## Screen Readers

### Screen Reader Only Text

Provide additional context for screen reader users:

```html
<!-- Button with icon only -->
<button class="p-2" aria-label="Close dialog">
  <svg class="w-6 h-6" aria-hidden="true">
    <!-- X icon -->
  </svg>
  <span class="sr-only">Close</span>
</button>

<!-- Link with "Read more" -->
<article>
  <h3>Article Title</h3>
  <p>Article excerpt...</p>
  <a href="/article">
    Read more
    <span class="sr-only">about Article Title</span>
  </a>
</article>
```

### Hiding Decorative Content

```html
<!-- Decorative icon (hidden from screen readers) -->
<button>
  <svg aria-hidden="true" class="w-5 h-5"><!-- Icon --></svg>
  Submit
</button>

<!-- Decorative image -->
<img src="decorative-pattern.svg" alt="" role="presentation">
```

### Live Regions

Announce dynamic content changes:

```html
<!-- Alert messages -->
<div role="alert" aria-live="assertive" aria-atomic="true">
  Error: Please fill out all required fields.
</div>

<!-- Status updates (less urgent) -->
<div role="status" aria-live="polite" aria-atomic="true">
  Form saved successfully.
</div>

<!-- Loading indicator -->
<div aria-live="polite" aria-busy="true">
  Loading content...
</div>
```

**aria-live values:**
- `off`: No announcements
- `polite`: Announce when user is idle
- `assertive`: Announce immediately (interrupts)

---

## Focus Management

### Focus Styles

Always provide visible focus indicators:

```css
/* ❌ Bad: Removing focus outline */
button:focus {
  outline: none;
}

/* ✅ Good: Custom focus style */
button:focus {
  outline: 2px solid hsl(220, 90%, 56%);
  outline-offset: 2px;
}

/* ✅ Better: Using Tailwind utilities */
.btn {
  @apply focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2;
}
```

**Tailwind focus utilities:**
```html
<button class="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
  Button
</button>

<a href="#" class="focus:underline focus:outline-none focus:ring-2 focus:ring-primary focus:rounded">
  Link
</a>
```

### Focus Trap (Modals)

Trap focus within modals:

```html
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="modal-content">
    <h2 id="modal-title">Modal Title</h2>
    <p>Modal content...</p>
    <button onclick="closeModal()">Close</button>
  </div>
</div>
```

JavaScript (conceptual):
```javascript
// When modal opens:
// 1. Save currently focused element
// 2. Move focus to first focusable element in modal
// 3. Trap Tab key to cycle within modal
// 4. Trap Escape key to close modal
// 5. Restore focus to saved element when modal closes
```

### Focus Management After Actions

```javascript
// After deleting an item, focus the next item or parent
deleteItem(itemId);
document.getElementById('next-item').focus();

// After closing a dialog, restore focus
const previouslyFocused = document.activeElement;
openDialog();
// ... later ...
closeDialog();
previouslyFocused.focus();
```

---

## Semantic HTML

### Use Proper HTML Elements

```html
<!-- ✅ Good: Semantic HTML -->
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Article content...</p>
  </article>
</main>

<aside>
  <h2>Related Articles</h2>
  <ul>
    <li><a href="#">Article 1</a></li>
  </ul>
</aside>

<footer>
  <p>&copy; 2024 Company</p>
</footer>

<!-- ❌ Bad: Generic divs -->
<div class="header">
  <div class="nav">
    <div><a href="/">Home</a></div>
    <div><a href="/about">About</a></div>
  </div>
</div>
```

### Heading Hierarchy

Maintain logical heading structure:

```html
<!-- ✅ Good: Logical hierarchy -->
<h1>Page Title</h1>
  <h2>Section 1</h2>
    <h3>Subsection 1.1</h3>
    <h3>Subsection 1.2</h3>
  <h2>Section 2</h2>
    <h3>Subsection 2.1</h3>

<!-- ❌ Bad: Skipping levels -->
<h1>Page Title</h1>
  <h3>Subsection</h3> <!-- Skipped h2 -->
  <h2>Section</h2>
```

**Rule**: Don't skip heading levels. Use CSS for styling, not HTML for sizing.

### Lists

```html
<!-- Unordered list -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>

<!-- Ordered list -->
<ol>
  <li>Step 1</li>
  <li>Step 2</li>
</ol>

<!-- Description list -->
<dl>
  <dt>Term 1</dt>
  <dd>Definition 1</dd>
  <dt>Term 2</dt>
  <dd>Definition 2</dd>
</dl>
```

### Buttons vs Links

```html
<!-- ✅ Button: Performs an action -->
<button onclick="submitForm()">Submit</button>
<button onclick="toggleMenu()">Menu</button>

<!-- ✅ Link: Navigates to a URL -->
<a href="/about">About Us</a>
<a href="#section">Jump to Section</a>

<!-- ❌ Wrong: Link styled as button performing action -->
<a href="#" onclick="submitForm()">Submit</a>

<!-- ❌ Wrong: Button navigating to URL -->
<button onclick="location.href='/about'">About</button>
```

---

## ARIA Labels and Roles

### ARIA Labels

Provide accessible names for elements:

```html
<!-- Button with text (no aria-label needed) -->
<button>Submit</button>

<!-- Button with icon only (aria-label required) -->
<button aria-label="Close dialog">
  <svg><!-- X icon --></svg>
</button>

<!-- Link with more context -->
<a href="/article" aria-label="Read more about Introduction to Web Accessibility">
  Read more
</a>

<!-- Search form -->
<form role="search" aria-label="Site search">
  <input type="search" aria-label="Search terms">
  <button type="submit">Search</button>
</form>
```

### ARIA Roles

Use when semantic HTML isn't sufficient:

```html
<!-- Navigation -->
<nav role="navigation" aria-label="Main navigation">
  <ul><!-- Links --></ul>
</nav>

<!-- Search -->
<form role="search">
  <input type="search" aria-label="Search">
</form>

<!-- Banner (for header) -->
<header role="banner">
  <h1>Site Title</h1>
</header>

<!-- Main content -->
<main role="main">
  <article>Content</article>
</main>

<!-- Complementary content (sidebar) -->
<aside role="complementary">
  <h2>Related</h2>
</aside>

<!-- Content info (footer) -->
<footer role="contentinfo">
  <p>&copy; 2024</p>
</footer>
```

**Note**: Most semantic HTML elements have implicit roles. Only add role attribute when needed.

### ARIA States and Properties

```html
<!-- Expanded/collapsed state -->
<button
  aria-expanded="false"
  aria-controls="menu"
  onclick="toggleMenu()"
>
  Menu
</button>
<div id="menu" hidden>
  <!-- Menu items -->
</div>

<!-- Current page in navigation -->
<nav>
  <a href="/" aria-current="page">Home</a>
  <a href="/about">About</a>
</nav>

<!-- Required field -->
<input type="text" aria-required="true" required>

<!-- Invalid field -->
<input
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
>
<p id="email-error">Please enter a valid email address</p>

<!-- Loading state -->
<div aria-busy="true" aria-live="polite">
  Loading content...
</div>
```

---

## Forms

### Labels

Always associate labels with inputs:

```html
<!-- ✅ Good: Explicit label -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email">

<!-- ✅ Good: Implicit label -->
<label>
  Email Address
  <input type="email" name="email">
</label>

<!-- ❌ Bad: No label association -->
<label>Email Address</label>
<input type="email" name="email">
```

### Required Fields

Indicate required fields clearly:

```html
<label for="name">
  Name <span aria-label="required">*</span>
</label>
<input
  type="text"
  id="name"
  name="name"
  required
  aria-required="true"
>

<!-- Alternative: Explicit text -->
<label for="email">
  Email Address <span class="text-red-600">(required)</span>
</label>
<input type="email" id="email" required aria-required="true">
```

### Error Messages

Associate errors with inputs:

```html
<label for="username">Username</label>
<input
  type="text"
  id="username"
  name="username"
  aria-invalid="true"
  aria-describedby="username-error"
>
<p id="username-error" class="text-red-600" role="alert">
  Username must be at least 3 characters
</p>
```

### Field Groups

```html
<fieldset>
  <legend>Choose your plan</legend>
  <label>
    <input type="radio" name="plan" value="basic">
    Basic - $9/month
  </label>
  <label>
    <input type="radio" name="plan" value="pro">
    Pro - $29/month
  </label>
</fieldset>
```

### Help Text

```html
<label for="password">Password</label>
<input
  type="password"
  id="password"
  aria-describedby="password-help"
>
<p id="password-help" class="text-sm text-gray-600">
  Must be at least 8 characters with one uppercase letter and one number
</p>
```

---

## Images

### Alt Text

```html
<!-- ✅ Informative image -->
<img src="chart.png" alt="Bar chart showing 50% increase in sales from 2023 to 2024">

<!-- ✅ Decorative image -->
<img src="decorative-pattern.svg" alt="" role="presentation">

<!-- ✅ Image in link (describe destination) -->
<a href="/products">
  <img src="products-icon.png" alt="View all products">
</a>

<!-- ✅ Complex image with long description -->
<img
  src="complex-diagram.png"
  alt="System architecture diagram"
  aria-describedby="diagram-description"
>
<div id="diagram-description" class="sr-only">
  Detailed description of the system architecture showing...
</div>

<!-- ❌ Bad: Generic alt text -->
<img src="photo.jpg" alt="image">

<!-- ❌ Bad: Filename as alt -->
<img src="hero_banner_2024.png" alt="hero_banner_2024.png">
```

### Alt Text Guidelines

- **Informative images**: Describe the content and function
- **Decorative images**: Use empty alt (`alt=""`)
- **Functional images**: Describe the action/destination
- **Complex images**: Use aria-describedby for long descriptions
- **Text in images**: Include the text in alt attribute

---

## Interactive Elements

### Buttons

```html
<!-- Standard button -->
<button type="button" onclick="handleClick()">
  Click Me
</button>

<!-- Submit button -->
<button type="submit">
  Submit Form
</button>

<!-- Button with icon and text -->
<button type="button" class="flex items-center gap-2">
  <svg aria-hidden="true" class="w-5 h-5"><!-- Icon --></svg>
  Delete
</button>

<!-- Icon-only button -->
<button type="button" aria-label="Delete item">
  <svg aria-hidden="true" class="w-5 h-5"><!-- Icon --></svg>
</button>

<!-- Disabled button -->
<button type="button" disabled aria-disabled="true">
  Cannot Click
</button>
```

### Links

```html
<!-- Standard link -->
<a href="/about">About Us</a>

<!-- Link opening in new tab -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  External Link
  <span class="sr-only">(opens in new tab)</span>
</a>

<!-- Download link -->
<a href="/document.pdf" download aria-label="Download PDF document">
  Download
</a>
```

### Tooltips

```html
<button
  type="button"
  aria-label="Help"
  aria-describedby="help-tooltip"
>
  ?
</button>
<div id="help-tooltip" role="tooltip" class="hidden">
  This feature allows you to...
</div>
```

### Dropdowns/Select

```html
<label for="country">Country</label>
<select id="country" name="country" aria-label="Select your country">
  <option value="">Choose a country</option>
  <option value="us">United States</option>
  <option value="uk">United Kingdom</option>
  <option value="ca">Canada</option>
</select>
```

### Custom Dropdowns

```html
<div class="relative">
  <button
    type="button"
    aria-haspopup="listbox"
    aria-expanded="false"
    aria-labelledby="dropdown-label"
    id="dropdown-button"
  >
    Choose option
  </button>
  <ul
    role="listbox"
    aria-labelledby="dropdown-label"
    hidden
  >
    <li role="option" tabindex="0">Option 1</li>
    <li role="option" tabindex="0">Option 2</li>
  </ul>
</div>
```

---

## Testing

### Automated Testing Tools

**Browser Extensions:**
- axe DevTools (Chrome, Firefox)
- WAVE (Chrome, Firefox, Edge)
- Lighthouse (Chrome DevTools)

**Command Line:**
- pa11y
- axe-core

### Manual Testing

1. **Keyboard Navigation**
   - Unplug mouse
   - Navigate entire site with Tab, Enter, Arrow keys
   - Verify all interactive elements are reachable and operable

2. **Screen Reader**
   - **Windows**: NVDA (free) or JAWS
   - **Mac**: VoiceOver (built-in)
   - **Mobile**: TalkBack (Android), VoiceOver (iOS)

3. **Zoom**
   - Test at 200% zoom
   - Verify no horizontal scrolling
   - Check all content still accessible

4. **Color Contrast**
   - Use browser DevTools color picker
   - Test all text/background combinations
   - Verify 4.5:1 for normal text, 3:1 for large text

### Testing Checklist

Color & Contrast:
- [ ] Text contrast ≥ 4.5:1
- [ ] Large text contrast ≥ 3:1
- [ ] UI components contrast ≥ 3:1
- [ ] Information not conveyed by color alone

Keyboard:
- [ ] All interactive elements reachable via Tab
- [ ] Visible focus indicators on all elements
- [ ] Logical tab order
- [ ] No keyboard traps
- [ ] Skip link available

Screen Readers:
- [ ] All images have appropriate alt text
- [ ] Form inputs have labels
- [ ] Buttons have accessible names
- [ ] Dynamic content announces changes
- [ ] Headings in logical order

Semantic HTML:
- [ ] Proper heading hierarchy (h1-h6)
- [ ] Semantic elements used (header, nav, main, footer)
- [ ] Lists use ul/ol/dl
- [ ] Buttons for actions, links for navigation

Forms:
- [ ] All inputs have labels
- [ ] Required fields indicated
- [ ] Error messages associated with fields
- [ ] Help text provided where needed

ARIA:
- [ ] ARIA roles used appropriately
- [ ] aria-label/aria-labelledby for non-text elements
- [ ] aria-describedby for additional context
- [ ] aria-live for dynamic content

---

## Quick Reference

### Contrast Ratios
- Normal text: 4.5:1 (AA), 7:1 (AAA)
- Large text: 3:1 (AA), 4.5:1 (AAA)
- UI components: 3:1

### Focus Indicators
```html
<button class="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
```

### Screen Reader Only
```html
<span class="sr-only">Text for screen readers</span>
```

### Skip Link
```html
<a href="#main" class="sr-only focus:not-sr-only">Skip to main content</a>
```

### ARIA Live
```html
<div role="alert" aria-live="assertive">Urgent message</div>
<div role="status" aria-live="polite">Status update</div>
```

### Semantic HTML
```html
<header>, <nav>, <main>, <article>, <aside>, <footer>, <section>
```

---

## Resources

- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
- [WebAIM Articles](https://webaim.org/articles/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [Inclusive Components](https://inclusive-components.design/)
