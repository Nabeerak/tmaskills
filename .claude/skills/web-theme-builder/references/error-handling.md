# Error Handling

Graceful error handling when generating themes and components.

## Table of Contents

1. [Script Execution Errors](#script-execution-errors)
2. [Generation Failures](#generation-failures)
3. [Recovery Strategies](#recovery-strategies)
4. [Common Edge Cases](#common-edge-cases)
5. [Code Examples](#code-examples)

---

## Script Execution Errors

### Missing Arguments
Provide clear error messages with usage examples:

```python
if not args.theme:
    print("❌ Error: --theme is required")
    print("   Usage: python theme_generator.py --theme modern --output ./my-theme")
    print("   Run with --list to see available themes")
    sys.exit(1)
```

### Invalid Input
Validate inputs before processing and show specific error messages:

```python
def validate_theme(theme: str) -> None:
    allowed = ['modern', 'corporate', 'creative', 'dark', 'warm', 'ecommerce', 'saas', 'portfolio']
    if theme not in allowed:
        print(f"❌ Error: Unknown theme '{theme}'")
        print(f"   Available themes: {', '.join(allowed)}")
        sys.exit(1)
```

### File System Errors
Handle permission errors, disk full, invalid paths:

```python
try:
    output_dir.mkdir(parents=True, exist_ok=True)
except PermissionError:
    print(f"❌ Error: No permission to create directory {output_dir}")
    print("   Solution: Check directory permissions or choose different location")
    sys.exit(1)
except OSError as e:
    print(f"❌ Error: Cannot create directory - {e}")
    print("   Solution: Check disk space and path validity")
    sys.exit(1)
```

### Dependency Errors
Check for required tools/libraries and provide installation guidance:

```python
import shutil

def check_dependencies():
    """Check required tools are available."""
    if not shutil.which('python3'):
        print("❌ Error: Python 3 not found")
        print("   Solution: Install Python 3.7+ from python.org")
        sys.exit(1)
```

---

## Generation Failures

### Invalid Color Combinations
Check accessibility contrast before generating:

```python
def check_contrast(bg_lightness: int, text_lightness: int) -> float:
    """Calculate approximate contrast ratio."""
    l1 = max(bg_lightness, text_lightness) / 100
    l2 = min(bg_lightness, text_lightness) / 100
    ratio = (l1 + 0.05) / (l2 + 0.05)

    if ratio < 4.5:
        print(f"⚠️ Warning: Contrast ratio {ratio:.1f}:1 below WCAG AA (4.5:1)")
        print("   Solution: Increase lightness difference between text and background")

    return ratio
```

### Font Loading Failures
Provide fallback fonts in generated CSS:

```css
/* Always include system font fallbacks */
:root {
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-text: 'Inter', system-ui, -apple-system, sans-serif;
}
```

### Asset Not Found
Verify template files exist before reading:

```python
def load_template(template_path: Path) -> str:
    """Load template with error handling."""
    if not template_path.exists():
        print(f"❌ Error: Template not found: {template_path}")
        print("   Solution: Verify template files are in assets/templates/")
        sys.exit(1)

    try:
        return template_path.read_text()
    except IOError as e:
        print(f"❌ Error: Cannot read template - {e}")
        sys.exit(1)
```

### Malformed Templates
Validate JSON/CSS syntax before writing files:

```python
import json

def validate_json_config(config_path: Path) -> dict:
    """Load and validate JSON configuration."""
    try:
        with open(config_path) as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {config_path}")
        print(f"   Line {e.lineno}, Column {e.colno}: {e.msg}")
        sys.exit(1)
```

---

## Recovery Strategies

### Partial Generation
If one component fails, continue with others and report failure:

```python
def generate_all_components(components: list, output_dir: Path) -> None:
    """Generate components with partial failure handling."""
    failed = []
    succeeded = []

    for component in components:
        try:
            generate_component(component, output_dir)
            succeeded.append(component)
            print(f"✅ Generated {component}")
        except Exception as e:
            failed.append((component, str(e)))
            print(f"⚠️ Failed to generate {component}: {e}")

    print(f"\nSummary: {len(succeeded)} succeeded, {len(failed)} failed")
    if failed:
        print("Failed components:")
        for comp, error in failed:
            print(f"  - {comp}: {error}")
```

### Rollback
Provide option to revert to previous working state:

```python
import shutil
from datetime import datetime

def backup_before_generation(output_dir: Path) -> Path:
    """Create backup before generating new files."""
    if output_dir.exists():
        backup_name = f"{output_dir.name}_backup_{datetime.now():%Y%m%d_%H%M%S}"
        backup_path = output_dir.parent / backup_name
        shutil.copytree(output_dir, backup_path)
        print(f"📦 Backup created: {backup_path}")
        return backup_path
    return None
```

### Validation
Run validation checks before finalizing output:

```python
def validate_output(output_dir: Path) -> bool:
    """Validate generated output."""
    required_files = ['theme.css', 'index.html']
    missing = [f for f in required_files if not (output_dir / f).exists()]

    if missing:
        print(f"❌ Validation failed: Missing files: {', '.join(missing)}")
        return False

    print("✅ Output validation passed")
    return True
```

### User Feedback
Show progress and clear error messages with resolution steps:

```python
def generate_with_progress(steps: list) -> None:
    """Generate with progress feedback."""
    total = len(steps)
    for i, step in enumerate(steps, 1):
        print(f"[{i}/{total}] {step['name']}...", end=" ")
        try:
            step['action']()
            print("✓")
        except Exception as e:
            print("✗")
            print(f"   Error: {e}")
            print(f"   Solution: {step.get('solution', 'Check the error message above')}")
            raise
```

---

## Common Edge Cases

| Edge Case | Problem | Solution |
|-----------|---------|----------|
| Very long text | Buttons/headings with 100+ characters overflow | Use `text-ellipsis` or `word-wrap` |
| Missing fonts | Font fails to load | Provide fallback fonts in font stack |
| Extreme viewports | Very narrow (<320px) or wide (>2560px) | Add container max-widths |
| Tall viewports | Very short heights (<400px) | Avoid `vh` units, use `min-height` |
| High contrast mode | User OS forces colors | Use semantic HTML, test with Windows High Contrast |
| Font scaling | Browser zoom >200% | Test with large font sizes (16px minimum) |
| No JavaScript | Users with JS disabled | Ensure core functionality works without JS |
| Slow connections | Large images/fonts | Optimize assets, use `font-display: swap` |

### CSS Solutions for Edge Cases

```css
/* Handle long text gracefully */
.button {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.heading {
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
}

/* Provide comprehensive font fallbacks */
:root {
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Handle extreme viewports */
.container {
  width: 100%;
  max-width: 1440px;
  min-width: 280px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Avoid viewport-dependent heights for critical content */
.hero {
  min-height: 400px; /* Not 100vh */
  padding: 4rem 0;
}
```

---

## Error Handling Checklist

- [ ] All user inputs validated before processing
- [ ] File operations wrapped in try/except
- [ ] Clear error messages with solutions provided
- [ ] Partial failures handled gracefully
- [ ] Progress feedback shown during generation
- [ ] Backup created before overwriting files
- [ ] Output validated before completion
- [ ] Edge cases handled in generated CSS
