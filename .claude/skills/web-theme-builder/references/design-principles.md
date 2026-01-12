# Design Principles Reference

Complete guide to design theory and when to use each of the 8 theme variations.

## Table of Contents

1. [Core Design Principles](#core-design-principles)
2. [Theme Selection Guide](#theme-selection-guide)
3. [Color Theory](#color-theory)
4. [Typography Principles](#typography-principles)
5. [Layout Principles](#layout-principles)
6. [Visual Hierarchy](#visual-hierarchy)
7. [White Space](#white-space)
8. [Consistency](#consistency)
9. [User Experience](#user-experience)
10. [Industry-Specific Patterns](#industry-specific-patterns)

---

## Core Design Principles

### 1. Contrast

Create visual interest and guide attention through contrast.

**Types of Contrast:**
- **Size**: Large headlines vs. small body text
- **Color**: Dark text on light background
- **Weight**: Bold vs. regular font weights
- **Space**: Dense vs. spacious layouts
- **Shape**: Round vs. angular elements

**Example:**
```html
<!-- High contrast hero -->
<section class="bg-black text-white py-24">
  <h1 class="text-7xl font-bold mb-4">Bold Statement</h1>
  <p class="text-xl font-light opacity-80">Subtle supporting text</p>
</section>
```

### 2. Repetition

Build consistency and strengthen unity through repeated elements.

**What to Repeat:**
- Color palette
- Font families
- Button styles
- Spacing values
- Border radius
- Icon style

**Example:**
```css
/* Repeated button style throughout site */
.btn {
  @apply px-6 py-3 rounded-lg font-semibold transition-colors;
}

.btn-primary {
  @apply btn bg-primary text-white hover:bg-primary-dark;
}
```

### 3. Alignment

Create clean, organized layouts through intentional alignment.

**Alignment Types:**
- **Edge alignment**: Elements align to same edge
- **Center alignment**: Elements centered on axis
- **Baseline alignment**: Text aligns on baseline

**Example:**
```html
<!-- Strong left alignment -->
<div class="max-w-4xl mx-auto">
  <h1 class="text-6xl font-bold mb-4">Title</h1>
  <p class="text-xl mb-8">Subtitle aligned to same left edge</p>
  <button class="px-8 py-3">Button also left-aligned</button>
</div>
```

### 4. Proximity

Group related items together to show relationships.

**Principle**: Items close together are perceived as related.

**Example:**
```html
<!-- Good grouping -->
<div class="space-y-12">
  <!-- Group 1: Related items close together -->
  <div class="space-y-2">
    <h3 class="text-2xl font-bold">Feature Name</h3>
    <p class="text-gray-600">Feature description</p>
  </div>

  <!-- Group 2: Separated by more space to show it's different -->
  <div class="space-y-2">
    <h3 class="text-2xl font-bold">Another Feature</h3>
    <p class="text-gray-600">Different feature description</p>
  </div>
</div>
```

### 5. Balance

Distribute visual weight evenly across the design.

**Types:**
- **Symmetrical**: Mirror image (formal, stable)
- **Asymmetrical**: Different but balanced (dynamic, modern)
- **Radial**: Elements radiate from center

**Example:**
```html
<!-- Asymmetrical balance -->
<div class="grid grid-cols-12 gap-8">
  <div class="col-span-7">
    <!-- Larger left section with lighter content -->
    <img src="large-image.jpg" class="w-full opacity-90">
  </div>
  <div class="col-span-5">
    <!-- Smaller right section with heavier (darker) content -->
    <div class="bg-black text-white p-12">
      <h2>Balanced by color weight</h2>
    </div>
  </div>
</div>
```

---

## Theme Selection Guide

### 1. Modern/Minimalist

**When to Use:**
- SaaS products
- Tech startups
- Design agencies
- Apps emphasizing simplicity

**Design Characteristics:**
- Maximum whitespace (breathing room)
- Monochromatic color scheme
- Sans-serif typography
- Subtle shadows and borders
- Clean geometric shapes
- Minimal decorative elements

**Psychology:**
- Conveys sophistication and professionalism
- Builds trust through clarity
- Appeals to design-conscious users
- Reduces cognitive load

**Color Palette:**
```css
--color-primary: 0 0% 10%;      /* Near black */
--color-secondary: 0 0% 30%;    /* Dark gray */
--color-background: 0 0% 100%;  /* White */
--color-surface: 0 0% 98%;      /* Off-white */
--color-text: 0 0% 10%;         /* Near black */
```

**Typography:**
- Display: Inter, SF Pro Display, Helvetica Neue
- Text: Inter, SF Pro Text, system-ui
- Weight contrast: Light (300) vs Bold (700)

**Examples:**
- Apple.com
- Stripe.com
- Linear.app

---

### 2. Corporate/Professional

**When to Use:**
- Enterprise software
- Financial services
- Consulting firms
- B2B products
- Law firms
- Healthcare

**Design Characteristics:**
- Trust-building blue hues
- Structured grid layouts
- Conservative typography
- High contrast for readability
- Professional imagery
- Clear hierarchy

**Psychology:**
- Establishes credibility and authority
- Conveys stability and reliability
- Appeals to decision-makers
- Professional and serious tone

**Color Palette:**
```css
--color-primary: 220 90% 56%;   /* Professional blue */
--color-secondary: 220 70% 45%; /* Darker blue */
--color-accent: 210 80% 60%;    /* Light blue */
--color-background: 0 0% 100%;  /* White */
--color-surface: 210 20% 98%;   /* Blue-tinted white */
```

**Typography:**
- Display: Inter, Roboto, Open Sans
- Text: Inter, Roboto, system-ui
- Weight: Medium (500) and Semibold (600)
- Formal and readable

**Examples:**
- IBM.com
- Microsoft.com
- Salesforce.com

---

### 3. Creative/Bold

**When to Use:**
- Creative agencies
- Art galleries
- Entertainment industry
- Events and conferences
- Fashion brands
- Startups wanting to stand out

**Design Characteristics:**
- Vibrant, saturated colors
- Experimental layouts
- Unique typography
- Unexpected animations
- Asymmetrical designs
- High energy and contrast

**Psychology:**
- Captures attention and stands out
- Expresses creativity and innovation
- Appeals to younger demographics
- Memorable and distinctive

**Color Palette:**
```css
--color-primary: 280 100% 50%;  /* Vibrant purple */
--color-secondary: 340 100% 60%; /* Bright pink */
--color-accent: 45 100% 50%;    /* Electric yellow */
--color-background: 0 0% 100%;  /* White */
--color-text: 0 0% 10%;         /* Near black */
```

**Typography:**
- Display: Space Grotesk, Poppins, Montserrat (bold, expressive)
- Text: Inter, Work Sans
- Large, bold headings
- Varied font sizes for visual interest

**Examples:**
- Awwwards.com winners
- Dribbble showcases
- Creative agency portfolios

---

### 4. Dark/Tech

**When to Use:**
- Developer tools
- Gaming platforms
- Tech products
- Code editors
- Crypto/blockchain
- Modern SaaS dashboards

**Design Characteristics:**
- Dark backgrounds (black, dark gray)
- Neon or bright accent colors
- Monospace or tech fonts
- Futuristic aesthetic
- Glowing effects
- High contrast

**Psychology:**
- Appeals to technical users
- Reduces eye strain in dark environments
- Modern and cutting-edge feeling
- Gaming and hacker aesthetic

**Color Palette:**
```css
--color-primary: 180 100% 50%;  /* Cyan */
--color-secondary: 280 100% 60%; /* Purple */
--color-accent: 330 100% 60%;   /* Pink */
--color-background: 220 20% 10%; /* Very dark blue */
--color-surface: 220 18% 15%;   /* Dark surface */
--color-text: 0 0% 95%;         /* Off-white */
```

**Typography:**
- Display: JetBrains Mono, Fira Code, Inconsolata
- Text: Inter, Roboto, system-ui
- Monospace for technical feel

**Examples:**
- GitHub.com (dark mode)
- Vercel.com
- Discord.com

---

### 5. Warm/Friendly

**When to Use:**
- Community platforms
- Education and learning
- Wellness and health
- Lifestyle brands
- Non-profits
- Family-oriented services

**Design Characteristics:**
- Warm colors (oranges, reds, yellows)
- Soft, rounded corners
- Approachable imagery
- Friendly tone
- Organic shapes
- Inviting whitespace

**Psychology:**
- Builds warmth and trust
- Creates welcoming atmosphere
- Approachable and human
- Encourages engagement

**Color Palette:**
```css
--color-primary: 25 95% 53%;    /* Warm orange */
--color-secondary: 340 75% 55%; /* Soft pink */
--color-accent: 45 100% 50%;    /* Warm yellow */
--color-background: 35 100% 98%; /* Warm white */
--color-surface: 30 50% 96%;    /* Cream */
--color-text: 20 20% 20%;       /* Warm black */
```

**Typography:**
- Display: Nunito, Quicksand, Comfortaa (rounded, friendly)
- Text: Inter, Open Sans, Lato
- Rounded letterforms

**Examples:**
- Airbnb.com
- Mailchimp.com
- Etsy.com

---

### 6. E-commerce/Product

**When to Use:**
- Online stores
- Product showcases
- Retail websites
- Marketplace platforms
- Product landing pages

**Design Characteristics:**
- Product-focused layouts
- Clear CTAs and pricing
- Trust signals (reviews, badges)
- Clean product imagery
- Conversion optimization
- Shopping cart prominence

**Psychology:**
- Drives purchasing decisions
- Builds trust and credibility
- Reduces friction in buying process
- Clear value proposition

**Color Palette:**
```css
--color-primary: 142 71% 45%;   /* Trust green for CTAs */
--color-secondary: 210 90% 56%; /* Blue for secondary actions */
--color-accent: 0 100% 60%;     /* Red for urgency/sales */
--color-background: 0 0% 100%;  /* Clean white */
--color-surface: 0 0% 97%;      /* Light gray */
--color-text: 0 0% 10%;         /* Black text */
```

**Typography:**
- Display: Inter, Roboto, Open Sans
- Text: Inter, system-ui
- Clear, readable prices and CTAs
- Product names stand out

**Examples:**
- Amazon product pages
- Shopify stores
- Nike.com

---

### 7. SaaS/Dashboard

**When to Use:**
- Software dashboards
- Data applications
- Admin panels
- Productivity tools
- Analytics platforms
- Project management tools

**Design Characteristics:**
- Data visualization friendly
- Clean, organized interfaces
- Clear information hierarchy
- Sidebar navigation
- Card-based layouts
- Neutral, non-distracting colors

**Psychology:**
- Promotes productivity
- Reduces cognitive load
- Organizes complex information
- Professional and functional

**Color Palette:**
```css
--color-primary: 220 90% 56%;   /* Blue for primary actions */
--color-secondary: 260 60% 60%; /* Purple for secondary */
--color-success: 142 71% 45%;   /* Green for success states */
--color-warning: 38 92% 50%;    /* Orange for warnings */
--color-error: 0 84% 60%;       /* Red for errors */
--color-background: 0 0% 98%;   /* Off-white */
--color-surface: 0 0% 100%;     /* White cards */
--color-text: 0 0% 10%;         /* Near black */
```

**Typography:**
- Display: Inter, Roboto, system-ui
- Text: Inter, system-ui
- Tabular numbers for data
- Clear hierarchy

**Examples:**
- Notion.com
- Figma.com
- Asana.com

---

### 8. Portfolio/Personal

**When to Use:**
- Personal websites
- Designer portfolios
- Photographer showcases
- Freelancer sites
- Creative professionals
- Personal brands

**Design Characteristics:**
- Personality-driven
- Unique layouts
- Showcase work prominently
- Storytelling elements
- Personal photography
- Custom details

**Psychology:**
- Expresses individuality
- Showcases creativity
- Builds personal connection
- Memorable and unique

**Color Palette:**
```css
/* Varies greatly based on personal brand */
/* Example: */
--color-primary: 280 70% 55%;   /* Personal brand color */
--color-secondary: 340 60% 50%; /* Complementary */
--color-background: 0 0% 100%;  /* White or black */
--color-text: 0 0% 10%;         /* High contrast text */
```

**Typography:**
- Display: Choose font that reflects personality
- Text: Readable, complements display font
- May use decorative fonts for impact

**Examples:**
- Designer portfolios on Dribbble
- Photographer personal sites
- Creative professional portfolios

---

## Color Theory

### Color Psychology

**Red (0-10° hue):**
- Energy, passion, urgency
- Use: CTAs, sales, food, warnings
- Avoid: Healthcare (anxiety), finance (danger)

**Orange (11-40° hue):**
- Friendly, creative, affordable
- Use: E-commerce, creative, youth brands
- Avoid: Corporate (too casual), luxury

**Yellow (41-70° hue):**
- Optimism, clarity, warmth
- Use: Accents, highlights, food
- Avoid: Primary color (hard on eyes)

**Green (71-170° hue):**
- Growth, health, success, money
- Use: Finance, health, environment, CTAs
- Avoid: Tech (traditional), creative (safe)

**Blue (171-260° hue):**
- Trust, professionalism, calm
- Use: Corporate, finance, healthcare, tech
- Avoid: Food (suppresses appetite)

**Purple (261-300° hue):**
- Luxury, creativity, spirituality
- Use: Beauty, creative, premium products
- Avoid: Corporate (too playful), budget brands

**Pink (301-330° hue):**
- Feminine, playful, modern
- Use: Beauty, fashion, youth brands
- Avoid: Masculine brands, serious topics

**Grayscale:**
- Neutral, sophisticated, timeless
- Use: Minimalist designs, backgrounds
- Pair with accent color for interest

### Color Harmony

**Monochromatic:**
- Single hue with varying lightness/saturation
- Simple, cohesive, elegant
- Example: `hsl(220, 90%, [30%, 50%, 70%])`

**Analogous:**
- Colors next to each other on color wheel
- Harmonious, natural
- Example: `hsl([200, 220, 240], 90%, 50%)`

**Complementary:**
- Opposite colors on wheel
- High contrast, vibrant
- Example: `hsl(220, 90%, 50%)` + `hsl(40, 90%, 50%)`

**Triadic:**
- Three colors evenly spaced
- Vibrant, balanced
- Example: `hsl([0, 120, 240], 90%, 50%)`

### Color Application (60-30-10 Rule)

- **60%**: Dominant color (usually neutral background)
- **30%**: Secondary color (surfaces, sections)
- **10%**: Accent color (CTAs, highlights)

**Example:**
```css
/* 60% - Background and large areas */
--color-background: 0 0% 98%;

/* 30% - Secondary surfaces */
--color-surface: 220 20% 95%;

/* 10% - Accent for CTAs and highlights */
--color-primary: 220 90% 56%;
```

---

## Typography Principles

### Font Pairing

**Contrast Pairing:**
- Display: Bold, distinctive
- Text: Neutral, readable
- Example: Playfair Display + Inter

**Similar Pairing:**
- Both fonts from same family
- Vary weight and size for hierarchy
- Example: Inter (all weights)

**Classic Pairing:**
- Serif + Sans-serif
- Traditional and readable
- Example: Georgia + Arial

### Font Selection Criteria

**Display Font (Headlines):**
- Strong personality
- Unique and memorable
- Large size readability
- Brand alignment

**Text Font (Body):**
- High readability
- Works at small sizes
- Neutral personality
- Multiple weights available

### Type Scale

Use consistent scale for harmony:

**Major Third (1.25 ratio):**
```
Base: 16px
Scale: 12.8, 16, 20, 25, 31.25, 39.06, 48.83, 61.04, 76.29
```

**Perfect Fourth (1.333 ratio):**
```
Base: 16px
Scale: 12, 16, 21, 28, 37, 50, 67, 89, 118
```

**Golden Ratio (1.618 ratio):**
```
Base: 16px
Scale: 10, 16, 26, 42, 68, 110
```

### Readability Guidelines

**Line Length:**
- Optimal: 50-75 characters per line
- Use `max-width: 65ch` for long-form content

**Line Height:**
- Body text: 1.5-1.75
- Headings: 1.1-1.3
- Adjust based on font and line length

**Font Size:**
- Minimum for body text: 16px (mobile), 18px (desktop)
- Headings: At least 2x body text size for clear hierarchy

**Letter Spacing:**
- Uppercase text: +0.05em to +0.1em
- Normal case: Use font default
- Large headings: -0.02em for tighter look

---

## Layout Principles

### Grid Systems

**12-Column Grid:**
- Most flexible
- Easy math for divisions
- Works for most layouts

**8-Column Grid:**
- Simpler than 12
- Good for content-heavy sites

**Custom Columns:**
- Based on content needs
- May vary per breakpoint

### Layout Patterns

**F-Pattern:**
- Users scan top and left
- Place important content there
- Good for text-heavy pages

**Z-Pattern:**
- Eye moves in Z shape
- Good for landing pages
- Logo → CTA → Content → Footer

**Centered Layout:**
- Single column
- Focused attention
- Good for simple messages

**Split Screen:**
- Two equal sections
- Dual content
- Modern aesthetic

---

## Visual Hierarchy

### Size

Larger = More important

```html
<h1 class="text-6xl">Most important</h1>
<h2 class="text-4xl">Secondary</h2>
<p class="text-base">Body text</p>
```

### Weight

Bolder = More important

```html
<h3 class="font-bold">Important heading</h3>
<p class="font-normal">Normal text</p>
<p class="font-light">De-emphasized text</p>
```

### Color

High contrast = More important

```html
<h1 class="text-black">High contrast heading</h1>
<p class="text-gray-600">Lower contrast body</p>
<small class="text-gray-400">Least important</small>
```

### Position

Top and left = More important (F-pattern)

### Spacing

More space around = More important

```html
<h1 class="text-6xl mb-12">Lots of space = important</h1>
<p class="mb-4">Less space = less important</p>
```

---

## White Space

### Why White Space Matters

- Reduces cognitive load
- Improves readability
- Creates elegance and sophistication
- Draws attention to content
- Improves comprehension

### Types of White Space

**Macro White Space:**
- Between sections
- Page margins
- Large breathing room

**Micro White Space:**
- Between lines (line-height)
- Between letters (letter-spacing)
- Between paragraphs

### White Space Guidelines

**Generous (Minimalist/Modern):**
```html
<section class="py-32 px-8">
  <h1 class="text-7xl mb-12">Title</h1>
  <p class="text-xl leading-relaxed">Content</p>
</section>
```

**Moderate (Corporate):**
```html
<section class="py-20 px-6">
  <h1 class="text-5xl mb-8">Title</h1>
  <p class="text-lg leading-normal">Content</p>
</section>
```

**Compact (E-commerce/Dashboard):**
```html
<section class="py-12 px-4">
  <h1 class="text-4xl mb-6">Title</h1>
  <p class="text-base leading-snug">Content</p>
</section>
```

---

## Consistency

### What to Keep Consistent

1. **Colors**: Use defined palette exclusively
2. **Typography**: Same fonts throughout
3. **Spacing**: Consistent spacing scale
4. **Border Radius**: Same rounding values
5. **Shadows**: Same shadow styles
6. **Icons**: Same style and weight
7. **Button Styles**: Consistent across site
8. **Imagery**: Same style and treatment

### Design System

Create reusable components:

```css
/* Buttons */
.btn { @apply px-6 py-3 rounded-lg font-semibold; }
.btn-primary { @apply btn bg-primary text-white; }
.btn-secondary { @apply btn border-2 border-primary text-primary; }

/* Cards */
.card { @apply bg-white rounded-xl shadow-md p-6; }

/* Spacing */
.section { @apply py-20 px-4; }
```

---

## User Experience

### Cognitive Load

Reduce mental effort required:
- Clear navigation
- Consistent patterns
- Progressive disclosure
- Meaningful defaults
- Clear feedback

### Affordances

Design suggests how to use it:
- Buttons look clickable (shadows, colors)
- Links are underlined or distinct
- Input fields look like input fields
- Icons are recognizable

### Feedback

Provide clear responses to actions:
- Hover states on interactive elements
- Active/focused states
- Loading indicators
- Success/error messages
- Disabled states look disabled

---

## Industry-Specific Patterns

### SaaS/Tech
- Clean, minimal
- Blue color schemes
- Data visualization
- Free trial CTAs

### E-commerce
- Large product images
- Clear pricing
- Trust signals
- Prominent cart

### Healthcare
- Calming colors (blue, green)
- Trust and credibility
- Clear information hierarchy
- Accessibility critical

### Finance
- Professional blue
- Trust signals
- Data tables
- Security indicators

### Education
- Friendly, approachable
- Clear structure
- Progress indicators
- Interactive elements

### Creative/Agency
- Bold, unique
- Portfolio showcase
- Experimental layouts
- Personality-driven

---

## Quick Decision Tree

**Start here**: What's your primary goal?

**Build trust & credibility** → Corporate/Professional
**Stand out & be memorable** → Creative/Bold
**Simplicity & elegance** → Modern/Minimalist
**Technical/developer audience** → Dark/Tech
**Community & warmth** → Warm/Friendly
**Sell products** → E-commerce
**Organize complex data** → SaaS/Dashboard
**Showcase work** → Portfolio

**Next question**: What industry?

**Tech/SaaS** → Modern/Minimalist or SaaS/Dashboard
**Finance/Enterprise** → Corporate/Professional
**Creative/Agency** → Creative/Bold or Portfolio
**Gaming/Developer tools** → Dark/Tech
**Education/Non-profit** → Warm/Friendly
**Retail/Marketplace** → E-commerce

**Final question**: What age demographic?

**18-25** → Creative/Bold or Dark/Tech
**25-40** → Modern/Minimalist or SaaS/Dashboard
**40-60** → Corporate/Professional
**All ages** → Warm/Friendly

---

## Summary

Great design is:
- **Purposeful**: Every element serves a function
- **Consistent**: Patterns repeat throughout
- **Clear**: Hierarchy guides the eye
- **Accessible**: Usable by everyone
- **Balanced**: Visual weight distributed evenly
- **Appropriate**: Matches brand and audience

Choose your theme based on:
1. Industry and audience
2. Brand personality
3. User goals
4. Content type
5. Competitive landscape

Remember: **Design is not decoration; it's communication.**
