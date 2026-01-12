#!/usr/bin/env python3
"""
Theme Generator Script

Generates complete theme boilerplate with chosen aesthetic style.
Supports all 8 theme variations with Tailwind CSS v4.0 @theme configuration.

Usage:
    python theme_generator.py --theme modern --output ./my-theme
    python theme_generator.py --theme corporate --dark-mode --output ./corporate-theme
    python theme_generator.py --list  # List available themes
"""

import argparse
from datetime import datetime
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any


# Theme configurations
THEMES = {
    "modern": {
        "name": "Modern/Minimalist",
        "description": "Maximum whitespace, monochromatic colors, clean typography",
        "colors": {
            "primary": "0 0% 10%",
            "secondary": "0 0% 30%",
            "accent": "0 0% 50%",
            "background": "0 0% 100%",
            "surface": "0 0% 98%",
            "text": "0 0% 10%",
            "text-muted": "0 0% 45%"
        },
        "fonts": {
            "display": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "text": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
        },
        "radius": {
            "sm": "0.125rem",
            "md": "0.25rem",
            "lg": "0.375rem"
        }
    },
    "corporate": {
        "name": "Corporate/Professional",
        "description": "Trust-building blues, structured layouts, professional",
        "colors": {
            "primary": "220 90% 56%",
            "secondary": "220 70% 45%",
            "accent": "210 80% 60%",
            "background": "0 0% 100%",
            "surface": "210 20% 98%",
            "text": "220 30% 15%",
            "text-muted": "220 15% 50%"
        },
        "fonts": {
            "display": "'Inter', 'Roboto', sans-serif",
            "text": "'Inter', sans-serif"
        },
        "radius": {
            "sm": "0.25rem",
            "md": "0.5rem",
            "lg": "0.75rem"
        }
    },
    "creative": {
        "name": "Creative/Bold",
        "description": "Vibrant colors, experimental layouts, high energy",
        "colors": {
            "primary": "280 100% 50%",
            "secondary": "340 100% 60%",
            "accent": "45 100% 50%",
            "background": "0 0% 100%",
            "surface": "0 0% 98%",
            "text": "0 0% 10%",
            "text-muted": "0 0% 45%"
        },
        "fonts": {
            "display": "'Space Grotesk', 'Poppins', sans-serif",
            "text": "'Inter', 'Work Sans', sans-serif"
        },
        "radius": {
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem"
        }
    },
    "dark": {
        "name": "Dark/Tech",
        "description": "Dark backgrounds, neon accents, futuristic",
        "colors": {
            "primary": "180 100% 50%",
            "secondary": "280 100% 60%",
            "accent": "330 100% 60%",
            "background": "220 20% 10%",
            "surface": "220 18% 15%",
            "text": "0 0% 95%",
            "text-muted": "0 0% 60%"
        },
        "fonts": {
            "display": "'JetBrains Mono', 'Fira Code', monospace",
            "text": "'Inter', sans-serif"
        },
        "radius": {
            "sm": "0.125rem",
            "md": "0.25rem",
            "lg": "0.5rem"
        }
    },
    "warm": {
        "name": "Warm/Friendly",
        "description": "Warm colors, rounded corners, inviting",
        "colors": {
            "primary": "25 95% 53%",
            "secondary": "340 75% 55%",
            "accent": "45 100% 50%",
            "background": "35 100% 98%",
            "surface": "30 50% 96%",
            "text": "20 20% 20%",
            "text-muted": "20 10% 50%"
        },
        "fonts": {
            "display": "'Nunito', 'Quicksand', sans-serif",
            "text": "'Inter', 'Open Sans', sans-serif"
        },
        "radius": {
            "sm": "0.5rem",
            "md": "0.75rem",
            "lg": "1rem"
        }
    },
    "ecommerce": {
        "name": "E-commerce/Product",
        "description": "Product-focused, clear CTAs, conversion-optimized",
        "colors": {
            "primary": "142 71% 45%",
            "secondary": "210 90% 56%",
            "accent": "0 100% 60%",
            "background": "0 0% 100%",
            "surface": "0 0% 97%",
            "text": "0 0% 10%",
            "text-muted": "0 0% 45%"
        },
        "fonts": {
            "display": "'Inter', 'Roboto', sans-serif",
            "text": "'Inter', system-ui, sans-serif"
        },
        "radius": {
            "sm": "0.25rem",
            "md": "0.5rem",
            "lg": "0.75rem"
        }
    },
    "saas": {
        "name": "SaaS/Dashboard",
        "description": "Data-friendly, clean interfaces, organized",
        "colors": {
            "primary": "220 90% 56%",
            "secondary": "260 60% 60%",
            "accent": "142 71% 45%",
            "background": "0 0% 98%",
            "surface": "0 0% 100%",
            "text": "0 0% 10%",
            "text-muted": "0 0% 45%",
            "success": "142 71% 45%",
            "warning": "38 92% 50%",
            "error": "0 84% 60%"
        },
        "fonts": {
            "display": "'Inter', 'Roboto', system-ui, sans-serif",
            "text": "'Inter', system-ui, sans-serif"
        },
        "radius": {
            "sm": "0.25rem",
            "md": "0.375rem",
            "lg": "0.5rem"
        }
    },
    "portfolio": {
        "name": "Portfolio/Personal",
        "description": "Personality-driven, unique layouts, showcase work",
        "colors": {
            "primary": "280 70% 55%",
            "secondary": "340 60% 50%",
            "accent": "180 60% 50%",
            "background": "0 0% 100%",
            "surface": "0 0% 98%",
            "text": "0 0% 10%",
            "text-muted": "0 0% 45%"
        },
        "fonts": {
            "display": "'Playfair Display', 'Merriweather', serif",
            "text": "'Inter', 'Lato', sans-serif"
        },
        "radius": {
            "sm": "0.25rem",
            "md": "0.5rem",
            "lg": "1rem"
        }
    }
}


def generate_theme_css(theme_config: Dict[str, Any], dark_mode: bool = False) -> str:
    """Generate Tailwind CSS v4.0 @theme configuration."""

    css = """@import "tailwindcss";

@theme {
  /* Colors (HSL format) */
"""

    # Add colors
    for color_name, color_value in theme_config["colors"].items():
        css += f"  --color-{color_name}: {color_value};\n"

    css += """
  /* Typography */
"""

    # Add fonts
    for font_type, font_value in theme_config["fonts"].items():
        css += f"  --font-{font_type}: {font_value};\n"

    css += """
  /* Border Radius */
"""

    # Add border radius
    for size, value in theme_config["radius"].items():
        css += f"  --radius-{size}: {value};\n"

    css += """  --radius-full: 9999px;

  /* Spacing (based on 0.25rem = 4px) */
  --spacing-0: 0;
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;
  --spacing-5: 1.25rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
  --spacing-10: 2.5rem;
  --spacing-12: 3rem;
  --spacing-16: 4rem;
  --spacing-20: 5rem;
  --spacing-24: 6rem;
  --spacing-32: 8rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
"""

    # Add dark mode if requested
    if dark_mode:
        css += """
/* Dark Mode */
@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: 220 20% 10%;
    --color-surface: 220 18% 15%;
    --color-text: 0 0% 95%;
    --color-text-muted: 0 0% 60%;
  }
}

.dark {
  --color-background: 220 20% 10%;
  --color-surface: 220 18% 15%;
  --color-text: 0 0% 95%;
  --color-text-muted: 0 0% 60%;
}
"""

    # Add component utilities
    css += """
/* Component Utilities */
@layer components {
  .btn {
    @apply px-6 py-3 rounded-lg font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2;
  }

  .btn-primary {
    @apply btn bg-primary text-white hover:bg-primary/90 focus:ring-primary;
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
"""

    return css


def generate_html_template(theme_name: str) -> str:
    """Generate sample HTML template using the theme."""
    current_year = datetime.now().year

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{THEMES[theme_name]['name']} Theme</title>
  <link rel="stylesheet" href="theme.css">
</head>
<body class="bg-background text-text">
  <!-- Header -->
  <header class="bg-surface shadow-sm sticky top-0 z-50">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex-shrink-0">
          <a href="/" class="text-2xl font-display font-bold text-primary">Brand</a>
        </div>
        <div class="hidden md:flex space-x-8">
          <a href="#" class="text-text hover:text-primary font-medium transition-colors">Home</a>
          <a href="#" class="text-text hover:text-primary font-medium transition-colors">Features</a>
          <a href="#" class="text-text hover:text-primary font-medium transition-colors">Pricing</a>
          <a href="#" class="text-text hover:text-primary font-medium transition-colors">Contact</a>
        </div>
        <div class="hidden md:flex items-center space-x-4">
          <a href="#" class="text-text hover:text-primary font-medium transition-colors">Sign In</a>
          <a href="#" class="btn-primary">Get Started</a>
        </div>
      </div>
    </nav>
  </header>

  <!-- Hero Section -->
  <section class="py-20 px-4 bg-background">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-5xl md:text-6xl lg:text-7xl font-display font-bold text-text mb-6 leading-tight">
        Welcome to {THEMES[theme_name]['name']}
      </h1>
      <p class="text-xl md:text-2xl text-text-muted mb-8 max-w-2xl mx-auto">
        {THEMES[theme_name]['description']}
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="#" class="btn-primary text-lg">Get Started</a>
        <a href="#" class="btn-secondary text-lg">Learn More</a>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="py-20 px-4 bg-surface">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-4xl font-display font-bold text-center mb-12">Features</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div class="card">
          <h3 class="text-xl font-display font-semibold mb-2">Feature One</h3>
          <p class="text-text-muted">Description of the first amazing feature.</p>
        </div>
        <div class="card">
          <h3 class="text-xl font-display font-semibold mb-2">Feature Two</h3>
          <p class="text-text-muted">Description of the second amazing feature.</p>
        </div>
        <div class="card">
          <h3 class="text-xl font-display font-semibold mb-2">Feature Three</h3>
          <p class="text-text-muted">Description of the third amazing feature.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-surface border-t border-gray-200 py-8 px-4">
    <div class="max-w-7xl mx-auto text-center">
      <p class="text-text-muted">&copy; {current_year} Your Company. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
"""


def generate_readme(theme_name: str) -> str:
    """Generate README for the theme."""

    return f"""# {THEMES[theme_name]['name']} Theme

{THEMES[theme_name]['description']}

## Installation

1. Include the theme CSS in your HTML:
   ```html
   <link rel="stylesheet" href="theme.css">
   ```

2. Or import in your CSS:
   ```css
   @import url('theme.css');
   ```

## Usage

### Buttons

```html
<button class="btn-primary">Primary Button</button>
<button class="btn-secondary">Secondary Button</button>
```

### Cards

```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content goes here.</p>
</div>
```

### Forms

```html
<input type="text" class="input" placeholder="Enter text">
```

## Color Palette

{json.dumps(THEMES[theme_name]['colors'], indent=2)}

## Typography

- Display Font: {THEMES[theme_name]['fonts']['display']}
- Text Font: {THEMES[theme_name]['fonts']['text']}

## Customization

Edit `theme.css` to customize colors, fonts, and other design tokens.

## Built With

- Tailwind CSS v4.0
- @theme directive for design tokens

## License

MIT License
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate complete theme boilerplate with chosen aesthetic style"
    )
    parser.add_argument(
        "--theme",
        choices=list(THEMES.keys()),
        help="Theme style to generate"
    )
    parser.add_argument(
        "--output",
        default="./theme-output",
        help="Output directory (default: ./theme-output)"
    )
    parser.add_argument(
        "--dark-mode",
        action="store_true",
        help="Include dark mode support"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available themes"
    )

    args = parser.parse_args()

    # List themes
    if args.list:
        print("\nAvailable Themes:\n")
        for key, theme in THEMES.items():
            print(f"  {key:12} - {theme['name']}")
            print(f"               {theme['description']}\n")
        return

    # Validate theme selection
    if not args.theme:
        parser.print_help()
        print("\n❌ Error: --theme is required (or use --list to see available themes)")
        sys.exit(1)

    theme_config = THEMES[args.theme]
    output_dir = Path(args.output)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🎨 Generating {theme_config['name']} theme...")

    # Generate theme.css
    theme_css = generate_theme_css(theme_config, args.dark_mode)
    (output_dir / "theme.css").write_text(theme_css)
    print(f"✅ Created theme.css")

    # Generate index.html
    index_html = generate_html_template(args.theme)
    (output_dir / "index.html").write_text(index_html)
    print(f"✅ Created index.html")

    # Generate README.md
    readme = generate_readme(args.theme)
    (output_dir / "README.md").write_text(readme)
    print(f"✅ Created README.md")

    # Generate theme-config.json
    config_json = json.dumps(theme_config, indent=2)
    (output_dir / "theme-config.json").write_text(config_json)
    print(f"✅ Created theme-config.json")

    print(f"\n✨ Theme generated successfully in: {output_dir.absolute()}")
    print(f"\n📝 Next steps:")
    print(f"   1. Open {output_dir / 'index.html'} in your browser")
    print(f"   2. Customize colors in theme.css")
    print(f"   3. Build your pages using the component classes\n")


if __name__ == "__main__":
    main()
