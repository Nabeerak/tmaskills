#!/usr/bin/env python3
"""
Dependency vulnerability checker for code review.
Checks for vulnerable dependencies in JavaScript/Python projects.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class DependencyChecker:
    def __init__(self, project_path: str = '.'):
        self.project_path = Path(project_path)
        self.findings = {
            'javascript': [],
            'python': []
        }
        self.stats = {
            'total_vulnerabilities': 0,
            'critical': 0,
            'high': 0,
            'moderate': 0,
            'low': 0
        }

    def check(self):
        """Run dependency vulnerability checks"""
        print(f"🔍 Checking dependencies: {self.project_path}")
        print("=" * 60)

        # Check for JavaScript dependencies
        if self._has_javascript_project():
            print("\n📦 Checking JavaScript/Node.js dependencies...")
            self._check_npm()

        # Check for Python dependencies
        if self._has_python_project():
            print("\n🐍 Checking Python dependencies...")
            self._check_python()

        # Print results
        self._print_results()

    def _has_javascript_project(self) -> bool:
        """Check if project has JavaScript dependencies"""
        package_json = self.project_path / 'package.json'
        return package_json.exists()

    def _has_python_project(self) -> bool:
        """Check if project has Python dependencies"""
        requirements_txt = self.project_path / 'requirements.txt'
        pipfile = self.project_path / 'Pipfile'
        setup_py = self.project_path / 'setup.py'
        pyproject_toml = self.project_path / 'pyproject.toml'

        return any([requirements_txt.exists(), pipfile.exists(),
                   setup_py.exists(), pyproject_toml.exists()])

    def _check_npm(self):
        """Check npm dependencies for vulnerabilities"""
        try:
            # Run npm audit
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode in [0, 1]:  # 0 = no issues, 1 = issues found
                try:
                    audit_data = json.loads(result.stdout)
                    self._parse_npm_audit(audit_data)
                except json.JSONDecodeError:
                    print("⚠️  Could not parse npm audit output")
            else:
                print(f"⚠️  npm audit failed: {result.stderr}")

        except FileNotFoundError:
            print("⚠️  npm not found. Install Node.js to check JavaScript dependencies.")
        except subprocess.TimeoutExpired:
            print("⚠️  npm audit timed out")
        except Exception as e:
            print(f"⚠️  Error running npm audit: {e}")

    def _parse_npm_audit(self, audit_data: dict):
        """Parse npm audit JSON output"""
        if 'vulnerabilities' in audit_data:
            # npm v7+ format
            vulnerabilities = audit_data.get('vulnerabilities', {})

            for package_name, vuln_data in vulnerabilities.items():
                severity = vuln_data.get('severity', 'unknown').lower()
                via = vuln_data.get('via', [])

                # Extract details
                for item in via:
                    if isinstance(item, dict):
                        self.findings['javascript'].append({
                            'package': package_name,
                            'severity': severity,
                            'title': item.get('title', 'Unknown vulnerability'),
                            'url': item.get('url', ''),
                            'range': vuln_data.get('range', 'unknown'),
                            'fixed_in': vuln_data.get('fixAvailable', {}).get('version', 'N/A') if isinstance(vuln_data.get('fixAvailable'), dict) else 'N/A'
                        })
                        self._update_stats(severity)

        elif 'advisories' in audit_data:
            # npm v6 format
            advisories = audit_data.get('advisories', {})

            for adv_id, advisory in advisories.items():
                severity = advisory.get('severity', 'unknown').lower()
                self.findings['javascript'].append({
                    'package': advisory.get('module_name', 'unknown'),
                    'severity': severity,
                    'title': advisory.get('title', 'Unknown vulnerability'),
                    'url': advisory.get('url', ''),
                    'range': advisory.get('vulnerable_versions', 'unknown'),
                    'fixed_in': advisory.get('patched_versions', 'N/A')
                })
                self._update_stats(severity)

    def _check_python(self):
        """Check Python dependencies for vulnerabilities"""
        # Try pip-audit first (recommended)
        if self._check_with_pip_audit():
            return

        # Fallback to safety
        if self._check_with_safety():
            return

        print("⚠️  Install pip-audit or safety to check Python dependencies:")
        print("    pip install pip-audit")
        print("    or")
        print("    pip install safety")

    def _check_with_pip_audit(self) -> bool:
        """Check using pip-audit"""
        try:
            result = subprocess.run(
                ['pip-audit', '--format', 'json'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode in [0, 1]:
                try:
                    audit_data = json.loads(result.stdout)
                    self._parse_pip_audit(audit_data)
                    return True
                except json.JSONDecodeError:
                    print("⚠️  Could not parse pip-audit output")
                    return False
            else:
                return False

        except FileNotFoundError:
            return False
        except subprocess.TimeoutExpired:
            print("⚠️  pip-audit timed out")
            return False
        except Exception:
            return False

    def _parse_pip_audit(self, audit_data: dict):
        """Parse pip-audit JSON output"""
        vulnerabilities = audit_data.get('vulnerabilities', [])

        for vuln in vulnerabilities:
            package = vuln.get('name', 'unknown')
            severity = self._map_cvss_to_severity(vuln.get('cvss', 0))

            self.findings['python'].append({
                'package': package,
                'severity': severity,
                'title': vuln.get('id', 'Unknown vulnerability'),
                'description': vuln.get('description', ''),
                'current_version': vuln.get('version', 'unknown'),
                'fixed_in': ', '.join(vuln.get('fix_versions', [])) or 'N/A'
            })
            self._update_stats(severity)

    def _check_with_safety(self) -> bool:
        """Check using safety"""
        try:
            result = subprocess.run(
                ['safety', 'check', '--json'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            # Safety returns non-zero if vulnerabilities found
            try:
                safety_data = json.loads(result.stdout)
                self._parse_safety(safety_data)
                return True
            except json.JSONDecodeError:
                print("⚠️  Could not parse safety output")
                return False

        except FileNotFoundError:
            return False
        except subprocess.TimeoutExpired:
            print("⚠️  safety check timed out")
            return False
        except Exception:
            return False

    def _parse_safety(self, safety_data: list):
        """Parse safety JSON output"""
        for vuln in safety_data:
            package = vuln[0]
            installed_version = vuln[2]
            vuln_id = vuln[3]
            description = vuln[4]

            # Safety doesn't provide severity, default to HIGH
            severity = 'high'

            self.findings['python'].append({
                'package': package,
                'severity': severity,
                'title': vuln_id,
                'description': description,
                'current_version': installed_version,
                'fixed_in': 'See description'
            })
            self._update_stats(severity)

    def _map_cvss_to_severity(self, cvss_score: float) -> str:
        """Map CVSS score to severity level"""
        if cvss_score >= 9.0:
            return 'critical'
        elif cvss_score >= 7.0:
            return 'high'
        elif cvss_score >= 4.0:
            return 'moderate'
        else:
            return 'low'

    def _update_stats(self, severity: str):
        """Update statistics"""
        severity = severity.lower()
        self.stats['total_vulnerabilities'] += 1

        if severity in ['critical', 'high', 'moderate', 'low']:
            self.stats[severity] += 1

    def _print_results(self):
        """Print check results"""
        print("\n" + "=" * 60)
        print("📊 DEPENDENCY CHECK RESULTS")
        print("=" * 60)

        total_findings = len(self.findings['javascript']) + len(self.findings['python'])

        print(f"\nTotal vulnerabilities: {self.stats['total_vulnerabilities']}")
        print(f"  🔴 Critical:  {self.stats['critical']}")
        print(f"  🟠 High:      {self.stats['high']}")
        print(f"  🟡 Moderate:  {self.stats['moderate']}")
        print(f"  🟢 Low:       {self.stats['low']}")

        if total_findings == 0:
            print("\n✅ No known vulnerabilities in dependencies!")
            return

        # JavaScript findings
        if self.findings['javascript']:
            print("\n" + "=" * 60)
            print("📦 JAVASCRIPT/NODE.JS VULNERABILITIES")
            print("=" * 60)

            for finding in self.findings['javascript']:
                severity_icon = {
                    'critical': '🔴',
                    'high': '🟠',
                    'moderate': '🟡',
                    'low': '🟢'
                }.get(finding['severity'], '⚪')

                print(f"\n{severity_icon} {finding['severity'].upper()}: {finding['package']}")
                print(f"   Title: {finding['title']}")
                print(f"   Vulnerable: {finding['range']}")
                print(f"   Fixed in: {finding['fixed_in']}")
                if finding['url']:
                    print(f"   More info: {finding['url']}")

        # Python findings
        if self.findings['python']:
            print("\n" + "=" * 60)
            print("🐍 PYTHON VULNERABILITIES")
            print("=" * 60)

            for finding in self.findings['python']:
                severity_icon = {
                    'critical': '🔴',
                    'high': '🟠',
                    'moderate': '🟡',
                    'low': '🟢'
                }.get(finding['severity'], '⚪')

                print(f"\n{severity_icon} {finding['severity'].upper()}: {finding['package']}")
                print(f"   ID: {finding['title']}")
                print(f"   Current: {finding['current_version']}")
                print(f"   Fixed in: {finding['fixed_in']}")
                if 'description' in finding:
                    desc = finding['description'][:200] + '...' if len(finding['description']) > 200 else finding['description']
                    print(f"   Description: {desc}")

        # Recommendations
        print("\n" + "=" * 60)
        print("💡 REMEDIATION STEPS")
        print("=" * 60)

        if self.findings['javascript']:
            print("\nJavaScript/Node.js:")
            print("  1. Run: npm audit fix")
            print("  2. For breaking changes: npm audit fix --force")
            print("  3. Update package.json manually if needed")
            print("  4. Run tests after updates")

        if self.findings['python']:
            print("\nPython:")
            print("  1. Update vulnerable packages:")
            print("     pip install --upgrade <package-name>")
            print("  2. Update requirements.txt")
            print("  3. Run tests after updates")

        print("\n⚠️  ALWAYS TEST AFTER UPDATING DEPENDENCIES")

def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else '.'

    checker = DependencyChecker(project_path)
    checker.check()

if __name__ == '__main__':
    main()
