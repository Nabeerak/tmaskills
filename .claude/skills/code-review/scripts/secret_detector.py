#!/usr/bin/env python3
"""
Secret detector for code review.
Scans for hardcoded secrets, API keys, passwords, and tokens.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class SecretDetector:
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.findings = []
        self.stats = {'files_scanned': 0, 'secrets_found': 0}

        # Define secret patterns with descriptions
        self.patterns = [
            # Generic secrets
            (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']([^"\']{8,})["\']',
             'Hardcoded Password', 'CRITICAL'),

            (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']([^"\']{16,})["\']',
             'API Key', 'CRITICAL'),

            (r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']([^"\']{16,})["\']',
             'Secret Key', 'CRITICAL'),

            (r'(?i)(access[_-]?token|accesstoken)\s*[=:]\s*["\']([^"\']{16,})["\']',
             'Access Token', 'HIGH'),

            (r'(?i)(auth[_-]?token|authtoken)\s*[=:]\s*["\']([^"\']{16,})["\']',
             'Auth Token', 'HIGH'),

            (r'(?i)(bearer\s+[A-Za-z0-9\-._~+/]+=*)',
             'Bearer Token', 'HIGH'),

            # AWS
            (r'(?i)aws[_-]?(access|secret)[_-]?key[_-]?id?\s*[=:]\s*["\']([A-Z0-9]{20})["\']',
             'AWS Access Key', 'CRITICAL'),

            (r'(?i)aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']([A-Za-z0-9/+=]{40})["\']',
             'AWS Secret Key', 'CRITICAL'),

            # GitHub
            (r'gh[pousr]_[A-Za-z0-9]{36}',
             'GitHub Token', 'CRITICAL'),

            # Private keys
            (r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
             'Private Key', 'CRITICAL'),

            (r'(?i)(private[_-]?key|privatekey)\s*[=:]\s*["\']([^"\']{32,})["\']',
             'Private Key', 'CRITICAL'),

            # Database connections
            (r'(mysql|postgres|postgresql|mongodb)://[^:]+:[^@]+@[^/]+',
             'Database Connection String', 'HIGH'),

            (r'(?i)db[_-]?(password|pass|pwd)\s*[=:]\s*["\']([^"\']{8,})["\']',
             'Database Password', 'CRITICAL'),

            # JWT
            (r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*',
             'JWT Token', 'HIGH'),

            # Slack
            (r'xox[pbar]-[0-9]{10,12}-[0-9]{10,12}-[A-Za-z0-9]{24}',
             'Slack Token', 'HIGH'),

            # Google API
            (r'AIza[0-9A-Za-z\\-_]{35}',
             'Google API Key', 'HIGH'),

            # Generic high-entropy strings (potential secrets)
            (r'(?i)(token|key|secret|password)\s*[=:]\s*["\']([A-Za-z0-9+/]{32,}={0,2})["\']',
             'High-Entropy String (Potential Secret)', 'MEDIUM'),

            # Encryption keys
            (r'(?i)(encryption[_-]?key|cipher[_-]?key)\s*[=:]\s*["\']([^"\']{16,})["\']',
             'Encryption Key', 'CRITICAL'),

            # OAuth
            (r'(?i)(client[_-]?secret|oauth[_-]?secret)\s*[=:]\s*["\']([^"\']{16,})["\']',
             'OAuth Client Secret', 'HIGH'),

            # Twilio
            (r'SK[a-z0-9]{32}',
             'Twilio API Key', 'HIGH'),

            # Stripe
            (r'(?i)sk_(test|live)_[0-9a-zA-Z]{24}',
             'Stripe Secret Key', 'CRITICAL'),

            # MailChimp
            (r'[0-9a-f]{32}-us[0-9]{1,2}',
             'MailChimp API Key', 'HIGH'),

            # SendGrid
            (r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}',
             'SendGrid API Key', 'HIGH'),
        ]

        # Files to skip
        self.skip_files = {
            '.env.example',
            '.env.sample',
            'config.example.json',
            'config.sample.json',
            'README.md',
            'CHANGELOG.md',
        }

    def scan(self):
        """Run secret detection scan"""
        print(f"🔍 Scanning for secrets: {self.target_path}")
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
        # Skip directories
        exclude_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__', 'venv', '.venv'}
        if any(part in exclude_dirs for part in filepath.parts):
            return False

        # Skip binary files
        binary_extensions = {'.jpg', '.png', '.gif', '.pdf', '.zip', '.exe', '.bin', '.so', '.dll'}
        if filepath.suffix.lower() in binary_extensions:
            return False

        # Skip example files
        if filepath.name in self.skip_files:
            return False

        return True

    def _scan_file(self, filepath: Path):
        """Scan a single file for secrets"""
        self.stats['files_scanned'] += 1

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            # Run pattern matching
            for pattern, description, severity in self.patterns:
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    # Find line number
                    line_num = content[:match.start()].count('\n') + 1
                    line = lines[line_num - 1].strip()

                    # Filter out false positives
                    if self._is_false_positive(line, description):
                        continue

                    self._add_finding(filepath, line_num, severity, description, line, match.group(0))

        except Exception as e:
            print(f"⚠️  Error scanning {filepath}: {e}")

    def _is_false_positive(self, line: str, description: str) -> bool:
        """Filter common false positives"""
        # Skip comments
        if line.strip().startswith(('#', '//', '/*', '*', '<!--')):
            return True

        # Skip test files with obvious dummy data
        if any(word in line.lower() for word in ['example', 'test', 'dummy', 'fake', 'sample', 'placeholder']):
            if any(word in line.lower() for word in ['password', 'secret', 'key', 'token']):
                return True

        # Skip empty or very short values
        if re.search(r'["\']["\']|["\'].{1,3}["\']', line):
            return True

        return False

    def _add_finding(self, filepath: Path, line_num: int, severity: str,
                    description: str, line: str, secret_value: str):
        """Add a secret finding"""
        # Mask the secret value for display
        masked_value = secret_value[:8] + '*' * (len(secret_value) - 8) if len(secret_value) > 8 else '***'

        self.findings.append({
            'file': str(filepath),
            'line': line_num,
            'severity': severity,
            'type': description,
            'code': line,
            'masked_value': masked_value
        })
        self.stats['secrets_found'] += 1

    def _print_results(self):
        """Print scan results"""
        print("\n" + "=" * 60)
        print("📊 SECRET DETECTION RESULTS")
        print("=" * 60)

        print(f"\nFiles scanned: {self.stats['files_scanned']}")
        print(f"Secrets found: {self.stats['secrets_found']}")

        if not self.findings:
            print("\n✅ No hardcoded secrets detected!")
            return

        # Group by severity
        severity_counts = {}
        for finding in self.findings:
            severity = finding['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        print("\nBreakdown by severity:")
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in severity_counts:
                icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}[severity]
                print(f"  {icon} {severity}: {severity_counts[severity]}")

        # Print findings
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

            print(f"\n{severity_icon} {severity} SECRETS ({len(severity_findings)})")
            print("-" * 60)

            for finding in severity_findings:
                print(f"\n📍 {finding['file']}:{finding['line']}")
                print(f"   Type: {finding['type']}")
                print(f"   Code: {finding['code']}")
                print(f"   Value: {finding['masked_value']}")

        # Recommendations
        print("\n" + "=" * 60)
        print("💡 REMEDIATION STEPS")
        print("=" * 60)
        print("1. Remove all hardcoded secrets from code")
        print("2. Store secrets in environment variables or secret manager")
        print("3. Add .env to .gitignore")
        print("4. Use .env.example with dummy values for documentation")
        print("5. Rotate any exposed secrets immediately")
        print("6. Enable secret scanning in CI/CD pipeline")
        print("7. Consider using: AWS Secrets Manager, HashiCorp Vault, or similar")

        print("\n⚠️  NEVER COMMIT SECRETS TO VERSION CONTROL")

def main():
    if len(sys.argv) < 2:
        print("Usage: python secret_detector.py <file_or_directory>")
        print("\nExample:")
        print("  python secret_detector.py src/")
        print("  python secret_detector.py config.js")
        sys.exit(1)

    target_path = sys.argv[1]
    detector = SecretDetector(target_path)
    detector.scan()

if __name__ == '__main__':
    main()
