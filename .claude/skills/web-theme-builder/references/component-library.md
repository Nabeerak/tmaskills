# Component Library Reference

Complete HTML/Tailwind component patterns for all standard web elements.

## Table of Contents

1. [Buttons](#buttons)
2. [Cards](#cards)
3. [Forms](#forms)
4. [Navigation](#navigation)
5. [Hero Sections](#hero-sections)
6. [Call-to-Action (CTA)](#call-to-action-cta)
7. [Footer](#footer)
8. [Component Composition Patterns](#component-composition-patterns)

---

## Buttons

### Primary Button

**Use**: Main CTAs, primary actions, form submissions

```html
<button class="px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors">
  Click Me
</button>
```

**Variants**:
- Small: `px-4 py-2 text-sm`
- Large: `px-8 py-4 text-lg`
- Full width: Add `w-full`
- With icon: Add `flex items-center gap-2`

### Secondary Button

**Use**: Secondary actions, cancel buttons

```html
<button class="px-6 py-3 bg-secondary text-white font-semibold rounded-lg hover:bg-secondary/90 focus:outline-none focus:ring-2 focus:ring-secondary focus:ring-offset-2 transition-colors">
  Secondary Action
</button>
```

### Outline Button

**Use**: Tertiary actions, less emphasis

```html
<button class="px-6 py-3 border-2 border-primary text-primary font-semibold rounded-lg hover:bg-primary hover:text-white focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-all">
  Outline Button
</button>
```

### Ghost Button

**Use**: Minimal emphasis, inline actions

```html
<button class="px-6 py-3 text-primary font-semibold rounded-lg hover:bg-primary/10 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors">
  Ghost Button
</button>
```

### Button with Icon

```html
<button class="px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors flex items-center gap-2">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
  </svg>
  Add Item
</button>
```

### Disabled State

```html
<button disabled class="px-6 py-3 bg-gray-300 text-gray-500 font-semibold rounded-lg cursor-not-allowed opacity-60">
  Disabled
</button>
```

---

## Cards

### Product Card

**Use**: E-commerce, product listings

```html
<div class="bg-surface rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
  <img src="product.jpg" alt="Product name" class="w-full h-48 object-cover">
  <div class="p-6">
    <h3 class="text-xl font-display font-semibold text-text mb-2">Product Name</h3>
    <p class="text-text-muted mb-4">Short product description goes here.</p>
    <div class="flex items-center justify-between">
      <span class="text-2xl font-bold text-primary">$49.99</span>
      <button class="px-4 py-2 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90">
        Add to Cart
      </button>
    </div>
  </div>
</div>
```

### Blog Card

**Use**: Blog posts, articles, news

```html
<article class="bg-surface rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
  <img src="blog-image.jpg" alt="Article title" class="w-full h-48 object-cover">
  <div class="p-6">
    <div class="flex items-center gap-2 text-sm text-text-muted mb-3">
      <time datetime="2024-01-15">Jan 15, 2024</time>
      <span>•</span>
      <span>5 min read</span>
    </div>
    <h3 class="text-xl font-display font-semibold text-text mb-2 hover:text-primary transition-colors">
      <a href="#">Article Title Goes Here</a>
    </h3>
    <p class="text-text-muted mb-4">
      Article excerpt that provides a brief summary of the content...
    </p>
    <a href="#" class="text-primary font-semibold hover:underline">Read More →</a>
  </div>
</article>
```

### Pricing Card

**Use**: Pricing tables, subscription plans

```html
<div class="bg-surface rounded-xl shadow-lg p-8 border-2 border-transparent hover:border-primary transition-colors">
  <div class="text-center mb-6">
    <h3 class="text-2xl font-display font-bold text-text mb-2">Pro Plan</h3>
    <div class="flex items-baseline justify-center gap-1">
      <span class="text-5xl font-bold text-text">$29</span>
      <span class="text-text-muted">/month</span>
    </div>
  </div>
  <ul class="space-y-3 mb-8">
    <li class="flex items-start gap-2">
      <svg class="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
      </svg>
      <span class="text-text">Unlimited projects</span>
    </li>
    <li class="flex items-start gap-2">
      <svg class="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
      </svg>
      <span class="text-text">Priority support</span>
    </li>
    <li class="flex items-start gap-2">
      <svg class="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
      </svg>
      <span class="text-text">Advanced analytics</span>
    </li>
  </ul>
  <button class="w-full px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors">
    Get Started
  </button>
</div>
```

### Feature Card

**Use**: Features, services, benefits

```html
<div class="bg-surface rounded-xl p-6 hover:shadow-lg transition-shadow">
  <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
    <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
    </svg>
  </div>
  <h3 class="text-xl font-display font-semibold text-text mb-2">Feature Name</h3>
  <p class="text-text-muted">Description of the feature and its benefits.</p>
</div>
```

---

## Forms

### Text Input

```html
<div class="mb-4">
  <label for="name" class="block text-sm font-medium text-text mb-2">
    Full Name
  </label>
  <input
    type="text"
    id="name"
    name="name"
    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
    placeholder="Enter your name"
  >
</div>
```

### Text Input with Error

```html
<div class="mb-4">
  <label for="email" class="block text-sm font-medium text-text mb-2">
    Email Address
  </label>
  <input
    type="email"
    id="email"
    name="email"
    class="w-full px-4 py-2 border-2 border-red-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
    placeholder="you@example.com"
    aria-invalid="true"
    aria-describedby="email-error"
  >
  <p id="email-error" class="mt-1 text-sm text-red-500">Please enter a valid email address</p>
</div>
```

### Textarea

```html
<div class="mb-4">
  <label for="message" class="block text-sm font-medium text-text mb-2">
    Message
  </label>
  <textarea
    id="message"
    name="message"
    rows="4"
    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
    placeholder="Enter your message"
  ></textarea>
</div>
```

### Select Dropdown

```html
<div class="mb-4">
  <label for="country" class="block text-sm font-medium text-text mb-2">
    Country
  </label>
  <select
    id="country"
    name="country"
    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
  >
    <option value="">Select a country</option>
    <option value="us">United States</option>
    <option value="uk">United Kingdom</option>
    <option value="ca">Canada</option>
  </select>
</div>
```

### Checkbox

```html
<div class="flex items-start gap-2 mb-4">
  <input
    type="checkbox"
    id="terms"
    name="terms"
    class="w-4 h-4 mt-1 text-primary border-gray-300 rounded focus:ring-2 focus:ring-primary"
  >
  <label for="terms" class="text-sm text-text">
    I agree to the <a href="#" class="text-primary hover:underline">Terms and Conditions</a>
  </label>
</div>
```

### Radio Buttons

```html
<fieldset class="mb-4">
  <legend class="block text-sm font-medium text-text mb-3">Select Plan</legend>
  <div class="space-y-2">
    <div class="flex items-center gap-2">
      <input
        type="radio"
        id="plan-basic"
        name="plan"
        value="basic"
        class="w-4 h-4 text-primary border-gray-300 focus:ring-2 focus:ring-primary"
      >
      <label for="plan-basic" class="text-text">Basic - $9/month</label>
    </div>
    <div class="flex items-center gap-2">
      <input
        type="radio"
        id="plan-pro"
        name="plan"
        value="pro"
        class="w-4 h-4 text-primary border-gray-300 focus:ring-2 focus:ring-primary"
      >
      <label for="plan-pro" class="text-text">Pro - $29/month</label>
    </div>
  </div>
</fieldset>
```

### Complete Contact Form

```html
<form class="max-w-2xl mx-auto bg-surface p-8 rounded-xl shadow-md">
  <h2 class="text-3xl font-display font-bold text-text mb-6">Get in Touch</h2>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
    <div>
      <label for="first-name" class="block text-sm font-medium text-text mb-2">First Name</label>
      <input type="text" id="first-name" name="first-name" required
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent">
    </div>
    <div>
      <label for="last-name" class="block text-sm font-medium text-text mb-2">Last Name</label>
      <input type="text" id="last-name" name="last-name" required
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent">
    </div>
  </div>

  <div class="mb-4">
    <label for="email" class="block text-sm font-medium text-text mb-2">Email</label>
    <input type="email" id="email" name="email" required
      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent">
  </div>

  <div class="mb-4">
    <label for="message" class="block text-sm font-medium text-text mb-2">Message</label>
    <textarea id="message" name="message" rows="5" required
      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"></textarea>
  </div>

  <button type="submit"
    class="w-full px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors">
    Send Message
  </button>
</form>
```

---

## Navigation

### Header Navigation (Desktop)

```html
<header class="bg-surface shadow-sm sticky top-0 z-50">
  <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <!-- Logo -->
      <div class="flex-shrink-0">
        <a href="/" class="text-2xl font-display font-bold text-primary">Brand</a>
      </div>

      <!-- Navigation Links -->
      <div class="hidden md:flex items-center space-x-8">
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Home</a>
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Features</a>
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Pricing</a>
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">About</a>
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Contact</a>
      </div>

      <!-- CTA Buttons -->
      <div class="hidden md:flex items-center space-x-4">
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Sign In</a>
        <a href="#" class="px-6 py-2 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors">
          Get Started
        </a>
      </div>

      <!-- Mobile Menu Button -->
      <button class="md:hidden p-2 rounded-lg hover:bg-gray-100" aria-label="Toggle menu">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
    </div>
  </nav>
</header>
```

### Mobile Navigation Menu

```html
<div class="md:hidden bg-surface border-t border-gray-200">
  <nav class="px-4 py-4 space-y-2">
    <a href="#" class="block px-4 py-2 text-text hover:bg-gray-100 rounded-lg transition-colors">Home</a>
    <a href="#" class="block px-4 py-2 text-text hover:bg-gray-100 rounded-lg transition-colors">Features</a>
    <a href="#" class="block px-4 py-2 text-text hover:bg-gray-100 rounded-lg transition-colors">Pricing</a>
    <a href="#" class="block px-4 py-2 text-text hover:bg-gray-100 rounded-lg transition-colors">About</a>
    <a href="#" class="block px-4 py-2 text-text hover:bg-gray-100 rounded-lg transition-colors">Contact</a>
    <div class="pt-4 space-y-2">
      <a href="#" class="block px-4 py-2 text-center border border-primary text-primary font-semibold rounded-lg hover:bg-primary hover:text-white transition-all">
        Sign In
      </a>
      <a href="#" class="block px-4 py-2 text-center bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors">
        Get Started
      </a>
    </div>
  </nav>
</div>
```

### Sidebar Navigation

```html
<aside class="w-64 bg-surface border-r border-gray-200 h-screen sticky top-0">
  <div class="p-6">
    <h2 class="text-2xl font-display font-bold text-primary mb-8">Dashboard</h2>
    <nav class="space-y-2">
      <a href="#" class="flex items-center gap-3 px-4 py-3 bg-primary/10 text-primary rounded-lg font-medium">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path>
        </svg>
        Home
      </a>
      <a href="#" class="flex items-center gap-3 px-4 py-3 text-text hover:bg-gray-100 rounded-lg font-medium transition-colors">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path>
          <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path>
        </svg>
        Analytics
      </a>
      <a href="#" class="flex items-center gap-3 px-4 py-3 text-text hover:bg-gray-100 rounded-lg font-medium transition-colors">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"></path>
          <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"></path>
        </svg>
        Projects
      </a>
      <a href="#" class="flex items-center gap-3 px-4 py-3 text-text hover:bg-gray-100 rounded-lg font-medium transition-colors">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
        </svg>
        Settings
      </a>
    </nav>
  </div>
</aside>
```

---

## Hero Sections

### Centered Hero

```html
<section class="py-20 px-4 bg-background">
  <div class="max-w-4xl mx-auto text-center">
    <h1 class="text-5xl md:text-6xl lg:text-7xl font-display font-bold text-text mb-6 leading-tight">
      Build Amazing Websites
    </h1>
    <p class="text-xl md:text-2xl text-text-muted mb-8 max-w-2xl mx-auto">
      Create beautiful, responsive web designs with our powerful theme builder. No coding required.
    </p>
    <div class="flex flex-col sm:flex-row gap-4 justify-center">
      <a href="#" class="px-8 py-4 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors text-lg">
        Get Started Free
      </a>
      <a href="#" class="px-8 py-4 border-2 border-primary text-primary font-semibold rounded-lg hover:bg-primary hover:text-white transition-all text-lg">
        View Demo
      </a>
    </div>
  </div>
</section>
```

### Split Hero with Image

```html
<section class="py-20 px-4 bg-background">
  <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div>
      <h1 class="text-5xl md:text-6xl font-display font-bold text-text mb-6 leading-tight">
        Transform Your Ideas Into Reality
      </h1>
      <p class="text-xl text-text-muted mb-8">
        Our platform helps you build, launch, and scale your projects faster than ever before.
      </p>
      <div class="flex flex-col sm:flex-row gap-4">
        <a href="#" class="px-8 py-4 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors text-center">
          Start Building
        </a>
        <a href="#" class="px-8 py-4 text-primary font-semibold rounded-lg hover:bg-primary/10 transition-colors flex items-center justify-center gap-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
          </svg>
          Watch Demo
        </a>
      </div>
    </div>
    <div>
      <img src="hero-image.jpg" alt="Product screenshot" class="rounded-xl shadow-2xl">
    </div>
  </div>
</section>
```

### Hero with Background Image

```html
<section class="relative py-32 px-4 bg-cover bg-center" style="background-image: url('hero-bg.jpg');">
  <div class="absolute inset-0 bg-black/50"></div>
  <div class="relative max-w-4xl mx-auto text-center text-white">
    <h1 class="text-5xl md:text-6xl lg:text-7xl font-display font-bold mb-6 leading-tight">
      Welcome to the Future
    </h1>
    <p class="text-xl md:text-2xl mb-8 max-w-2xl mx-auto opacity-90">
      Experience the next generation of web design and development.
    </p>
    <a href="#" class="inline-block px-8 py-4 bg-white text-primary font-semibold rounded-lg hover:bg-gray-100 transition-colors text-lg">
      Get Started
    </a>
  </div>
</section>
```

---

## Call-to-Action (CTA)

### Inline CTA

```html
<div class="bg-primary rounded-xl p-8 text-center text-white">
  <h3 class="text-3xl font-display font-bold mb-4">Ready to Get Started?</h3>
  <p class="text-lg mb-6 opacity-90">Join thousands of satisfied customers today.</p>
  <button class="px-8 py-3 bg-white text-primary font-semibold rounded-lg hover:bg-gray-100 transition-colors">
    Sign Up Now
  </button>
</div>
```

### Full-Width CTA Banner

```html
<section class="bg-gradient-to-r from-primary to-secondary py-16 px-4">
  <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
    <div class="text-white">
      <h3 class="text-3xl md:text-4xl font-display font-bold mb-2">Start Your Free Trial</h3>
      <p class="text-lg opacity-90">No credit card required. Cancel anytime.</p>
    </div>
    <div class="flex-shrink-0">
      <button class="px-8 py-4 bg-white text-primary font-semibold rounded-lg hover:bg-gray-100 transition-colors text-lg whitespace-nowrap">
        Get Started Free
      </button>
    </div>
  </div>
</section>
```

### CTA with Form

```html
<section class="py-20 px-4 bg-surface">
  <div class="max-w-3xl mx-auto text-center">
    <h2 class="text-4xl font-display font-bold text-text mb-4">Stay Updated</h2>
    <p class="text-xl text-text-muted mb-8">Subscribe to our newsletter for the latest updates and exclusive offers.</p>
    <form class="flex flex-col sm:flex-row gap-4 max-w-xl mx-auto">
      <input
        type="email"
        placeholder="Enter your email"
        required
        class="flex-1 px-6 py-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
      >
      <button
        type="submit"
        class="px-8 py-4 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors whitespace-nowrap"
      >
        Subscribe
      </button>
    </form>
  </div>
</section>
```

---

## Footer

### Simple Footer

```html
<footer class="bg-surface border-t border-gray-200 py-8 px-4">
  <div class="max-w-7xl mx-auto text-center">
    <p class="text-text-muted mb-4">&copy; 2024 Your Company. All rights reserved.</p>
    <div class="flex justify-center gap-6">
      <a href="#" class="text-text-muted hover:text-primary transition-colors">Privacy Policy</a>
      <a href="#" class="text-text-muted hover:text-primary transition-colors">Terms of Service</a>
      <a href="#" class="text-text-muted hover:text-primary transition-colors">Contact</a>
    </div>
  </div>
</footer>
```

### Multi-Column Footer

```html
<footer class="bg-surface border-t border-gray-200 py-12 px-4">
  <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
    <!-- Company Info -->
    <div>
      <h3 class="text-2xl font-display font-bold text-primary mb-4">Brand</h3>
      <p class="text-text-muted">Building amazing web experiences since 2024.</p>
    </div>

    <!-- Product Links -->
    <div>
      <h4 class="font-semibold text-text mb-4">Product</h4>
      <ul class="space-y-2">
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Features</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Pricing</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Demo</a></li>
      </ul>
    </div>

    <!-- Company Links -->
    <div>
      <h4 class="font-semibold text-text mb-4">Company</h4>
      <ul class="space-y-2">
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">About</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Blog</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Careers</a></li>
      </ul>
    </div>

    <!-- Legal Links -->
    <div>
      <h4 class="font-semibold text-text mb-4">Legal</h4>
      <ul class="space-y-2">
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Privacy</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Terms</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Contact</a></li>
      </ul>
    </div>
  </div>

  <!-- Bottom Bar -->
  <div class="border-t border-gray-200 pt-8">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
      <p class="text-text-muted">&copy; 2024 Your Company. All rights reserved.</p>
      <div class="flex gap-4">
        <a href="#" class="text-text-muted hover:text-primary transition-colors" aria-label="Twitter">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path></svg>
        </a>
        <a href="#" class="text-text-muted hover:text-primary transition-colors" aria-label="GitHub">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path></svg>
        </a>
      </div>
    </div>
  </div>
</footer>
```

### Footer with Newsletter

```html
<footer class="bg-gray-900 text-white py-12 px-4">
  <div class="max-w-7xl mx-auto">
    <!-- Newsletter Section -->
    <div class="mb-12 text-center">
      <h3 class="text-3xl font-display font-bold mb-4">Stay Connected</h3>
      <p class="text-gray-400 mb-6">Get the latest updates and exclusive offers.</p>
      <form class="flex flex-col sm:flex-row gap-4 max-w-xl mx-auto">
        <input
          type="email"
          placeholder="Enter your email"
          class="flex-1 px-6 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        >
        <button class="px-8 py-3 bg-primary hover:bg-primary/90 font-semibold rounded-lg transition-colors">
          Subscribe
        </button>
      </form>
    </div>

    <!-- Links Section -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
      <div>
        <h4 class="font-semibold mb-4">Product</h4>
        <ul class="space-y-2 text-gray-400">
          <li><a href="#" class="hover:text-white transition-colors">Features</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Pricing</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Demo</a></li>
        </ul>
      </div>
      <div>
        <h4 class="font-semibold mb-4">Company</h4>
        <ul class="space-y-2 text-gray-400">
          <li><a href="#" class="hover:text-white transition-colors">About</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Blog</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Careers</a></li>
        </ul>
      </div>
      <div>
        <h4 class="font-semibold mb-4">Resources</h4>
        <ul class="space-y-2 text-gray-400">
          <li><a href="#" class="hover:text-white transition-colors">Documentation</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Support</a></li>
          <li><a href="#" class="hover:text-white transition-colors">API</a></li>
        </ul>
      </div>
      <div>
        <h4 class="font-semibold mb-4">Legal</h4>
        <ul class="space-y-2 text-gray-400">
          <li><a href="#" class="hover:text-white transition-colors">Privacy</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Terms</a></li>
          <li><a href="#" class="hover:text-white transition-colors">Contact</a></li>
        </ul>
      </div>
    </div>

    <!-- Copyright -->
    <div class="border-t border-gray-800 pt-8 text-center text-gray-400">
      <p>&copy; 2024 Your Company. All rights reserved.</p>
    </div>
  </div>
</footer>
```

---

## Component Composition Patterns

### Pattern 1: Content Block with Image

Combine multiple components for rich content sections:

```html
<section class="py-20 px-4 bg-background">
  <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div>
      <h2 class="text-4xl font-display font-bold text-text mb-6">Feature Title</h2>
      <p class="text-lg text-text-muted mb-8">
        Detailed description of the feature and its benefits. Explain how it helps users solve their problems.
      </p>
      <ul class="space-y-4 mb-8">
        <li class="flex items-start gap-3">
          <svg class="w-6 h-6 text-primary flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <span class="text-text">Benefit one explained in detail</span>
        </li>
        <li class="flex items-start gap-3">
          <svg class="w-6 h-6 text-primary flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <span class="text-text">Benefit two explained in detail</span>
        </li>
      </ul>
      <a href="#" class="inline-block px-8 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors">
        Learn More
      </a>
    </div>
    <div>
      <img src="feature-image.jpg" alt="Feature visualization" class="rounded-xl shadow-xl">
    </div>
  </div>
</section>
```

### Pattern 2: Feature Grid

```html
<section class="py-20 px-4 bg-background">
  <div class="max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <h2 class="text-4xl font-display font-bold text-text mb-4">Our Features</h2>
      <p class="text-xl text-text-muted">Everything you need to succeed</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Feature Card 1 -->
      <div class="bg-surface rounded-xl p-8 hover:shadow-lg transition-shadow">
        <div class="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
          <svg class="w-7 h-7 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <h3 class="text-xl font-display font-semibold text-text mb-3">Fast Performance</h3>
        <p class="text-text-muted">Lightning-fast load times for optimal user experience.</p>
      </div>
      <!-- Repeat for more features -->
    </div>
  </div>
</section>
```

### Pattern 3: Testimonial Section

```html
<section class="py-20 px-4 bg-surface">
  <div class="max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <h2 class="text-4xl font-display font-bold text-text mb-4">What Our Customers Say</h2>
      <p class="text-xl text-text-muted">Trusted by thousands worldwide</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Testimonial Card -->
      <div class="bg-background rounded-xl p-8">
        <div class="flex items-center gap-1 mb-4">
          <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
          </svg>
          <!-- Repeat for 5 stars -->
        </div>
        <p class="text-text mb-6">"This product has completely transformed how we work. Highly recommended!"</p>
        <div class="flex items-center gap-3">
          <img src="avatar.jpg" alt="Customer name" class="w-12 h-12 rounded-full">
          <div>
            <p class="font-semibold text-text">John Doe</p>
            <p class="text-sm text-text-muted">CEO, Company</p>
          </div>
        </div>
      </div>
      <!-- Repeat for more testimonials -->
    </div>
  </div>
</section>
```

---

## Usage Guidelines

1. **Customize Colors**: Replace `bg-primary`, `text-primary`, etc. with your theme's color system
2. **Adjust Spacing**: Modify padding (`p-*`) and margins (`m-*`) to match your design
3. **Responsive Breakpoints**: Use `sm:`, `md:`, `lg:`, `xl:`, `2xl:` prefixes for responsive design
4. **Accessibility**: Always include `aria-label`, `alt` text, and focus states
5. **Dark Mode**: Add `dark:` prefix for dark mode variants (e.g., `dark:bg-gray-800`)

## Component Checklist

When creating a new component, ensure:

- [ ] Mobile-first responsive design
- [ ] Hover and focus states defined
- [ ] ARIA labels for accessibility
- [ ] Consistent with theme design tokens
- [ ] Semantic HTML elements used
- [ ] Touch targets minimum 44x44px
- [ ] Color contrast meets WCAG AA
- [ ] Keyboard navigation supported
