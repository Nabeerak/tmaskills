---
name: code-review
description: |
  Performs security-focused code reviews with OWASP alignment for JavaScript/TypeScript, Python, and other languages.
  This skill should be used when users ask to review code, check for security vulnerabilities, audit code quality,
  analyze pull requests, identify security risks, check for OWASP Top 10 issues, or validate code security.
---

# Code Review

Security-focused code review with OWASP alignment and automated security scanning.

## What This Skill Does

- Reviews code for security vulnerabilities (OWASP Top 10)
- Analyzes JavaScript/TypeScript and Python code with language-specific checks
- Provides automated security scanning with included Python scripts
- Reviews pull requests and merge requests
- Identifies code quality issues, anti-patterns, and security risks
- Generates structured feedback with severity ratings and remediation guidance

## What This Skill Does NOT Do

- Fix code automatically (provides guidance for user to fix)
- Deploy or execute code in production
- Handle backend infrastructure or deployment pipelines
- Perform dynamic analysis or runtime security testing

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Files to review, existing patterns, project structure, tech stack |
| **Conversation** | User's specific focus areas, constraints, severity thresholds |
| **Skill References** | Security patterns from `references/` (OWASP, best practices, language-specific) |
| **User Guidelines** | Team coding standards, security policies, compliance requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Before proceeding, ask:

1. **Scope**: "What files, directories, or pull request should I review?"
   - Single file, directory, PR number, or full codebase
2. **Focus**: "Security-focused review or full quality review?"
   - Security-only (OWASP, vulnerabilities)
   - Full quality (security + code quality + best practices)

## Optional Clarifications

3. **Severity threshold**: "What severity level to report?" (if not specified, report all)
   - All findings (recommended)
   - Critical and High only
   - Critical only
4. **Language-specific focus**: "Any specific languages to prioritize?" (if multiple languages present)

**Note**: Avoid asking too many questions in a single message. Start with required questions, infer from context when possible.

## If User Skips Clarifications

- **Required questions (Scope, Focus)**: If not provided, infer from context:
  - Check conversation for file/directory mentions
  - Look for open files in IDE or current working directory
  - If still unclear, ask again with specific examples
  - Default: Security-focused review of all code files in current directory

- **Optional questions**: Proceed with sensible defaults:
  - Severity threshold: Report all findings (Critical, High, Medium, Low)
  - Language focus: Analyze all detected languages equally

- **Ambiguous answers**: Confirm interpretation before proceeding
  - Example: "By 'everything', do you mean the entire codebase or just the src/ directory?"

---

## Review Process

### 1. Scope Determination

Identify what to review:

| Scope Type | When to Use |
|------------|-------------|
| **Single file** | User specifies file path |
| **Pull request** | Review changed files in PR/MR |
| **Directory** | Review all files in directory recursively |
| **Full codebase** | Comprehensive security audit |

### 2. Automated Security Scan (Optional)

Run security scripts before manual review:

```bash
# Run comprehensive security scan
python .claude/skills/code-review/scripts/security_scan.py <target_path>

# Detect hardcoded secrets
python .claude/skills/code-review/scripts/secret_detector.py <target_path>

# Check for vulnerable dependencies
python .claude/skills/code-review/scripts/dependency_check.py
```

### 3. Manual Security Review

Review code against security checklist:

1. **Read** target files using Read tool
2. **Analyze** against OWASP Top 10 (see `references/owasp-top-10.md`)
3. **Check** language-specific patterns (see `references/javascript-security.md` or `references/python-security.md`)
4. **Identify** anti-patterns (see `references/anti-patterns.md`)
5. **Document** findings with severity and location

### 4. Output Generation

Provide structured review feedback (see Output Format below).

---

## Security Focus Areas

### OWASP Top 10 Checklist

Review code for these vulnerabilities (details in `references/owasp-top-10.md`):

- [ ] **A01: Broken Access Control** - Unauthorized access, privilege escalation
- [ ] **A02: Cryptographic Failures** - Weak encryption, exposed sensitive data
- [ ] **A03: Injection** - SQL injection, XSS, command injection, template injection
- [ ] **A04: Insecure Design** - Missing security controls, threat modeling gaps
- [ ] **A05: Security Misconfiguration** - Default configs, verbose errors, missing patches
- [ ] **A06: Vulnerable Components** - Outdated dependencies with known CVEs
- [ ] **A07: Authentication Failures** - Weak passwords, broken session management
- [ ] **A08: Software and Data Integrity** - Insecure CI/CD, deserialization attacks
- [ ] **A09: Security Logging Failures** - Missing audit logs, insufficient monitoring
- [ ] **A10: Server-Side Request Forgery (SSRF)** - Unvalidated URL fetching

### Additional Security Checks

- **Secrets Detection** - Hardcoded API keys, tokens, passwords, credentials
- **Input Validation** - Missing or insufficient input sanitization
- **Output Encoding** - Unescaped output leading to XSS
- **Error Handling** - Information leakage through error messages
- **Business Logic** - Flaws in authorization, workflow, or data handling

---

## Language-Specific Considerations

### JavaScript/TypeScript

See `references/javascript-security.md` for comprehensive patterns.

**Key areas:**
- Prototype pollution
- DOM-based XSS
- `eval()` and `Function()` constructor usage
- Unsafe deserialization (`JSON.parse` with untrusted data)
- Client-side authorization checks (must validate server-side)
- npm dependency vulnerabilities

### Python

See `references/python-security.md` for comprehensive patterns.

**Key areas:**
- SQL injection (raw queries, string interpolation)
- Command injection (`os.system`, `subprocess` with shell=True)
- Pickle deserialization attacks
- Path traversal (`os.path.join` with user input)
- YAML/XML unsafe loading
- Flask/Django security misconfigurations

### Language-Agnostic

Applies to all languages:
- Principle of least privilege
- Defense in depth
- Secure by default configurations
- Zero trust architecture principles

---

## Analysis Scope

### What to Analyze

| Category | Check For |
|----------|-----------|
| **Security** | OWASP Top 10, injection flaws, auth issues, crypto failures |
| **Input Validation** | Missing sanitization, type checking, boundary validation |
| **Authentication** | Weak password policies, session management, token handling |
| **Authorization** | Privilege escalation, missing access controls |
| **Data Protection** | Sensitive data exposure, weak encryption, insecure storage |
| **Dependencies** | Known CVEs, outdated packages, malicious packages |
| **Configuration** | Hardcoded secrets, debug mode in production, default credentials |
| **Error Handling** | Information leakage, improper exception handling |

### What to Ignore

- Code style and formatting (unless security-relevant)
- Performance optimization (unless security-impacting)
- Documentation completeness
- Test coverage (unless security tests missing)

---

## Evaluation Criteria

| Criterion | Weight | How to Assess |
|-----------|--------|---------------|
| **Security Vulnerabilities** | 40% | OWASP Top 10 violations, exploitability, impact |
| **Input Validation** | 20% | Missing sanitization, weak validation, type safety |
| **Authentication/Authorization** | 15% | Access control flaws, privilege escalation risks |
| **Cryptography** | 10% | Weak algorithms, key management, data protection |
| **Dependencies** | 10% | Known CVEs, outdated packages, supply chain risks |
| **Configuration** | 5% | Hardcoded secrets, insecure defaults, debug flags |

---

## Output Format

Structure review feedback as follows:

```markdown
# Code Review Summary

**Review Scope**: [file/directory/PR reviewed]
**Review Date**: [date]
**Reviewer**: Claude Code (code-review skill)

---

## Executive Summary

[2-3 sentence overview of findings and overall security posture]

---

## Critical Findings (Severity: Critical)

### 1. [Vulnerability Title] - [File:Line]

**Category**: [OWASP category or security type]
**Severity**: Critical
**CWE**: [CWE ID if applicable]

**Description**: [Clear explanation of the vulnerability]

**Location**:
```
[language]
[Code snippet showing the issue]
```

**Impact**: [What attacker can achieve]

**Remediation**:
```
[language]
[Fixed code example]
```

**References**: [OWASP link, CWE link, or other resources]

---

## High Severity Findings

[Same format as Critical]

---

## Medium Severity Findings

[Same format as Critical]

---

## Low Severity Findings / Recommendations

[Same format as Critical]

---

## Positive Observations

- [Security control implemented well]
- [Good practice followed]

---

## Summary Statistics

- **Total Issues**: [count]
- **Critical**: [count]
- **High**: [count]
- **Medium**: [count]
- **Low**: [count]

---

## Remediation Priority

1. [Most critical issue - fix immediately]
2. [Next priority issue]
3. [Additional issues in priority order]

---

## Next Steps

1. Fix critical and high severity issues before deployment
2. Implement missing security controls
3. Run automated security scan: `python .claude/skills/code-review/scripts/security_scan.py`
4. Consider security testing (SAST/DAST) in CI/CD pipeline
```

---

## Severity Classification

| Severity | Criteria | Examples |
|----------|----------|----------|
| **Critical** | Directly exploitable, high impact, remote execution | SQL injection, RCE, authentication bypass |
| **High** | Exploitable with moderate effort, significant impact | XSS, CSRF, privilege escalation, sensitive data exposure |
| **Medium** | Requires specific conditions, moderate impact | Information disclosure, weak crypto, missing validation |
| **Low** | Difficult to exploit or low impact | Verbose errors, missing security headers, code quality issues |

---

## Synthesis

After completing analysis, synthesize findings into actionable intelligence:

1. **Aggregate**: Group related vulnerabilities across files
   - Example: "5 instances of SQL injection in user management module"
   - Identify patterns (same root cause, similar attack vectors)

2. **Prioritize**: Order by severity × exploitability × business impact
   - Critical issues affecting authentication/payment first
   - Consider: ease of exploit + potential damage + likelihood

3. **Contextualize**: Assess impact for this specific application
   - Public-facing vs internal tool
   - Data sensitivity (PII, financial, health)
   - Compliance requirements (GDPR, PCI-DSS, HIPAA)

4. **Actionable Remediation**: Provide clear, specific fix paths
   - Code examples (vulnerable → fixed)
   - Step-by-step remediation instructions
   - Verification steps after fix

5. **Preventive Measures**: Suggest process improvements
   - Linting rules to catch issues pre-commit
   - Security tests to add to test suite
   - Training needs identified
   - CI/CD security gates

---

## Output Checklist

Before delivering review, verify:

- [ ] All target files analyzed
- [ ] OWASP Top 10 checked
- [ ] Language-specific patterns reviewed
- [ ] Each finding includes: title, location, severity, description, impact, remediation
- [ ] Code examples provided for both vulnerable and fixed code
- [ ] Findings prioritized by severity
- [ ] Remediation guidance is actionable
- [ ] Positive observations included (if any)
- [ ] Summary statistics calculated
- [ ] Next steps clearly defined

---

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/security_scan.py` | Comprehensive security scan | `python security_scan.py <path>` |
| `scripts/secret_detector.py` | Detect hardcoded secrets | `python secret_detector.py <path>` |
| `scripts/dependency_check.py` | Check vulnerable dependencies | `python dependency_check.py` |

---

## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| OWASP Top 10 | https://owasp.org/Top10/ | Core vulnerability patterns (A01-A10) |
| OWASP Cheat Sheets | https://cheatsheetseries.owasp.org/ | Quick security patterns |
| OWASP Code Review Guide | https://owasp.org/www-project-code-review-guide/ | Comprehensive review methodology |
| CWE Top 25 | https://cwe.mitre.org/top25/ | Common weakness enumeration |
| Google Code Review Guide | https://google.github.io/eng-practices/review/ | Best practices and standards |

**Version Awareness**: OWASP Top 10 updates periodically (last: 2021). Check official site for latest version. Security patterns evolve—verify current best practices for new languages/frameworks.

**Unlisted Patterns**: For security issues not covered in references (new CVEs, emerging attack vectors, framework-specific vulnerabilities):
1. Fetch from official documentation above
2. Search for "[technology] security best practices [current year]"
3. Apply same severity classification and output format
4. Document findings with authoritative sources

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/owasp-top-10.md` | For OWASP vulnerability patterns and examples |
| `references/security-checklist.md` | For comprehensive security checklist |
| `references/javascript-security.md` | When reviewing JavaScript/TypeScript code |
| `references/python-security.md` | When reviewing Python code |
| `references/best-practices.md` | For general code review best practices |
| `references/anti-patterns.md` | For common code review mistakes to avoid |

---

## Finding Specific Patterns in References

References total ~11k words. Use grep to quickly locate specific content:

**Security vulnerabilities:**
```bash
# OWASP categories
grep -n "A01\|A02\|A03\|A04\|A05" references/owasp-top-10.md

# Specific vulnerability types
grep -n "SQL injection" references/*.md
grep -n "XSS\|Cross-Site Scripting" references/*.md
grep -n "CSRF\|Cross-Site Request" references/*.md
grep -n "Injection\|command injection" references/*.md
```

**Language-specific patterns:**
```bash
# JavaScript/TypeScript
grep -n "eval()\|Function()\|innerHTML" references/javascript-security.md
grep -n "prototype pollution\|__proto__" references/javascript-security.md
grep -n "dangerouslySetInnerHTML" references/javascript-security.md

# Python
grep -n "pickle\|yaml.load\|exec()" references/python-security.md
grep -n "os.system\|subprocess.*shell" references/python-security.md
grep -n "SQL.*f-string\|cursor.execute.*%" references/python-security.md
```

**Best practices & anti-patterns:**
```bash
# Code review process
grep -n "Pull Request\|PR size\|400 lines" references/best-practices.md
grep -n "automate\|linting\|CI/CD" references/best-practices.md

# Common mistakes
grep -n "Iterative Nitpicking\|Scope Creep" references/anti-patterns.md
grep -n "God Class\|Magic Number\|Copy.*Paste" references/anti-patterns.md
```

**Security checklists:**
```bash
# By category
grep -n "Input Validation\|Output Encoding" references/security-checklist.md
grep -n "Authentication\|Session Management" references/security-checklist.md
grep -n "Cryptography\|encryption" references/security-checklist.md
```
