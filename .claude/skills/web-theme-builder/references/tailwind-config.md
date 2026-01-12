# Tailwind CSS v4.0 Configuration Reference

Complete guide to configuring Tailwind CSS v4.0 with @theme directive and design tokens.

## Table of Contents

1. [Overview](#overview)
2. [@theme Directive](#theme-directive)
3. [Color Configuration](#color-configuration)
4. [Typography Configuration](#typography-configuration)
5. [Spacing System](#spacing-system)
6. [Border Radius](#border-radius)
7. [Shadows](#shadows)
8. [Breakpoints](#breakpoints)
9. [Custom Utilities](#custom-utilities)
10. [Dark Mode](#dark-mode)
11. [Complete Examples](#complete-examples)

---

## Overview

Tailwind CSS v4.0 introduces the `@theme` directive for defining design tokens in CSS. This replaces the JavaScript configuration file with native CSS custom properties.

**Key Benefits:**
- Type-safe design tokens
- Better IDE support
- Faster build times
- Native CSS variables
- Easier theme switching

---

## @theme Directive

The `@theme` directive defines design tokens that Tailwind uses to generate utility classes.

### Basic Structure

```css
@import "tailwindcss";

@theme {
  /* Your design tokens here */
  --color-primary: 220 90% 56%;
  --font-display: 'Inter', sans-serif;
  --spacing-xl: 3rem;
}
```

### File Structure

**Recommended approach**: Create a dedicated `theme.css` file

```css
/* theme.css */
@import "tailwindcss";

@theme {
  /* Colors */
  --color-*: value;

  /* Typography */
  --font-*: value;
  --text-*: value;

  /* Spacing */
  --spacing-*: value;

  /* Layout */
  --width-*: value;
  --height-*: value;

  /* Effects */
  --shadow-*: value;
  --radius-*: value;
}

/* Custom utilities and components */
@layer components {
  /* ... */
}
```

---

## Color Configuration

### HSL Format (Recommended)

Use HSL without the `hsl()` wrapper for flexibility:

```css
@theme {
  /* Primary Colors */
  --color-primary: 220 90% 56%;          /* Blue */
  --color-primary-dark: 220 90% 45%;
  --color-primary-light: 220 90% 67%;

  /* Secondary Colors */
  --color-secondary: 280 70% 60%;        /* Purple */
  --color-accent: 340 80% 58%;           /* Pink */

  /* Neutral Colors */
  --color-background: 0 0% 100%;         /* White */
  --color-surface: 0 0% 98%;             /* Light gray */
  --color-text: 0 0% 10%;                /* Near black */
  --color-text-muted: 0 0% 45%;          /* Gray */

  /* Semantic Colors */
  --color-success: 142 71% 45%;          /* Green */
  --color-warning: 38 92% 50%;           /* Orange */
  --color-error: 0 84% 60%;              /* Red */
  --color-info: 199 89% 48%;             /* Light blue */
}
```

### Usage in HTML

```html
<div class="bg-primary text-white">Primary background</div>
<div class="bg-primary-dark text-white">Darker primary</div>
<div class="text-primary border-primary">Primary text and border</div>
```

### Color Scale Generation

For a complete color scale, define shades from 50 to 950:

```css
@theme {
  --color-blue-50: 214 100% 97%;
  --color-blue-100: 214 95% 93%;
  --color-blue-200: 213 97% 87%;
  --color-blue-300: 212 96% 78%;
  --color-blue-400: 213 94% 68%;
  --color-blue-500: 217 91% 60%;         /* Base */
  --color-blue-600: 221 83% 53%;
  --color-blue-700: 224 76% 48%;
  --color-blue-800: 226 71% 40%;
  --color-blue-900: 224 64% 33%;
  --color-blue-950: 226 57% 21%;
}
```

Usage:
```html
<div class="bg-blue-500 hover:bg-blue-600">Button</div>
```

### Opacity Modifiers

HSL format automatically supports opacity:

```html
<div class="bg-primary/50">50% opacity</div>
<div class="bg-primary/90">90% opacity</div>
<div class="text-text-muted/70">70% opacity</div>
```

---

## Typography Configuration

### Font Families

```css
@theme {
  /* Display fonts (headings, hero text) */
  --font-display: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  /* Text fonts (body copy) */
  --font-text: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;

  /* Monospace fonts (code) */
  --font-mono: 'Fira Code', 'JetBrains Mono', 'Courier New', monospace;
}
```

Usage:
```html
<h1 class="font-display">Heading</h1>
<p class="font-text">Body text</p>
<code class="font-mono">const x = 10;</code>
```

### Font Sizes

```css
@theme {
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */
  --text-6xl: 3.75rem;     /* 60px */
  --text-7xl: 4.5rem;      /* 72px */
  --text-8xl: 6rem;        /* 96px */
  --text-9xl: 8rem;        /* 128px */
}
```

Usage:
```html
<h1 class="text-5xl">Large heading</h1>
<p class="text-base">Normal text</p>
<small class="text-sm">Small text</small>
```

### Font Weights

```css
@theme {
  --font-thin: 100;
  --font-extralight: 200;
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-extrabold: 800;
  --font-black: 900;
}
```

Usage:
```html
<h1 class="font-bold">Bold heading</h1>
<p class="font-normal">Normal text</p>
<span class="font-light">Light text</span>
```

### Line Heights

```css
@theme {
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
}
```

### Letter Spacing

```css
@theme {
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
  --tracking-widest: 0.1em;
}
```

---

## Spacing System

### Base Spacing Scale

Using 4px base unit (0.25rem):

```css
@theme {
  --spacing-0: 0;
  --spacing-px: 1px;
  --spacing-0-5: 0.125rem;  /* 2px */
  --spacing-1: 0.25rem;     /* 4px */
  --spacing-1-5: 0.375rem;  /* 6px */
  --spacing-2: 0.5rem;      /* 8px */
  --spacing-2-5: 0.625rem;  /* 10px */
  --spacing-3: 0.75rem;     /* 12px */
  --spacing-3-5: 0.875rem;  /* 14px */
  --spacing-4: 1rem;        /* 16px */
  --spacing-5: 1.25rem;     /* 20px */
  --spacing-6: 1.5rem;      /* 24px */
  --spacing-7: 1.75rem;     /* 28px */
  --spacing-8: 2rem;        /* 32px */
  --spacing-9: 2.25rem;     /* 36px */
  --spacing-10: 2.5rem;     /* 40px */
  --spacing-11: 2.75rem;    /* 44px */
  --spacing-12: 3rem;       /* 48px */
  --spacing-14: 3.5rem;     /* 56px */
  --spacing-16: 4rem;       /* 64px */
  --spacing-20: 5rem;       /* 80px */
  --spacing-24: 6rem;       /* 96px */
  --spacing-28: 7rem;       /* 112px */
  --spacing-32: 8rem;       /* 128px */
  --spacing-36: 9rem;       /* 144px */
  --spacing-40: 10rem;      /* 160px */
  --spacing-44: 11rem;      /* 176px */
  --spacing-48: 12rem;      /* 192px */
  --spacing-52: 13rem;      /* 208px */
  --spacing-56: 14rem;      /* 224px */
  --spacing-60: 15rem;      /* 240px */
  --spacing-64: 16rem;      /* 256px */
  --spacing-72: 18rem;      /* 288px */
  --spacing-80: 20rem;      /* 320px */
  --spacing-96: 24rem;      /* 384px */
}
```

Usage:
```html
<div class="p-4">Padding 16px</div>
<div class="m-8">Margin 32px</div>
<div class="gap-6">Gap 24px</div>
<div class="space-x-4">Horizontal spacing 16px</div>
```

---

## Border Radius

```css
@theme {
  --radius-none: 0;
  --radius-sm: 0.125rem;    /* 2px */
  --radius-base: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;    /* 6px */
  --radius-lg: 0.5rem;      /* 8px */
  --radius-xl: 0.75rem;     /* 12px */
  --radius-2xl: 1rem;       /* 16px */
  --radius-3xl: 1.5rem;     /* 24px */
  --radius-full: 9999px;    /* Fully rounded */
}
```

Usage:
```html
<div class="rounded-lg">Large rounded corners</div>
<button class="rounded-full">Pill button</button>
<img class="rounded-xl" src="...">
```

---

## Shadows

```css
@theme {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
  --shadow-none: 0 0 #0000;
}
```

Usage:
```html
<div class="shadow-md">Medium shadow</div>
<div class="shadow-xl hover:shadow-2xl">Elevated card</div>
```

---

## Breakpoints

```css
@theme {
  --breakpoint-sm: 640px;   /* Small devices (landscape phones) */
  --breakpoint-md: 768px;   /* Medium devices (tablets) */
  --breakpoint-lg: 1024px;  /* Large devices (laptops) */
  --breakpoint-xl: 1280px;  /* Extra large devices (desktops) */
  --breakpoint-2xl: 1536px; /* 2X large devices (large desktops) */
}
```

Usage:
```html
<div class="w-full md:w-1/2 lg:w-1/3">Responsive width</div>
<h1 class="text-3xl md:text-5xl lg:text-7xl">Responsive text</h1>
```

---

## Custom Utilities

### Adding Custom Utilities

```css
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }

  .gradient-text {
    @apply bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent;
  }
}
```

Usage:
```html
<h1 class="text-balance">Balanced text wrapping</h1>
<div class="scrollbar-hide">Hidden scrollbar</div>
<h2 class="gradient-text">Gradient text effect</h2>
```

### Component Classes

```css
@layer components {
  .btn {
    @apply px-6 py-3 rounded-lg font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2;
  }

  .btn-primary {
    @apply btn bg-primary text-white hover:bg-primary-dark focus:ring-primary;
  }

  .btn-secondary {
    @apply btn border-2 border-primary text-primary hover:bg-primary hover:text-white focus:ring-primary;
  }

  .card {
    @apply bg-surface rounded-xl shadow-md p-6;
  }

  .input {
    @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent;
  }
}
```

Usage:
```html
<button class="btn-primary">Primary Button</button>
<div class="card">Card content</div>
<input class="input" type="text">
```

---

## Dark Mode

### Approach 1: CSS Variables

Define dark mode colors in your theme:

```css
@theme {
  /* Light mode (default) */
  --color-background: 0 0% 100%;
  --color-text: 0 0% 10%;

  /* Dark mode variants */
  @media (prefers-color-scheme: dark) {
    --color-background: 0 0% 10%;
    --color-text: 0 0% 90%;
  }
}
```

### Approach 2: Class-Based

```css
@theme {
  --color-background: 0 0% 100%;
  --color-text: 0 0% 10%;
}

.dark {
  --color-background: 0 0% 10%;
  --color-text: 0 0% 90%;
}
```

Toggle dark mode with JavaScript:
```javascript
document.documentElement.classList.toggle('dark');
```

### Approach 3: Utility Classes

```html
<div class="bg-white dark:bg-gray-900 text-black dark:text-white">
  Content with dark mode
</div>
```

---

## Complete Examples

### Modern/Minimalist Theme

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: 0 0% 10%;
  --color-secondary: 0 0% 30%;
  --color-accent: 0 0% 50%;
  --color-background: 0 0% 100%;
  --color-surface: 0 0% 98%;
  --color-text: 0 0% 10%;
  --color-text-muted: 0 0% 45%;

  /* Typography */
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-text: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Spacing - using minimal scale */
  --spacing-unit: 0.25rem;

  /* Border Radius - minimal */
  --radius-sm: 0.125rem;
  --radius-md: 0.25rem;
  --radius-lg: 0.375rem;

  /* Shadows - subtle */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 2px 4px 0 rgb(0 0 0 / 0.08);
}

@layer components {
  .btn-minimal {
    @apply px-8 py-3 bg-primary text-white rounded-sm font-medium hover:bg-secondary transition-colors;
  }
}
```

### Corporate/Professional Theme

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: 220 90% 56%;
  --color-secondary: 220 70% 45%;
  --color-accent: 210 80% 60%;
  --color-background: 0 0% 100%;
  --color-surface: 210 20% 98%;
  --color-text: 220 30% 15%;
  --color-text-muted: 220 15% 50%;

  /* Typography */
  --font-display: 'Inter', 'Roboto', sans-serif;
  --font-text: 'Inter', sans-serif;

  /* Border Radius - moderate */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;

  /* Shadows - pronounced */
  --shadow-sm: 0 2px 4px 0 rgb(0 0 0 / 0.08);
  --shadow-md: 0 4px 12px 0 rgb(0 0 0 / 0.12);
  --shadow-lg: 0 8px 24px 0 rgb(0 0 0 / 0.15);
}
```

### Dark/Tech Theme

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: 180 100% 50%;
  --color-secondary: 280 100% 60%;
  --color-accent: 330 100% 60%;
  --color-background: 220 20% 10%;
  --color-surface: 220 18% 15%;
  --color-text: 0 0% 95%;
  --color-text-muted: 0 0% 60%;

  /* Typography */
  --font-display: 'JetBrains Mono', 'Fira Code', monospace;
  --font-text: 'Inter', sans-serif;

  /* Border Radius - sharp */
  --radius-sm: 0.125rem;
  --radius-md: 0.25rem;
  --radius-lg: 0.5rem;

  /* Shadows - glowing */
  --shadow-glow: 0 0 20px rgb(180 100% 50% / 0.3);
  --shadow-glow-lg: 0 0 40px rgb(180 100% 50% / 0.4);
}

@layer components {
  .btn-neon {
    @apply px-6 py-3 bg-primary text-background rounded-sm font-semibold;
    box-shadow: 0 0 20px var(--color-primary);
  }

  .card-tech {
    @apply bg-surface rounded-md p-6 border border-primary/20;
  }
}
```

---

## Performance Optimization

### Purge Unused Styles

Tailwind v4.0 automatically purges unused styles. Ensure your configuration scans all template files:

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

### Content Configuration

Specify which files to scan for class names:

```javascript
// tailwind.config.js
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx,html}',
  ],
}
```

---

## Best Practices

1. **Use Semantic Names**: Name colors by purpose (primary, secondary) not appearance (blue, red)
2. **Consistent Scale**: Use powers of 2 or Fibonacci for spacing (4, 8, 16, 24, 32...)
3. **HSL Format**: Use HSL for easier color manipulation and dark mode
4. **Component Classes**: Create reusable component classes with @layer
5. **Mobile First**: Design for mobile, enhance for larger screens
6. **Accessibility**: Ensure 4.5:1 contrast ratio for text
7. **Performance**: Only include utilities you need
8. **Dark Mode**: Plan dark mode from the start with CSS variables

---

## Troubleshooting

### Colors Not Working

Ensure HSL values don't include `hsl()` wrapper:
```css
/* ❌ Wrong */
--color-primary: hsl(220, 90%, 56%);

/* ✅ Correct */
--color-primary: 220 90% 56%;
```

### Opacity Not Applying

Use `/` syntax for opacity:
```html
<!-- ❌ Wrong -->
<div class="bg-primary opacity-50">

<!-- ✅ Correct -->
<div class="bg-primary/50">
```

### Custom Fonts Not Loading

Include font-face declarations before @theme:
```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom-font.woff2') format('woff2');
}

@theme {
  --font-display: 'CustomFont', sans-serif;
}
```

---

## Migration from v3.x

### Old Format (tailwind.config.js)

```javascript
module.exports = {
  theme: {
    colors: {
      primary: '#3b82f6',
    },
    fontFamily: {
      display: ['Inter', 'sans-serif'],
    },
  },
}
```

### New Format (CSS @theme)

```css
@theme {
  --color-primary: 217 91% 60%;
  --font-display: 'Inter', sans-serif;
}
```

---

## Additional Resources

- [Tailwind CSS v4.0 Blog Post](https://tailwindcss.com/blog/tailwindcss-v4)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Color Palette Generator](https://uicolors.app/)
- [HSL Color Picker](https://hslpicker.com/)
