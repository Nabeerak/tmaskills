# Responsive Design Patterns Reference

Complete guide to mobile-first responsive design patterns and best practices.

## Table of Contents

1. [Mobile-First Philosophy](#mobile-first-philosophy)
2. [Breakpoint System](#breakpoint-system)
3. [Layout Patterns](#layout-patterns)
4. [Typography Patterns](#typography-patterns)
5. [Navigation Patterns](#navigation-patterns)
6. [Image Patterns](#image-patterns)
7. [Spacing Patterns](#spacing-patterns)
8. [Component Patterns](#component-patterns)
9. [Touch Targets](#touch-targets)
10. [Testing](#testing)

---

## Mobile-First Philosophy

**Mobile-first** means designing for the smallest screen first, then progressively enhancing for larger screens.

### Why Mobile-First?

1. **Performance**: Smaller devices get lighter, faster experiences
2. **Constraints**: Forces focus on essential content and features
3. **Progressive Enhancement**: Easier to add than subtract
4. **Usage Patterns**: Mobile traffic often exceeds desktop

### Mobile-First Code Pattern

```html
<!-- ❌ Wrong: Desktop-first -->
<div class="grid-cols-3 md:grid-cols-1">
  <!-- This requires overriding for mobile -->
</div>

<!-- ✅ Correct: Mobile-first -->
<div class="grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <!-- This enhances progressively -->
</div>
```

### Design Process

1. **Start Small**: Design for 320px width first (smallest common viewport)
2. **Add Breakpoints**: When layout breaks or content demands it
3. **Enhance**: Add features and complexity for larger screens
4. **Test**: Verify on real devices, not just browser resize

---

## Breakpoint System

### Standard Breakpoints

```css
/* Tailwind default breakpoints */
/* No prefix: 0px and up (mobile) */
sm: 640px   /* Small devices (landscape phones) */
md: 768px   /* Medium devices (tablets) */
lg: 1024px  /* Large devices (laptops) */
xl: 1280px  /* Extra large devices (desktops) */
2xl: 1536px /* 2X large devices (large desktops) */
```

### Common Device Sizes

| Device Type | Portrait | Landscape |
|-------------|----------|-----------|
| Phone (small) | 320px | 568px |
| Phone (medium) | 375px | 667px |
| Phone (large) | 414px | 896px |
| Tablet | 768px | 1024px |
| Laptop | - | 1366px |
| Desktop | - | 1920px |

### Breakpoint Usage

```html
<!-- Width -->
<div class="w-full sm:w-1/2 lg:w-1/3">
  <!-- Full width on mobile, half on small screens, third on large -->
</div>

<!-- Padding -->
<section class="px-4 md:px-8 lg:px-16">
  <!-- Progressive padding increase -->
</section>

<!-- Display -->
<div class="block md:hidden">Mobile only</div>
<div class="hidden md:block">Desktop only</div>
<div class="hidden md:block lg:hidden">Tablet only</div>
```

### Custom Breakpoints

For specific needs:

```css
@media (min-width: 900px) {
  /* Custom breakpoint */
}

@media (min-width: 640px) and (max-width: 1024px) {
  /* Tablet-specific styles */
}
```

---

## Layout Patterns

### Container Pattern

Responsive container with max-width:

```html
<div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Content constrained to max 1280px with responsive padding -->
</div>
```

Sizes:
- `max-w-sm`: 384px (24rem)
- `max-w-md`: 448px (28rem)
- `max-w-lg`: 512px (32rem)
- `max-w-xl`: 576px (36rem)
- `max-w-2xl`: 672px (42rem)
- `max-w-3xl`: 768px (48rem)
- `max-w-4xl`: 896px (56rem)
- `max-w-5xl`: 1024px (64rem)
- `max-w-6xl`: 1152px (72rem)
- `max-w-7xl`: 1280px (80rem)

### Grid Patterns

**Responsive Grid:**

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <!-- ... -->
</div>
```

**Auto-Fit Grid** (CSS Grid):

```html
<div class="grid gap-6" style="grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));">
  <!-- Items automatically wrap based on available space -->
</div>
```

**Asymmetric Grid:**

```html
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
  <div class="lg:col-span-8">Main content (2/3)</div>
  <div class="lg:col-span-4">Sidebar (1/3)</div>
</div>
```

### Flexbox Patterns

**Stack to Row:**

```html
<div class="flex flex-col md:flex-row gap-4">
  <div class="flex-1">Item 1</div>
  <div class="flex-1">Item 2</div>
  <div class="flex-1">Item 3</div>
</div>
```

**Centered Content:**

```html
<div class="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>
```

**Responsive Alignment:**

```html
<div class="flex flex-col items-start md:flex-row md:items-center md:justify-between gap-4">
  <div>Left content</div>
  <div>Right content</div>
</div>
```

### Two-Column Layout

```html
<div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
  <div>
    <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">Heading</h2>
    <p class="text-lg">Content</p>
  </div>
  <div>
    <img src="image.jpg" alt="Description" class="rounded-xl w-full">
  </div>
</div>
```

### Three-Column Layout

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

### Sidebar Layout

```html
<div class="flex flex-col lg:flex-row gap-8">
  <!-- Sidebar -->
  <aside class="w-full lg:w-64 flex-shrink-0">
    <nav>Navigation</nav>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 min-w-0">
    <article>Content</article>
  </main>
</div>
```

---

## Typography Patterns

### Responsive Font Sizes

```html
<!-- Headings -->
<h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold">
  Hero Heading
</h1>

<h2 class="text-3xl sm:text-4xl md:text-5xl font-bold">
  Section Heading
</h2>

<h3 class="text-2xl sm:text-3xl md:text-4xl font-semibold">
  Subsection Heading
</h3>

<!-- Body Text -->
<p class="text-base md:text-lg">
  Body text that's slightly larger on bigger screens
</p>

<!-- Small Text -->
<small class="text-sm md:text-base">
  Fine print that's more readable on larger screens
</small>
```

### Line Length

Optimal reading: 50-75 characters per line

```html
<div class="max-w-prose mx-auto">
  <!-- max-w-prose = 65ch (characters) for optimal readability -->
  <p>Long-form content with optimal line length...</p>
</div>
```

### Line Height

```html
<!-- Tight for headings -->
<h1 class="leading-tight md:leading-none">
  Heading
</h1>

<!-- Relaxed for body text -->
<p class="leading-relaxed md:leading-loose">
  Body text with comfortable line spacing for reading.
</p>
```

### Text Alignment

```html
<!-- Center on mobile, left on desktop -->
<h2 class="text-center md:text-left">
  Heading
</h2>

<!-- Stack center, then align left in columns -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
  <div class="text-center md:text-left">Content</div>
  <div class="text-center md:text-left">Content</div>
</div>
```

---

## Navigation Patterns

### Mobile-First Navigation

```html
<nav class="bg-white shadow-sm sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <!-- Logo -->
      <div class="flex-shrink-0">
        <a href="/" class="text-2xl font-bold">Logo</a>
      </div>

      <!-- Desktop Navigation (hidden on mobile) -->
      <div class="hidden md:flex space-x-8">
        <a href="#" class="hover:text-primary">Home</a>
        <a href="#" class="hover:text-primary">Features</a>
        <a href="#" class="hover:text-primary">Pricing</a>
        <a href="#" class="hover:text-primary">Contact</a>
      </div>

      <!-- Mobile Menu Button -->
      <button class="md:hidden p-2" aria-label="Toggle menu">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
    </div>
  </div>

  <!-- Mobile Menu (toggle with JavaScript) -->
  <div class="md:hidden border-t">
    <div class="px-4 py-4 space-y-2">
      <a href="#" class="block px-4 py-2 hover:bg-gray-100 rounded">Home</a>
      <a href="#" class="block px-4 py-2 hover:bg-gray-100 rounded">Features</a>
      <a href="#" class="block px-4 py-2 hover:bg-gray-100 rounded">Pricing</a>
      <a href="#" class="block px-4 py-2 hover:bg-gray-100 rounded">Contact</a>
    </div>
  </div>
</nav>
```

### Hamburger to Full Menu

```html
<!-- Hamburger icon on mobile, full menu on desktop -->
<nav class="flex items-center justify-between">
  <a href="/" class="text-2xl font-bold">Brand</a>

  <!-- Mobile: Hamburger -->
  <button class="lg:hidden">
    <svg class="w-6 h-6"><!-- Hamburger icon --></svg>
  </button>

  <!-- Desktop: Full Menu -->
  <ul class="hidden lg:flex space-x-8">
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Services</a></li>
    <li><a href="#">Contact</a></li>
  </ul>
</nav>
```

### Sticky Navigation

```html
<!-- Sticky on all screens -->
<nav class="sticky top-0 z-50 bg-white shadow-md">
  <!-- Navigation content -->
</nav>

<!-- Sticky only on desktop -->
<nav class="md:sticky md:top-0 z-50 bg-white shadow-md">
  <!-- Navigation content -->
</nav>
```

---

## Image Patterns

### Responsive Images

```html
<!-- Full width on mobile, constrained on desktop -->
<img
  src="image.jpg"
  alt="Description"
  class="w-full md:w-auto md:max-w-md lg:max-w-lg"
>

<!-- Different aspect ratios -->
<div class="aspect-square md:aspect-video">
  <img src="image.jpg" alt="Description" class="w-full h-full object-cover">
</div>

<!-- Responsive object-fit -->
<img
  src="image.jpg"
  alt="Description"
  class="w-full h-48 md:h-64 lg:h-80 object-cover rounded-xl"
>
```

### Picture Element (Art Direction)

Different images for different screens:

```html
<picture>
  <source media="(min-width: 1024px)" srcset="desktop-image.jpg">
  <source media="(min-width: 768px)" srcset="tablet-image.jpg">
  <img src="mobile-image.jpg" alt="Description" class="w-full">
</picture>
```

### Lazy Loading

```html
<img
  src="image.jpg"
  alt="Description"
  loading="lazy"
  class="w-full"
>
```

---

## Spacing Patterns

### Responsive Padding

```html
<!-- Section padding -->
<section class="py-12 md:py-16 lg:py-24 px-4 md:px-8 lg:px-16">
  Content
</section>

<!-- Card padding -->
<div class="p-4 md:p-6 lg:p-8">
  Card content
</div>
```

### Responsive Gaps

```html
<!-- Grid gaps -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
  <div>Item</div>
  <!-- ... -->
</div>

<!-- Flex gaps -->
<div class="flex flex-col md:flex-row gap-4 md:gap-6 lg:gap-8">
  <div>Item</div>
  <!-- ... -->
</div>
```

### Responsive Margins

```html
<!-- Section margins -->
<section class="mb-12 md:mb-16 lg:mb-24">
  Content
</section>

<!-- Component spacing -->
<h2 class="mb-4 md:mb-6 lg:mb-8">Heading</h2>
<p class="mb-4 md:mb-6">Paragraph</p>
```

---

## Component Patterns

### Responsive Cards

```html
<div class="bg-white rounded-xl shadow-md overflow-hidden flex flex-col md:flex-row">
  <!-- Image: full width on mobile, fixed width on desktop -->
  <img src="card.jpg" alt="Card" class="w-full md:w-48 h-48 md:h-auto object-cover">

  <!-- Content: full width on mobile, flex-1 on desktop -->
  <div class="p-6 md:p-8 flex-1">
    <h3 class="text-xl md:text-2xl font-bold mb-2">Card Title</h3>
    <p class="text-base md:text-lg text-gray-600">Card description text.</p>
  </div>
</div>
```

### Responsive Buttons

```html
<!-- Full width on mobile, auto on desktop -->
<button class="w-full md:w-auto px-6 py-3 bg-primary text-white rounded-lg">
  Button
</button>

<!-- Stack on mobile, inline on desktop -->
<div class="flex flex-col md:flex-row gap-4">
  <button class="w-full md:w-auto px-6 py-3 bg-primary text-white rounded-lg">
    Primary
  </button>
  <button class="w-full md:w-auto px-6 py-3 border-2 border-primary text-primary rounded-lg">
    Secondary
  </button>
</div>
```

### Responsive Forms

```html
<form class="max-w-2xl mx-auto px-4">
  <!-- Single column on mobile, two columns on desktop -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
    <div>
      <label class="block mb-2">First Name</label>
      <input type="text" class="w-full px-4 py-2 border rounded-lg">
    </div>
    <div>
      <label class="block mb-2">Last Name</label>
      <input type="text" class="w-full px-4 py-2 border rounded-lg">
    </div>
  </div>

  <!-- Full width button on mobile, auto on desktop -->
  <button class="w-full md:w-auto px-8 py-3 bg-primary text-white rounded-lg">
    Submit
  </button>
</form>
```

### Responsive Modals

```html
<!-- Full screen on mobile, centered on desktop -->
<div class="fixed inset-0 bg-black/50 flex items-end md:items-center justify-center p-0 md:p-4">
  <div class="bg-white rounded-t-2xl md:rounded-2xl w-full md:max-w-lg max-h-[90vh] overflow-y-auto">
    <div class="p-6 md:p-8">
      <h2 class="text-2xl md:text-3xl font-bold mb-4">Modal Title</h2>
      <p class="mb-6">Modal content...</p>
      <button class="w-full md:w-auto px-6 py-3 bg-primary text-white rounded-lg">
        Action
      </button>
    </div>
  </div>
</div>
```

---

## Touch Targets

### Minimum Touch Target Size

**WCAG Guideline**: Minimum 44x44px (iOS) or 48x48px (Android)

```html
<!-- ❌ Too small -->
<button class="px-2 py-1 text-sm">
  Tap Me
</button>

<!-- ✅ Appropriate size -->
<button class="px-6 py-3 text-base">
  Tap Me
</button>

<!-- ✅ Icon button with padding -->
<button class="p-3">
  <svg class="w-6 h-6"><!-- Icon --></svg>
</button>
```

### Spacing Between Targets

Minimum 8px spacing between interactive elements:

```html
<!-- Buttons with adequate spacing -->
<div class="flex gap-4">
  <button class="px-6 py-3">Button 1</button>
  <button class="px-6 py-3">Button 2</button>
</div>

<!-- Links in navigation -->
<nav class="space-y-2">
  <a href="#" class="block py-2">Link 1</a>
  <a href="#" class="block py-2">Link 2</a>
  <a href="#" class="block py-2">Link 3</a>
</nav>
```

---

## Testing

### Device Testing Checklist

- [ ] iPhone SE (375x667) - small phone
- [ ] iPhone 12 Pro (390x844) - standard phone
- [ ] iPad (768x1024) - tablet portrait
- [ ] iPad (1024x768) - tablet landscape
- [ ] Laptop (1366x768) - small laptop
- [ ] Desktop (1920x1080) - standard desktop

### Browser DevTools

**Chrome/Edge:**
1. F12 → Toggle device toolbar (Ctrl+Shift+M)
2. Select device preset or custom dimensions
3. Test touch mode, throttle network

**Firefox:**
1. F12 → Responsive Design Mode (Ctrl+Shift+M)
2. Test various screen sizes
3. Screenshot entire page

**Safari:**
1. Develop → Enter Responsive Design Mode
2. Test iOS devices

### Testing Checklist

Layout:
- [ ] Content readable at all breakpoints
- [ ] No horizontal scrolling
- [ ] Images scale appropriately
- [ ] Navigation accessible on all devices

Typography:
- [ ] Text size appropriate for screen
- [ ] Line length comfortable (50-75 characters)
- [ ] Headings hierarchy clear

Interaction:
- [ ] Buttons large enough to tap (44x44px minimum)
- [ ] Forms usable on mobile
- [ ] Dropdown menus accessible
- [ ] Modal/overlay behavior appropriate

Performance:
- [ ] Images optimized for mobile
- [ ] Fast load times on 3G
- [ ] Minimal layout shift

Accessibility:
- [ ] Zoom to 200% still usable
- [ ] Keyboard navigation works
- [ ] Screen reader friendly
- [ ] Color contrast sufficient

---

## Common Patterns Summary

### Hero Section

```html
<section class="py-12 md:py-20 lg:py-32 px-4">
  <div class="max-w-7xl mx-auto text-center">
    <h1 class="text-4xl md:text-5xl lg:text-7xl font-bold mb-6">
      Hero Heading
    </h1>
    <p class="text-lg md:text-xl lg:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
      Hero description text
    </p>
    <div class="flex flex-col sm:flex-row gap-4 justify-center">
      <button class="px-8 py-4 bg-primary text-white rounded-lg">
        Primary CTA
      </button>
      <button class="px-8 py-4 border-2 border-primary text-primary rounded-lg">
        Secondary CTA
      </button>
    </div>
  </div>
</section>
```

### Feature Grid

```html
<section class="py-12 md:py-20 px-4">
  <div class="max-w-7xl mx-auto">
    <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold text-center mb-12">
      Features
    </h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
      <!-- Feature cards -->
    </div>
  </div>
</section>
```

### Content + Image

```html
<section class="py-12 md:py-20 px-4">
  <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 items-center">
    <div class="order-2 lg:order-1">
      <h2 class="text-3xl md:text-4xl font-bold mb-4">Heading</h2>
      <p class="text-lg text-gray-600 mb-6">Description</p>
      <button class="px-8 py-3 bg-primary text-white rounded-lg">
        CTA
      </button>
    </div>
    <div class="order-1 lg:order-2">
      <img src="image.jpg" alt="Description" class="rounded-xl w-full">
    </div>
  </div>
</section>
```

---

## Best Practices

1. **Always Start Mobile**: Design smallest screen first
2. **Progressive Enhancement**: Add complexity for larger screens
3. **Test Early**: Check responsive behavior frequently
4. **Touch Targets**: 44px minimum for interactive elements
5. **Readable Text**: 16px minimum for body text on mobile
6. **Avoid Fixed Widths**: Use percentages, flex, and grid
7. **Optimize Images**: Use responsive images and lazy loading
8. **Consider Landscape**: Test both orientations on mobile/tablet
9. **Performance**: Smaller screens often have slower connections
10. **Accessibility**: Ensure usable at any size, with keyboard, screen readers

---

## Quick Reference

### Breakpoint Prefixes

```
(no prefix): 0px+
sm: 640px+
md: 768px+
lg: 1024px+
xl: 1280px+
2xl: 1536px+
```

### Common Patterns

```html
<!-- Responsive width -->
<div class="w-full md:w-1/2 lg:w-1/3">

<!-- Responsive padding -->
<div class="p-4 md:p-6 lg:p-8">

<!-- Responsive text -->
<h1 class="text-3xl md:text-5xl lg:text-7xl">

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

<!-- Hide/show -->
<div class="block md:hidden">Mobile only</div>
<div class="hidden md:block">Desktop only</div>

<!-- Flex direction -->
<div class="flex flex-col md:flex-row gap-4">
```
