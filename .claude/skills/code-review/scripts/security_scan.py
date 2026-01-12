#!/usr/bin/env python3
"""
Comprehensive security scanner for code review.
Scans for common security vulnerabilities in JavaScript/TypeScript and Python code.
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityScanner:
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.findings = []
        self.stats = {
            'files_scanned': 0,
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }

    def scan(self):
        """Run all security scans"""
        print(f"🔍 Scanning: {self.target_path}")
        print("=" * 60)

        if self.target_path.is_file():
            self._scan_file(self.target_path)
        elif self.target_path.is_dir():
            self._scan_directory(self.target_path)
        else:
            print(f"❌ Error: {self.target_path} is not a valid file or directory")
            sys.exit(1)

        self._print_results()

    def _scan_directory(self, directory: Path):
        """Recursively scan directory"""
        for item in directory.rglob('*'):
            if item.is_file() and self._should_scan(item):
                self._scan_file(item)

    def _should_scan(self, filepath: Path) -> bool:
        """Check if file should be scanned"""
        # Skip common non-code directories
        exclude_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__', 'venv', '.venv'}
        if any(part in exclude_dirs for part in filepath.parts):
            return False

        # Only scan code files
        extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.vue', '.html', '.php', '.java', '.go', '.rb'}
        return filepath.suffix in extensions

    def _scan_file(self, filepath: Path):
        """Scan a single file"""
        self.stats['files_scanned'] += 1

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            # Run all checks
            if filepath.suffix in {'.js', '.jsx', '.ts', '.tsx'}:
                self._scan_javascript(filepath, content, lines)
            elif filepath.suffix == '.py':
                self._scan_python(filepath, content, lines)

            # Language-agnostic checks
            self._scan_secrets(filepath, content, lines)
            self._scan_common_issues(filepath, content, lines)

        except Exception as e:
            print(f"⚠️  Error scanning {filepath}: {e}")

    def _scan_javascript(self, filepath: Path, content: str, lines: List[str]):
        """Scan JavaScript/TypeScript files"""
        patterns = [
            # Critical
            (r'\beval\s*\(', 'CRITICAL', 'Use of eval() - Remote Code Execution risk',
             'Never use eval() with user input. Use JSON.parse() or safe alternatives.'),
            (r'new\s+Function\s*\(', 'CRITICAL', 'Function constructor - Remote Code Execution risk',
             'Avoid Function constructor. Use regular functions or arrow functions.'),
            (r'dangerouslySetInnerHTML', 'HIGH', 'Potential XSS via dangerouslySetInnerHTML',
             'Sanitize HTML with DOMPurify before using dangerouslySetInnerHTML.'),

            # High
            (r'\.innerHTML\s*=', 'HIGH', 'Potential XSS via innerHTML',
             'Use textContent or sanitize HTML with DOMPurify.'),
            (r'document\.write\s*\(', 'HIGH', 'Use of document.write - XSS risk',
             'Avoid document.write. Use DOM manipulation methods.'),
            (r'\$\{.*?\}.*?(sql|query|exec|eval)', 'HIGH', 'Potential SQL injection via template literal',
             'Use parameterized queries instead of string interpolation.'),

            # Medium
            (r'localStorage\.(setItem|getItem)', 'MEDIUM', 'Sensitive data in localStorage',
             'Avoid storing sensitive data in localStorage. Use HttpOnly cookies.'),
            (r'sessionStorage\.(setItem|getItem)', 'MEDIUM', 'Sensitive data in sessionStorage',
             'Avoid storing sensitive data in sessionStorage. Use HttpOnly cookies.'),
            (r'__proto__', 'MEDIUM', 'Prototype pollution risk',
             'Validate object keys. Avoid __proto__, constructor, prototype.'),

            # Low
            (r'console\.(log|error|warn|info)', 'LOW', 'Console statements in production code',
             'Remove console statements before production deployment.'),
        ]

        for pattern, severity, message, remediation in patterns:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_finding(filepath, line_num, severity, message, line.strip(), remediation)

    def _scan_python(self, filepath: Path, content: str, lines: List[str]):
        """Scan Python files"""
        patterns = [
            # Critical
            (r'\beval\s*\(', 'CRITICAL', 'Use of eval() - Remote Code Execution risk',
             'Never use eval() with user input. Use ast.literal_eval() for safe evaluation.'),
            (r'\bexec\s*\(', 'CRITICAL', 'Use of exec() - Remote Code Execution risk',
             'Avoid exec(). Refactor to use functions or safe alternatives.'),
            (r'pickle\.loads?\s*\(', 'CRITICAL', 'Pickle deserialization - Remote Code Execution risk',
             'Never unpickle untrusted data. Use JSON or implement RestrictedUnpickler.'),
            (r'yaml\.load\s*\(', 'CRITICAL', 'Unsafe YAML loading - Code Execution risk',
             'Use yaml.safe_load() instead of yaml.load().'),

            # High
            (r'os\.system\s*\(', 'HIGH', 'Command injection via os.system',
             'Use subprocess with list arguments instead of shell=True.'),
            (r'subprocess\.(call|run|Popen).*shell\s*=\s*True', 'HIGH', 'Command injection via subprocess shell=True',
             'Use subprocess with list arguments, not shell=True.'),
            (r'(cursor|connection)\.execute\s*\(\s*f["\']', 'HIGH', 'SQL injection via f-string',
             'Use parameterized queries with placeholders.'),
            (r'(cursor|connection)\.execute\s*\(.*%\s', 'HIGH', 'SQL injection via string formatting',
             'Use parameterized queries with placeholders.'),

            # Medium
            (r'random\.(randint|choice|random)', 'MEDIUM', 'Weak random number generation',
             'Use secrets module for security-sensitive randomness.'),
            (r'hashlib\.(md5|sha1)\s*\(', 'MEDIUM', 'Weak hashing algorithm',
             'Use SHA-256 or stronger. For passwords, use bcrypt or Argon2.'),
            (r'input\s*\(', 'MEDIUM', 'User input without validation',
             'Validate and sanitize all user input.'),

            # Low
            (r'print\s*\(', 'LOW', 'Print statements in production code',
             'Use proper logging instead of print statements.'),
        ]

        for pattern, severity, message, remediation in patterns:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_finding(filepath, line_num, severity, message, line.strip(), remediation)

    def _scan_secrets(self, filepath: Path, content: str, lines: List[str]):
        """Scan for hardcoded secrets"""
        secret_patterns = [
            (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{8,}["\']', 'CRITICAL', 'Hardcoded password'),
            (r'(?i)(api[_-]?key|apikey)\s*=\s*["\'][^"\']{16,}["\']', 'CRITICAL', 'Hardcoded API key'),
            (r'(?i)(secret[_-]?key|secretkey)\s*=\s*["\'][^"\']{16,}["\']', 'CRITICAL', 'Hardcoded secret key'),
            (r'(?i)(access[_-]?token|accesstoken)\s*=\s*["\'][^"\']{16,}["\']', 'HIGH', 'Hardcoded access token'),
            (r'(?i)(private[_-]?key|privatekey)\s*=\s*["\'][^"\']{16,}["\']', 'CRITICAL', 'Hardcoded private key'),
            (r'(?i)aws[_-]?(access|secret)[_-]?key', 'CRITICAL', 'AWS credentials'),
            (r'(?i)(mysql|postgres|mongodb)://[^:]+:[^@]+@', 'HIGH', 'Database connection string with credentials'),
        ]

        for pattern, severity, message in secret_patterns:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    remediation = 'Use environment variables or secret management service. Never commit secrets.'
                    self._add_finding(filepath, line_num, severity, f'Potential secret: {message}',
                                      line.strip(), remediation)

    def _scan_common_issues(self, filepath: Path, content: str, lines: List[str]):
        """Scan for common security issues"""
        # Check for TODO/FIXME security comments
        for line_num, line in enumerate(lines, 1):
            if re.search(r'(?i)(TODO|FIXME|XXX).*?(security|vuln|hack|exploit)', line):
                self._add_finding(filepath, line_num, 'MEDIUM', 'Security-related TODO/FIXME',
                                  line.strip(), 'Address security TODOs before production.')

    def _add_finding(self, filepath: Path, line_num: int, severity: str,
                    message: str, code: str, remediation: str):
        """Add a security finding"""
        self.findings.append({
            'file': str(filepath),
            'line': line_num,
            'severity': severity,
            'message': message,
            'code': code,
            'remediation': remediation
        })
        self.stats[severity.lower()] = self.stats.get(severity.lower(), 0) + 1

    def _print_results(self):
        """Print scan results"""
        print("\n" + "=" * 60)
        print("📊 SCAN RESULTS")
        print("=" * 60)

        print(f"\nFiles scanned: {self.stats['files_scanned']}")
        print(f"Total issues: {len(self.findings)}")
        print(f"  🔴 Critical: {self.stats['critical']}")
        print(f"  🟠 High:     {self.stats['high']}")
        print(f"  🟡 Medium:   {self.stats['medium']}")
        print(f"  🟢 Low:      {self.stats['low']}")

        if not self.findings:
            print("\n✅ No security issues found!")
            return

        # Group findings by severity
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_findings = [f for f in self.findings if f['severity'] == severity]
            if not severity_findings:
                continue

            severity_icon = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }[severity]

            print(f"\n{severity_icon} {severity} FINDINGS ({len(severity_findings)})")
            print("-" * 60)

            for finding in severity_findings:
                print(f"\n📍 {finding['file']}:{finding['line']}")
                print(f"   {finding['message']}")
                print(f"   Code: {finding['code']}")
                print(f"   Fix: {finding['remediation']}")

        # Recommendations
        print("\n" + "=" * 60)
        print("💡 RECOMMENDATIONS")
        print("=" * 60)
        if self.stats['critical'] > 0 or self.stats['high'] > 0:
            print("⚠️  FIX CRITICAL AND HIGH ISSUES BEFORE DEPLOYMENT")
        print("1. Review all findings and apply recommended fixes")
        print("2. Run dependency vulnerability scan: npm audit / pip-audit")
        print("3. Use security linters: eslint-plugin-security / bandit")
        print("4. Enable security scanning in CI/CD pipeline")

def main():
    if len(sys.argv) < 2:
        print("Usage: python security_scan.py <file_or_directory>")
        print("\nExample:")
        print("  python security_scan.py src/")
        print("  python security_scan.py app.js")
        sys.exit(1)

    target_path = sys.argv[1]
    scanner = SecurityScanner(target_path)
    scanner.scan()

if __name__ == '__main__':
    main()
