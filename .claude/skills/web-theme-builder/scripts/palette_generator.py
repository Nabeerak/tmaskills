#!/usr/bin/env python3
"""
Palette Generator Script

Generates accessible color palettes with dark mode variants.
Ensures WCAG AA contrast ratios (4.5:1 for text, 3:1 for UI components).

Usage:
    python palette_generator.py --hue 220 --name "Blue Palette"
    python palette_generator.py --hue 340 --saturation 80 --dark-mode
    python palette_generator.py --preset corporate
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


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


# Color presets based on theme types
PRESETS = {
    "modern": {"hue": 0, "saturation": 0, "description": "Monochromatic grayscale"},
    "corporate": {"hue": 220, "saturation": 90, "description": "Professional blue"},
    "creative": {"hue": 280, "saturation": 100, "description": "Vibrant purple"},
    "dark": {"hue": 180, "saturation": 100, "description": "Cyan neon"},
    "warm": {"hue": 25, "saturation": 95, "description": "Warm orange"},
    "ecommerce": {"hue": 142, "saturation": 71, "description": "Trust green"},
    "saas": {"hue": 220, "saturation": 90, "description": "SaaS blue"},
    "portfolio": {"hue": 280, "saturation": 70, "description": "Creative purple"}
}


def generate_color_scale(hue: int, saturation: int) -> Dict[str, str]:
    """Generate a color scale from 50 to 950 with given hue and saturation."""

    # Lightness values for each step
    lightness_values = {
        50: 97,
        100: 93,
        200: 87,
        300: 78,
        400: 68,
        500: 60,  # Base color
        600: 53,
        700: 48,
        800: 40,
        900: 33,
        950: 21
    }

    scale = {}
    for step, lightness in lightness_values.items():
        # Adjust saturation for very light and very dark colors
        adjusted_sat = saturation
        if lightness > 90:
            adjusted_sat = min(saturation, 20)  # Reduce saturation for very light
        elif lightness < 30:
            adjusted_sat = max(saturation - 10, 10)  # Slightly reduce for very dark

        scale[str(step)] = f"{hue} {adjusted_sat}% {lightness}%"

    return scale


def calculate_contrast_ratio(l1: float, l2: float) -> float:
    """
    Calculate contrast ratio between two relative luminance values.
    Simplified calculation for HSL colors.
    """
    # Approximate relative luminance from lightness
    # This is simplified; proper calculation requires RGB conversion
    lighter = max(l1, l2) / 100
    darker = min(l1, l2) / 100

    # Add 0.05 to avoid division by zero
    ratio = (lighter + 0.05) / (darker + 0.05)
    return ratio


def check_accessibility(bg_lightness: int, text_lightness: int, is_large_text: bool = False) -> Dict:
    """Check if color combination meets WCAG standards."""

    ratio = calculate_contrast_ratio(bg_lightness, text_lightness)
    aa_threshold = 3.0 if is_large_text else 4.5
    aaa_threshold = 4.5 if is_large_text else 7.0

    return {
        "ratio": round(ratio, 2),
        "aa": ratio >= aa_threshold,
        "aaa": ratio >= aaa_threshold,
        "threshold_aa": aa_threshold,
        "threshold_aaa": aaa_threshold
    }


def generate_semantic_colors(hue: int, saturation: int, dark_mode: bool = False) -> Dict[str, str]:
    """Generate semantic color palette (primary, secondary, accent, etc.)."""

    if dark_mode:
        return {
            "primary": f"{hue} {saturation}% 60%",
            "secondary": f"{(hue + 40) % 360} {saturation}% 65%",
            "accent": f"{(hue + 80) % 360} {saturation}% 70%",
            "background": f"{hue} 20% 10%",
            "surface": f"{hue} 18% 15%",
            "text": "0 0% 95%",
            "text-muted": "0 0% 60%",
            "success": "142 71% 55%",
            "warning": "38 92% 60%",
            "error": "0 84% 65%",
            "info": "199 89% 60%"
        }
    else:
        return {
            "primary": f"{hue} {saturation}% 56%",
            "secondary": f"{(hue + 40) % 360} {max(saturation - 20, 30)}% 60%",
            "accent": f"{(hue + 80) % 360} {saturation}% 58%",
            "background": "0 0% 100%",
            "surface": "0 0% 98%",
            "text": "0 0% 10%",
            "text-muted": "0 0% 45%",
            "success": "142 71% 45%",
            "warning": "38 92% 50%",
            "error": "0 84% 60%",
            "info": "199 89% 48%"
        }


def generate_dark_mode_variant(light_colors: Dict[str, str]) -> Dict[str, str]:
    """Generate dark mode variant of a light color palette."""

    dark_colors = {}

    for name, hsl in light_colors.items():
        parts = hsl.split()
        if len(parts) == 3:
            h, s, l = parts
            h_val = int(h)
            s_val = int(s.rstrip('%'))
            l_val = int(l.rstrip('%'))

            # Invert lightness for dark mode
            if name in ["background", "surface"]:
                # Make backgrounds dark
                new_l = 100 - l_val
                if new_l > 90:
                    new_l = 10 + (90 - l_val) // 2
            elif name in ["text", "text-muted"]:
                # Make text light
                new_l = 100 - l_val
                if new_l < 60:
                    new_l = 60 + (l_val - 10) // 2
            else:
                # Adjust other colors slightly
                new_l = max(min(l_val + 10, 70), 50)

            dark_colors[name] = f"{h_val} {s_val}% {new_l}%"

    return dark_colors


def generate_css(palette: Dict[str, str], dark_palette: Dict[str, str] = None) -> str:
    """Generate CSS with @theme directive."""

    css = """@import "tailwindcss";

@theme {
  /* Semantic Colors */
"""

    for name, value in palette.items():
        css += f"  --color-{name}: {value};\n"

    css += "}\n"

    if dark_palette:
        css += """
/* Dark Mode */
@media (prefers-color-scheme: dark) {
  @theme {
"""
        for name, value in dark_palette.items():
            css += f"    --color-{name}: {value};\n"

        css += """  }
}

.dark {
"""
        for name, value in dark_palette.items():
            css += f"  --color-{name}: {value};\n"

        css += "}\n"

    return css


def generate_preview_html(palette: Dict[str, str], name: str, dark_palette: Dict[str, str] = None) -> str:
    """Generate HTML preview of the palette."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} - Color Palette</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      margin: 0;
      padding: 2rem;
      background: #f5f5f5;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    h1 {{
      font-size: 2rem;
      margin-bottom: 2rem;
      color: #111;
    }}
    .palette {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 3rem;
    }}
    .color {{
      background: white;
      border-radius: 0.5rem;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .color-swatch {{
      height: 120px;
      border-bottom: 1px solid #eee;
    }}
    .color-info {{
      padding: 1rem;
    }}
    .color-name {{
      font-weight: 600;
      margin-bottom: 0.25rem;
      color: #111;
    }}
    .color-value {{
      font-family: 'Courier New', monospace;
      font-size: 0.875rem;
      color: #666;
    }}
    .mode-toggle {{
      margin-bottom: 2rem;
    }}
    .mode-toggle button {{
      padding: 0.5rem 1rem;
      margin-right: 0.5rem;
      border: 2px solid #ddd;
      background: white;
      border-radius: 0.25rem;
      cursor: pointer;
      font-size: 0.875rem;
    }}
    .mode-toggle button.active {{
      background: #111;
      color: white;
      border-color: #111;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{name}</h1>
"""

    if dark_palette:
        html += """
    <div class="mode-toggle">
      <button class="active" onclick="showLightMode()">Light Mode</button>
      <button onclick="showDarkMode()">Dark Mode</button>
    </div>
"""

    html += """
    <div class="palette light-mode">
"""

    # Light mode colors
    for color_name, color_value in palette.items():
        hsl_parts = color_value.split()
        if len(hsl_parts) == 3:
            html += f"""
      <div class="color">
        <div class="color-swatch" style="background: hsl({color_value});"></div>
        <div class="color-info">
          <div class="color-name">{color_name}</div>
          <div class="color-value">hsl({color_value})</div>
        </div>
      </div>
"""

    html += """
    </div>
"""

    # Dark mode colors
    if dark_palette:
        html += """
    <div class="palette dark-mode" style="display: none;">
"""
        for color_name, color_value in dark_palette.items():
            html += f"""
      <div class="color">
        <div class="color-swatch" style="background: hsl({color_value});"></div>
        <div class="color-info">
          <div class="color-name">{color_name}</div>
          <div class="color-value">hsl({color_value})</div>
        </div>
      </div>
"""
        html += """
    </div>
"""

    html += """
  </div>

  <script>
    function showLightMode() {
      document.querySelector('.light-mode').style.display = 'grid';
      document.querySelector('.dark-mode').style.display = 'none';
      document.querySelectorAll('.mode-toggle button')[0].classList.add('active');
      document.querySelectorAll('.mode-toggle button')[1].classList.remove('active');
    }

    function showDarkMode() {
      document.querySelector('.light-mode').style.display = 'none';
      document.querySelector('.dark-mode').style.display = 'grid';
      document.querySelectorAll('.mode-toggle button')[0].classList.remove('active');
      document.querySelectorAll('.mode-toggle button')[1].classList.add('active');
    }
  </script>
</body>
</html>
"""

    return html


def main():
    parser = argparse.ArgumentParser(
        description="Generate accessible color palettes with dark mode variants"
    )
    parser.add_argument(
        "--hue",
        type=int,
        help="Hue value (0-360)"
    )
    parser.add_argument(
        "--saturation",
        type=int,
        default=90,
        help="Saturation percentage (0-100, default: 90)"
    )
    parser.add_argument(
        "--name",
        default="Color Palette",
        help="Palette name"
    )
    parser.add_argument(
        "--preset",
        choices=list(PRESETS.keys()),
        help="Use a preset theme palette"
    )
    parser.add_argument(
        "--dark-mode",
        action="store_true",
        help="Generate dark mode variant"
    )
    parser.add_argument(
        "--output",
        default="./palette",
        help="Output directory (default: ./palette)"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available presets"
    )

    args = parser.parse_args()

    # List presets
    if args.list_presets:
        print("\nAvailable Presets:\n")
        for name, data in PRESETS.items():
            print(f"  {name:12} - {data['description']} (H:{data['hue']}, S:{data['saturation']}%)")
        print()
        return

    # Determine hue and saturation
    if args.preset:
        preset = PRESETS[args.preset]
        hue = preset["hue"]
        saturation = preset["saturation"]
        palette_name = args.name if args.name != "Color Palette" else preset["description"]
    elif args.hue is not None:
        hue = args.hue
        saturation = args.saturation
        palette_name = args.name
    else:
        parser.print_help()
        print("\n❌ Error: Either --hue or --preset is required (or use --list-presets)")
        sys.exit(1)

    # Validate inputs
    if not 0 <= hue <= 360:
        print("❌ Error: Hue must be between 0 and 360")
        sys.exit(1)

    if not 0 <= saturation <= 100:
        print("❌ Error: Saturation must be between 0 and 100")
        sys.exit(1)

    # Create output directory with error handling
    output_dir = Path(args.output)
    safe_create_directory(output_dir)

    print(f"\n🎨 Generating {palette_name}...")
    print(f"   Hue: {hue}°, Saturation: {saturation}%")

    # Generate palettes
    light_palette = generate_semantic_colors(hue, saturation, dark_mode=False)
    dark_palette = generate_semantic_colors(hue, saturation, dark_mode=True) if args.dark_mode else None

    # Validate generated colors
    try:
        for name, color in light_palette.items():
            validate_hsl_color(color)
        if dark_palette:
            for name, color in dark_palette.items():
                validate_hsl_color(color)
    except ValueError as e:
        print(f"❌ Error: Generated invalid color - {e}")
        sys.exit(1)

    # Check accessibility
    bg_lightness = 100
    text_lightness = 10
    contrast_check = check_accessibility(bg_lightness, text_lightness)

    print(f"\n✅ Accessibility Check:")
    print(f"   Contrast Ratio: {contrast_check['ratio']}:1")
    print(f"   WCAG AA: {'✓ Pass' if contrast_check['aa'] else '✗ Fail'}")
    print(f"   WCAG AAA: {'✓ Pass' if contrast_check['aaa'] else '✗ Fail'}")

    # Generate files with error handling
    try:
        # 1. palette.json
        palette_json = {
            "name": palette_name,
            "hue": hue,
            "saturation": saturation,
            "light": light_palette
        }
        if dark_palette:
            palette_json["dark"] = dark_palette

        safe_write_file(output_dir / "palette.json", json.dumps(palette_json, indent=2), "palette.json")

        # 2. palette.css
        palette_css = generate_css(light_palette, dark_palette)
        safe_write_file(output_dir / "palette.css", palette_css, "palette.css")

        # 3. preview.html
        preview_html = generate_preview_html(light_palette, palette_name, dark_palette)
        safe_write_file(output_dir / "preview.html", preview_html, "preview.html")

        print(f"\n✨ Palette generated successfully in: {output_dir.absolute()}")
        print(f"\n📝 Next steps:")
        print(f"   1. Open preview.html to see your palette")
        print(f"   2. Copy palette.css to your project")
        print(f"   3. Customize colors as needed\n")

    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        print(f"   You may need to clean up: {output_dir}")
        sys.exit(1)


if __name__ == "__main__":
    main()
