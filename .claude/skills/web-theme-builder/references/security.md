# Security Considerations

Security practices for generating themes and components.

## Table of Contents

1. [Input Sanitization](#input-sanitization)
2. [XSS Prevention](#xss-prevention)
3. [Safe Defaults](#safe-defaults)
4. [Generated Code Safety](#generated-code-safety)
5. [Code Examples](#code-examples)

---

## Input Sanitization

### User-Provided Content
Sanitize all user-provided text (names, descriptions, custom colors) before inserting into HTML:

```python
import html

def sanitize_text(user_input: str) -> str:
    """Escape HTML entities in user input."""
    return html.escape(user_input, quote=True)
```

### Color Values
Validate HSL/hex color input to prevent CSS injection (only accept numeric values and valid formats):

```python
import re

def validate_hsl_color(hsl_string: str) -> bool:
    """Validate HSL color format to prevent injection."""
    pattern = r'^\d{1,3}\s+\d{1,3}%\s+\d{1,3}%$'
    if not re.match(pattern, hsl_string):
        raise ValueError("Invalid HSL format")

    parts = hsl_string.replace('%', '').split()
    h, s, l = int(parts[0]), int(parts[1]), int(parts[2])

    if not (0 <= h <= 360):
        raise ValueError(f"Hue value {h} out of range (0-360)")
    if not (0 <= s <= 100):
        raise ValueError(f"Saturation value {s} out of range (0-100)")
    if not (0 <= l <= 100):
        raise ValueError(f"Lightness value {l} out of range (0-100)")

    return True

def validate_hex_color(hex_string: str) -> bool:
    """Validate hex color format."""
    pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    if not re.match(pattern, hex_string):
        raise ValueError("Invalid hex color format")
    return True
```

### File Names
Sanitize file names and paths to prevent directory traversal attacks:

```python
import re
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    """Remove dangerous characters from filename."""
    # Remove path separators and null bytes
    sanitized = re.sub(r'[/\\:\x00]', '', filename)
    # Remove leading dots (hidden files)
    sanitized = sanitized.lstrip('.')
    # Limit length
    return sanitized[:255] if sanitized else 'unnamed'

def safe_path_join(base_dir: Path, user_path: str) -> Path:
    """Safely join paths, preventing directory traversal."""
    # Resolve to absolute path
    full_path = (base_dir / user_path).resolve()
    # Ensure it's still under base_dir
    if not str(full_path).startswith(str(base_dir.resolve())):
        raise ValueError("Path traversal detected")
    return full_path
```

### Script Parameters
Validate all command-line arguments before processing:

```python
def validate_theme_name(theme: str) -> bool:
    """Validate theme name is in allowed list."""
    allowed = ['modern', 'corporate', 'creative', 'dark', 'warm', 'ecommerce', 'saas', 'portfolio']
    if theme not in allowed:
        raise ValueError(f"Unknown theme: {theme}. Allowed: {', '.join(allowed)}")
    return True
```

---

## XSS Prevention

### Escape HTML Entities
When generating HTML with user content, escape `<`, `>`, `&`, `"`, and `'`:

```python
import html

# Use html.escape() for all user content
user_title = html.escape(user_input, quote=True)
html_output = f'<h1 class="title">{user_title}</h1>'
```

### Avoid Inline JavaScript
Never generate inline JavaScript with user input:

```html
<!-- BAD: User input in onclick -->
<button onclick="doAction('{{user_input}}')">Click</button>

<!-- GOOD: Use data attributes -->
<button data-action="submit" data-value="safe-value">Click</button>
```

### Content Security Policy
Recommend CSP headers for generated sites:

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
               font-src 'self' https://fonts.gstatic.com;
               img-src 'self' data: https:;">
```

### Alt Text Sanitization
Sanitize image alt text attributes:

```python
def safe_alt_text(alt: str) -> str:
    """Sanitize alt text for HTML attribute."""
    # Remove newlines and excessive whitespace
    sanitized = ' '.join(alt.split())
    # Escape HTML entities
    return html.escape(sanitized, quote=True)
```

---

## Safe Defaults

### Content Placeholders
Use safe placeholder text in generated templates:

```html
<!-- Use generic, safe placeholder text -->
<h1>Your Headline Here</h1>
<p>Add your content description here. This placeholder text demonstrates the typography and spacing of the theme.</p>

<!-- For images, use placeholder services or local assets -->
<img src="placeholder.svg" alt="Placeholder image description">
```

### External Resources
Use HTTPS for all external fonts and CDN resources:

```html
<!-- Always use HTTPS -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
```

### Font Loading
Use `font-display: swap` to prevent FOIT/FOUT attacks:

```css
@font-face {
  font-family: 'Inter';
  src: url('inter.woff2') format('woff2');
  font-display: swap; /* Prevent invisible text during load */
}
```

---

## Generated Code Safety

### No eval()
Never generate JavaScript code using eval() or Function():

```javascript
// BAD: Using eval with user input
eval('var x = ' + userInput);

// GOOD: Use safe parsing
const data = JSON.parse(safeJsonString);
```

### Validate URLs
Check that links and image sources are valid URLs:

```python
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate URL is safe to use."""
    try:
        parsed = urlparse(url)
        # Only allow http/https schemes
        if parsed.scheme not in ('http', 'https', ''):
            raise ValueError(f"Invalid URL scheme: {parsed.scheme}")
        # Check for javascript: pseudo-protocol
        if url.lower().startswith('javascript:'):
            raise ValueError("JavaScript URLs not allowed")
        return True
    except Exception as e:
        raise ValueError(f"Invalid URL: {e}")
```

### ARIA Attributes
Validate ARIA attribute values to prevent injection:

```python
VALID_ARIA_ROLES = {'button', 'link', 'navigation', 'main', 'banner', 'contentinfo', 'dialog', 'alert'}

def validate_aria_role(role: str) -> bool:
    """Validate ARIA role is from allowed list."""
    if role not in VALID_ARIA_ROLES:
        raise ValueError(f"Invalid ARIA role: {role}")
    return True
```

---

## Security Checklist

Before delivering generated themes:

- [ ] All user input sanitized before HTML insertion
- [ ] Color values validated against injection patterns
- [ ] File paths checked for directory traversal
- [ ] No inline JavaScript with dynamic content
- [ ] External resources use HTTPS
- [ ] CSP headers recommended in documentation
- [ ] Alt text and ARIA values escaped
- [ ] No eval() or Function() in generated code
- [ ] URLs validated before href/src attributes
