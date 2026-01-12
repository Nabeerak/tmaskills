#!/usr/bin/env python3
"""
Component Builder Script

Creates individual components in specified theme with HTML/Tailwind markup.

Usage:
    python component_builder.py --component button --variant primary --output ./components
    python component_builder.py --component card --variant pricing --output ./components
    python component_builder.py --list  # List available components
"""

import argparse
import sys
from pathlib import Path
from typing import Dict


# Component templates
COMPONENTS = {
    "button": {
        "description": "Interactive button component",
        "variants": {
            "primary": """<button class="px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors">
  Primary Button
</button>""",
            "secondary": """<button class="px-6 py-3 bg-secondary text-white font-semibold rounded-lg hover:bg-secondary/90 focus:outline-none focus:ring-2 focus:ring-secondary focus:ring-offset-2 transition-colors">
  Secondary Button
</button>""",
            "outline": """<button class="px-6 py-3 border-2 border-primary text-primary font-semibold rounded-lg hover:bg-primary hover:text-white focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-all">
  Outline Button
</button>""",
            "ghost": """<button class="px-6 py-3 text-primary font-semibold rounded-lg hover:bg-primary/10 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors">
  Ghost Button
</button>""",
            "icon": """<button class="px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors flex items-center gap-2">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
  </svg>
  Button with Icon
</button>"""
        }
    },
    "card": {
        "description": "Content container component",
        "variants": {
            "basic": """<div class="bg-surface rounded-xl shadow-md p-6">
  <h3 class="text-xl font-display font-semibold text-text mb-2">Card Title</h3>
  <p class="text-text-muted">Card content goes here with a brief description.</p>
</div>""",
            "product": """<div class="bg-surface rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
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
</div>""",
            "blog": """<article class="bg-surface rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
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
</article>""",
            "pricing": """<div class="bg-surface rounded-xl shadow-lg p-8 border-2 border-transparent hover:border-primary transition-colors">
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
  </ul>
  <button class="w-full px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors">
    Get Started
  </button>
</div>"""
        }
    },
    "form": {
        "description": "Form input components",
        "variants": {
            "text": """<div class="mb-4">
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
</div>""",
            "textarea": """<div class="mb-4">
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
</div>""",
            "select": """<div class="mb-4">
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
</div>""",
            "checkbox": """<div class="flex items-start gap-2 mb-4">
  <input
    type="checkbox"
    id="terms"
    name="terms"
    class="w-4 h-4 mt-1 text-primary border-gray-300 rounded focus:ring-2 focus:ring-primary"
  >
  <label for="terms" class="text-sm text-text">
    I agree to the <a href="#" class="text-primary hover:underline">Terms and Conditions</a>
  </label>
</div>""",
            "radio": """<fieldset class="mb-4">
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
</fieldset>"""
        }
    },
    "navigation": {
        "description": "Navigation components",
        "variants": {
            "header": """<header class="bg-surface shadow-sm sticky top-0 z-50">
  <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <div class="flex-shrink-0">
        <a href="/" class="text-2xl font-display font-bold text-primary">Brand</a>
      </div>
      <div class="hidden md:flex items-center space-x-8">
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Home</a>
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Features</a>
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Pricing</a>
        <a href="#" class="text-text hover:text-primary font-medium transition-colors">Contact</a>
      </div>
      <div class="hidden md:flex items-center space-x-4">
        <a href="#" class="px-6 py-2 bg-primary text-white font-semibold rounded-lg hover:bg-primary/90 transition-colors">
          Get Started
        </a>
      </div>
    </div>
  </nav>
</header>""",
            "sidebar": """<aside class="w-64 bg-surface border-r border-gray-200 h-screen sticky top-0">
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
        </svg>
        Analytics
      </a>
    </nav>
  </div>
</aside>"""
        }
    },
    "hero": {
        "description": "Hero section components",
        "variants": {
            "centered": """<section class="py-20 px-4 bg-background">
  <div class="max-w-4xl mx-auto text-center">
    <h1 class="text-5xl md:text-6xl lg:text-7xl font-display font-bold text-text mb-6 leading-tight">
      Build Amazing Websites
    </h1>
    <p class="text-xl md:text-2xl text-text-muted mb-8 max-w-2xl mx-auto">
      Create beautiful, responsive web designs with our powerful theme builder.
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
</section>""",
            "split": """<section class="py-20 px-4 bg-background">
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
      </div>
    </div>
    <div>
      <img src="hero-image.jpg" alt="Product screenshot" class="rounded-xl shadow-2xl">
    </div>
  </div>
</section>"""
        }
    },
    "cta": {
        "description": "Call-to-action components",
        "variants": {
            "inline": """<div class="bg-primary rounded-xl p-8 text-center text-white">
  <h3 class="text-3xl font-display font-bold mb-4">Ready to Get Started?</h3>
  <p class="text-lg mb-6 opacity-90">Join thousands of satisfied customers today.</p>
  <button class="px-8 py-3 bg-white text-primary font-semibold rounded-lg hover:bg-gray-100 transition-colors">
    Sign Up Now
  </button>
</div>""",
            "banner": """<section class="bg-gradient-to-r from-primary to-secondary py-16 px-4">
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
</section>"""
        }
    },
    "footer": {
        "description": "Footer components",
        "variants": {
            "simple": """<footer class="bg-surface border-t border-gray-200 py-8 px-4">
  <div class="max-w-7xl mx-auto text-center">
    <p class="text-text-muted mb-4">&copy; 2024 Your Company. All rights reserved.</p>
    <div class="flex justify-center gap-6">
      <a href="#" class="text-text-muted hover:text-primary transition-colors">Privacy Policy</a>
      <a href="#" class="text-text-muted hover:text-primary transition-colors">Terms of Service</a>
      <a href="#" class="text-text-muted hover:text-primary transition-colors">Contact</a>
    </div>
  </div>
</footer>""",
            "multi-column": """<footer class="bg-surface border-t border-gray-200 py-12 px-4">
  <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
    <div>
      <h3 class="text-2xl font-display font-bold text-primary mb-4">Brand</h3>
      <p class="text-text-muted">Building amazing web experiences.</p>
    </div>
    <div>
      <h4 class="font-semibold text-text mb-4">Product</h4>
      <ul class="space-y-2">
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Features</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Pricing</a></li>
      </ul>
    </div>
    <div>
      <h4 class="font-semibold text-text mb-4">Company</h4>
      <ul class="space-y-2">
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">About</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Blog</a></li>
      </ul>
    </div>
    <div>
      <h4 class="font-semibold text-text mb-4">Legal</h4>
      <ul class="space-y-2">
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Privacy</a></li>
        <li><a href="#" class="text-text-muted hover:text-primary transition-colors">Terms</a></li>
      </ul>
    </div>
  </div>
  <div class="border-t border-gray-200 pt-8">
    <div class="max-w-7xl mx-auto text-center">
      <p class="text-text-muted">&copy; 2024 Your Company. All rights reserved.</p>
    </div>
  </div>
</footer>"""
        }
    }
}


def main():
    parser = argparse.ArgumentParser(
        description="Create individual components with HTML/Tailwind markup"
    )
    parser.add_argument(
        "--component",
        choices=list(COMPONENTS.keys()),
        help="Component type to generate"
    )
    parser.add_argument(
        "--variant",
        help="Component variant"
    )
    parser.add_argument(
        "--output",
        default="./components",
        help="Output directory (default: ./components)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available components and variants"
    )

    args = parser.parse_args()

    # List components
    if args.list:
        print("\nAvailable Components:\n")
        for comp_name, comp_data in COMPONENTS.items():
            print(f"  {comp_name:15} - {comp_data['description']}")
            print(f"                   Variants: {', '.join(comp_data['variants'].keys())}\n")
        return

    # Validate inputs
    if not args.component:
        parser.print_help()
        print("\n❌ Error: --component is required (or use --list)")
        sys.exit(1)

    component_data = COMPONENTS[args.component]

    if not args.variant:
        print(f"\n❌ Error: --variant is required")
        print(f"Available variants for {args.component}: {', '.join(component_data['variants'].keys())}")
        sys.exit(1)

    if args.variant not in component_data["variants"]:
        print(f"\n❌ Error: Unknown variant '{args.variant}'")
        print(f"Available variants: {', '.join(component_data['variants'].keys())}")
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate component file
    component_html = component_data["variants"][args.variant]
    filename = f"{args.component}-{args.variant}.html"
    output_file = output_dir / filename

    # Wrap in complete HTML
    complete_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{args.component.title()} - {args.variant.title()}</title>
  <link rel="stylesheet" href="../theme.css">
</head>
<body class="bg-background text-text p-8">
  <h1 class="text-3xl font-bold mb-8">{args.component.title()} - {args.variant.title()}</h1>

  <!-- Component -->
  {component_html}

</body>
</html>
"""

    output_file.write_text(complete_html)

    print(f"\n✅ Component generated: {output_file.absolute()}")
    print(f"\n📝 To use this component:")
    print(f"   1. Open {filename} in your browser to preview")
    print(f"   2. Copy the HTML markup to your project")
    print(f"   3. Customize the content and styling as needed\n")


if __name__ == "__main__":
    main()
