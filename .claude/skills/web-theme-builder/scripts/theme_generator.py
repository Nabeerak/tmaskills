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
import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def validate_hsl_color(hsl_string: str) -> bool:
    """
    Validate HSL color format to prevent injection.

    Args:
        hsl_string: HSL color in format "H S% L%" (e.g., "220 90% 56%")

    Returns:
        True if valid, raises ValueError otherwise.
    """
    pattern = r'^\d{1,3}\s+\d{1,3}%\s+\d{1,3}%$'
    if not re.match(pattern, hsl_string):
        raise ValueError(f"Invalid HSL format: '{hsl_string}'. Expected format: 'H S% L%'")

    parts = hsl_string.replace('%', '').split()
    h, s, l = int(parts[0]), int(parts[1]), int(parts[2])

    if not (0 <= h <= 360):
        raise ValueError(f"Hue value {h} out of range (0-360)")
    if not (0 <= s <= 100):
        raise ValueError(f"Saturation value {s} out of range (0-100)")
    if not (0 <= l <= 100):
        raise ValueError(f"Lightness value {l} out of range (0-100)")

    return True


def validate_theme_config(theme_config: Dict[str, Any]) -> bool:
    """
    Validate entire theme configuration.

    Args:
        theme_config: Theme configuration dictionary

    Returns:
        True if valid, raises ValueError otherwise.
    """
    required_keys = ["name", "description", "colors", "fonts", "radius"]
    for key in required_keys:
        if key not in theme_config:
            raise ValueError(f"Missing required key in theme config: {key}")

    # Validate colors
    for color_name, color_value in theme_config["colors"].items():
        try:
            validate_hsl_color(color_value)
        except ValueError as e:
            raise ValueError(f"Invalid color '{color_name}': {e}")

    return True


def safe_write_file(file_path: Path, content: str, description: str) -> bool:
    """
    Safely write content to a file with error handling.

    Args:
        file_path: Path to write to
        content: Content to write
        description: Description for error messages

    Returns:
        True if successful, exits on failure.
    """
    try:
        file_path.write_text(content)
        print(f"✅ Created {description}")
        return True
    except PermissionError:
        print(f"❌ Error: No write permission for {file_path}")
        print(f"   Solution: Check file permissions or choose different output directory")
        sys.exit(1)
    except OSError as e:
        print(f"❌ Error writing {description}: {e}")
        print(f"   Solution: Check disk space and file system permissions")
        sys.exit(1)


def safe_create_directory(dir_path: Path) -> bool:
    """
    Safely create a directory with error handling.

    Args:
        dir_path: Path to create

    Returns:
        True if successful, exits on failure.
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        print(f"❌ Error: No permission to create directory {dir_path}")
        print(f"   Solution: Check directory permissions or choose different location")
        sys.exit(1)
    except OSError as e:
        print(f"❌ Error creating directory {dir_path}: {e}")
        sys.exit(1)


# Theme name mapping to JSON config files
THEME_CONFIG_MAP = {
    "modern": "modern-minimalist.json",
    "corporate": "corporate-professional.json",
    "creative": "creative-bold.json",
    "dark": "dark-tech.json",
    "warm": "warm-friendly.json",
    "ecommerce": "ecommerce-product.json",
    "saas": "saas-dashboard.json",
    "portfolio": "portfolio-personal.json"
}


def get_config_dir() -> Path:
    """Get the path to the theme-configs directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "assets" / "theme-configs"


def load_theme_config(theme_key: str) -> Dict[str, Any]:
    """
    Load theme configuration from JSON file.

    Args:
        theme_key: Theme identifier (e.g., "modern", "corporate")

    Returns:
        Theme configuration dictionary

    Raises:
        ValueError: If theme not found or config invalid
    """
    if theme_key not in THEME_CONFIG_MAP:
        raise ValueError(f"Unknown theme: {theme_key}")

    config_file = get_config_dir() / THEME_CONFIG_MAP[theme_key]

    if not config_file.exists():
        raise ValueError(f"Theme config file not found: {config_file}")

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in theme config {config_file}: {e}")

    # Transform JSON config to expected format
    return transform_json_config(config)


def transform_json_config(json_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform JSON config file format to internal format.

    Args:
        json_config: Raw JSON config from file

    Returns:
        Transformed config in expected format
    """
    return {
        "name": json_config.get("name", "Unknown"),
        "description": json_config.get("description", ""),
        "colors": json_config.get("colors", {}),
        "fonts": {
            "display": json_config.get("typography", {}).get("display", {}).get("family", "sans-serif"),
            "text": json_config.get("typography", {}).get("text", {}).get("family", "sans-serif")
        },
        "radius": json_config.get("borderRadius", {
            "sm": "0.25rem",
            "md": "0.5rem",
            "lg": "0.75rem"
        })
    }


def get_all_themes() -> Dict[str, Dict[str, Any]]:
    """
    Load all available themes.

    Returns:
        Dictionary of theme_key -> theme_config
    """
    themes = {}
    for theme_key in THEME_CONFIG_MAP:
        try:
            themes[theme_key] = load_theme_config(theme_key)
        except ValueError as e:
            print(f"Warning: Could not load theme '{theme_key}': {e}")
    return themes


# Load themes at module level for backwards compatibility
THEMES = get_all_themes()


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
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate theme config without generating files"
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

    # Validate theme configuration
    try:
        validate_theme_config(theme_config)
        if args.validate_only:
            print(f"✅ Theme '{args.theme}' configuration is valid")
            return
    except ValueError as e:
        print(f"❌ Error: Invalid theme configuration - {e}")
        sys.exit(1)

    output_dir = Path(args.output)

    # Create output directory with error handling
    safe_create_directory(output_dir)

    print(f"\n🎨 Generating {theme_config['name']} theme...")

    # Track generated files for potential rollback
    generated_files = []

    try:
        # Generate theme.css
        theme_css = generate_theme_css(theme_config, args.dark_mode)
        safe_write_file(output_dir / "theme.css", theme_css, "theme.css")
        generated_files.append(output_dir / "theme.css")

        # Generate index.html
        index_html = generate_html_template(args.theme)
        safe_write_file(output_dir / "index.html", index_html, "index.html")
        generated_files.append(output_dir / "index.html")

        # Generate README.md
        readme = generate_readme(args.theme)
        safe_write_file(output_dir / "README.md", readme, "README.md")
        generated_files.append(output_dir / "README.md")

        # Generate theme-config.json
        config_json = json.dumps(theme_config, indent=2)
        safe_write_file(output_dir / "theme-config.json", config_json, "theme-config.json")
        generated_files.append(output_dir / "theme-config.json")

        print(f"\n✨ Theme generated successfully in: {output_dir.absolute()}")
        print(f"\n📝 Next steps:")
        print(f"   1. Open {output_dir / 'index.html'} in your browser")
        print(f"   2. Customize colors in theme.css")
        print(f"   3. Build your pages using the component classes\n")

    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        print(f"   Generated {len(generated_files)} files before failure.")
        print(f"   You may need to clean up: {output_dir}")
        sys.exit(1)


if __name__ == "__main__":
    main()
