# OWASP Top 10 Security Vulnerabilities

Comprehensive guide to OWASP Top 10 2021 vulnerabilities with detection patterns and remediation.

---

## A01: Broken Access Control

### Description

Failures in access control allow users to act outside their intended permissions, enabling unauthorized access to data or functionality.

### Common Patterns

**Missing Authorization Checks**:
```javascript
// ❌ Vulnerable
app.get('/api/users/:id/profile', async (req, res) => {
  const profile = await User.findById(req.params.id);
  res.json(profile); // No check if requester can access this profile
});

// ✅ Secure
app.get('/api/users/:id/profile', requireAuth, async (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const profile = await User.findById(req.params.id);
  res.json(profile);
});
```

**Insecure Direct Object References (IDOR)**:
```python
# ❌ Vulnerable
@app.route('/documents/<doc_id>')
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return jsonify(doc.to_dict())  # No ownership check

# ✅ Secure
@app.route('/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    if not doc or doc.owner_id != current_user.id:
        abort(404)  # Don't reveal existence
    return jsonify(doc.to_dict())
```

**Path Traversal**:
```javascript
// ❌ Vulnerable
app.get('/files/:filename', (req, res) => {
  res.sendFile(`/uploads/${req.params.filename}`);
  // Attacker: GET /files/../../etc/passwd
});

// ✅ Secure
const path = require('path');
app.get('/files/:filename', (req, res) => {
  const filename = path.basename(req.params.filename); // Remove path components
  const filepath = path.join(__dirname, 'uploads', filename);
  if (!filepath.startsWith(path.join(__dirname, 'uploads'))) {
    return res.status(400).send('Invalid filename');
  }
  res.sendFile(filepath);
});
```

### Detection Checklist

- [ ] Authorization checks present for all sensitive operations
- [ ] Object-level permissions verified (not just function-level)
- [ ] File paths validated and restricted to allowed directories
- [ ] URL tampering doesn't bypass access controls
- [ ] Horizontal privilege escalation prevented (user A can't access user B's data)
- [ ] Vertical privilege escalation prevented (user can't access admin functions)

---

## A02: Cryptographic Failures

### Description

Failures related to cryptography that lead to exposure of sensitive data.

### Common Patterns

**Weak or Hardcoded Encryption Keys**:
```python
# ❌ Vulnerable
from cryptography.fernet import Fernet
key = b'hardcoded_key_12345'  # Never hardcode keys!
cipher = Fernet(key)

# ✅ Secure
import os
from cryptography.fernet import Fernet
key = os.environ['ENCRYPTION_KEY'].encode()  # From environment
cipher = Fernet(key)
```

**Weak Hashing for Passwords**:
```javascript
// ❌ Vulnerable
const crypto = require('crypto');
const hash = crypto.createHash('md5').update(password).digest('hex'); // MD5 is broken

// ✅ Secure
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 10); // Use bcrypt with salt rounds
```

**Insecure Data Transmission**:
```python
# ❌ Vulnerable
import requests
response = requests.get('http://api.example.com/sensitive-data')  # HTTP not HTTPS

# ✅ Secure
import requests
response = requests.get('https://api.example.com/sensitive-data', verify=True)
```

### Detection Checklist

- [ ] Sensitive data encrypted at rest and in transit
- [ ] Strong encryption algorithms used (AES-256, not DES/3DES)
- [ ] Passwords hashed with strong algorithms (bcrypt, Argon2, not MD5/SHA1)
- [ ] Encryption keys stored securely (not hardcoded)
- [ ] HTTPS enforced for all sensitive communications
- [ ] No sensitive data in URLs or logs

---

## A03: Injection

### Description

Injection flaws occur when untrusted data is sent to an interpreter as part of a command or query.

### Common Patterns

**SQL Injection**:
```python
# ❌ Vulnerable
username = request.args.get('username')
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)  # Attacker: ' OR '1'='1

# ✅ Secure
username = request.args.get('username')
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))  # Parameterized query
```

**Cross-Site Scripting (XSS)**:
```javascript
// ❌ Vulnerable
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${req.query.q}</h1>`);
  // Attacker: ?q=<script>alert('XSS')</script>
});

// ✅ Secure
const escapeHtml = require('escape-html');
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${escapeHtml(req.query.q)}</h1>`);
});
```

**Command Injection**:
```python
# ❌ Vulnerable
import os
filename = request.args.get('file')
os.system(f'cat {filename}')  # Attacker: file=test.txt; rm -rf /

# ✅ Secure
import subprocess
filename = request.args.get('file')
# Validate filename first
if not re.match(r'^[\w\-. ]+$', filename):
    abort(400)
result = subprocess.run(['cat', filename], capture_output=True, text=True)
```

**Template Injection**:
```python
# ❌ Vulnerable - Server-Side Template Injection (SSTI)
from jinja2 import Template
user_input = request.args.get('name')
template = Template(f'Hello {user_input}!')  # Never template user input
output = template.render()

# ✅ Secure
from jinja2 import Template
user_input = request.args.get('name')
template = Template('Hello {{ name }}!')
output = template.render(name=user_input)  # Pass as variable
```

### Detection Checklist

- [ ] All user input validated and sanitized
- [ ] Parameterized queries used for database access
- [ ] Output properly encoded for context (HTML, JavaScript, SQL, etc.)
- [ ] ORM/prepared statements used instead of string concatenation
- [ ] Input validation with allowlists (not just denylists)
- [ ] No direct evaluation of user input (`eval()`, `exec()`, etc.)

---

## A04: Insecure Design

### Description

Risks from design and architectural flaws, missing or ineffective security controls.

### Common Patterns

**Missing Rate Limiting**:
```javascript
// ❌ Vulnerable
app.post('/api/login', async (req, res) => {
  const user = await authenticate(req.body.username, req.body.password);
  // No rate limiting - brute force attacks possible
});

// ✅ Secure
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts'
});
app.post('/api/login', loginLimiter, async (req, res) => {
  const user = await authenticate(req.body.username, req.body.password);
});
```

**Insufficient Security Logging**:
```python
# ❌ Vulnerable
@app.route('/admin/delete-user/<user_id>', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return 'User deleted'  # No audit log

# ✅ Secure
import logging
@app.route('/admin/delete-user/<user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    logging.info(f'Admin {current_user.id} deleting user {user_id}')
    db.session.delete(user)
    db.session.commit()
    return 'User deleted'
```

### Detection Checklist

- [ ] Threat modeling performed for critical flows
- [ ] Rate limiting on sensitive endpoints
- [ ] Security controls designed into architecture
- [ ] Secure defaults configured
- [ ] Security logging for sensitive operations

---

## A05: Security Misconfiguration

### Description

Missing security hardening, misconfigured permissions, or default configurations.

### Common Patterns

**Debug Mode in Production**:
```python
# ❌ Vulnerable
app = Flask(__name__)
app.config['DEBUG'] = True  # Never in production!
app.run(host='0.0.0.0')

# ✅ Secure
app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'
app.run(host='127.0.0.1')
```

**Verbose Error Messages**:
```javascript
// ❌ Vulnerable
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.stack }); // Exposes internals
});

// ✅ Secure
app.use((err, req, res, next) => {
  console.error(err.stack); // Log internally
  res.status(500).json({ error: 'Internal server error' }); // Generic message
});
```

**Missing Security Headers**:
```javascript
// ✅ Secure
const helmet = require('helmet');
app.use(helmet()); // Sets security headers
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"]
  }
}));
```

### Detection Checklist

- [ ] Debug/development features disabled in production
- [ ] Default passwords changed
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] Unnecessary features/services disabled
- [ ] Error messages don't expose sensitive information
- [ ] CORS configured restrictively

---

## A06: Vulnerable and Outdated Components

### Description

Using components with known vulnerabilities or outdated versions.

### Detection

**Check for Vulnerabilities**:
```bash
# JavaScript/Node.js
npm audit
npm audit fix

# Python
pip-audit
safety check

# Using scripts in this skill
python .claude/skills/code-review/scripts/dependency_check.py
```

**Common Vulnerable Patterns**:
```json
// ❌ Vulnerable package.json
{
  "dependencies": {
    "lodash": "4.17.15",  // Known prototype pollution CVE-2020-8203
    "axios": "0.19.0"      // Known vulnerability
  }
}

// ✅ Updated
{
  "dependencies": {
    "lodash": "^4.17.21",
    "axios": "^1.6.0"
  }
}
```

### Detection Checklist

- [ ] All dependencies regularly updated
- [ ] Vulnerability scanning in CI/CD
- [ ] No deprecated libraries used
- [ ] Security advisories monitored
- [ ] Minimal dependencies (smaller attack surface)

---

## A07: Identification and Authentication Failures

### Description

Weaknesses in authentication and session management.

### Common Patterns

**Weak Password Requirements**:
```javascript
// ❌ Vulnerable
if (password.length >= 6) {
  // Accept password
}

// ✅ Secure
const passwordStrength = require('check-password-strength');
const result = passwordStrength(password);
if (result.value !== 'Strong' && result.value !== 'Medium') {
  throw new Error('Password too weak');
}
```

**Insecure Session Management**:
```python
# ❌ Vulnerable
from flask import session
session['user_id'] = user.id  # Without proper configuration

# ✅ Secure
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
```

**Missing Multi-Factor Authentication**:
```javascript
// ✅ Secure - Implement MFA for sensitive operations
const speakeasy = require('speakeasy');
app.post('/verify-mfa', (req, res) => {
  const verified = speakeasy.totp.verify({
    secret: user.mfaSecret,
    encoding: 'base32',
    token: req.body.token
  });
  if (!verified) {
    return res.status(401).json({ error: 'Invalid MFA code' });
  }
});
```

### Detection Checklist

- [ ] Strong password policy enforced
- [ ] Multi-factor authentication available
- [ ] Session tokens secure (HttpOnly, Secure, SameSite)
- [ ] Session timeout implemented
- [ ] Account lockout after failed attempts
- [ ] Credentials never stored in plaintext

---

## A08: Software and Data Integrity Failures

### Description

Code and infrastructure that don't protect against integrity violations.

### Common Patterns

**Insecure Deserialization**:
```python
# ❌ Vulnerable
import pickle
data = pickle.loads(user_input)  # Can execute arbitrary code

# ✅ Secure
import json
data = json.loads(user_input)  # Safe deserialization
# Or validate with schema
from jsonschema import validate
validate(instance=data, schema=expected_schema)
```

**Missing CI/CD Security**:
```yaml
# ✅ Secure GitHub Actions example
name: Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security scan
        run: |
          npm audit
          npm run test:security
      - name: Build
        run: npm run build
```

### Detection Checklist

- [ ] Code signing implemented
- [ ] Integrity checks for dependencies
- [ ] Secure deserialization practices
- [ ] CI/CD pipeline security controls
- [ ] Supply chain security measures

---

## A09: Security Logging and Monitoring Failures

### Description

Insufficient logging and monitoring to detect breaches.

### Common Patterns

**Missing Security Logging**:
```python
# ❌ Vulnerable - No logging
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        session['user_id'] = user.id
        return redirect('/dashboard')
    return render_template('login.html', error='Invalid credentials')

# ✅ Secure - With security logging
import logging
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = authenticate(username, password)
    if user:
        logging.info(f'Successful login: {username} from {request.remote_addr}')
        session['user_id'] = user.id
        return redirect('/dashboard')
    logging.warning(f'Failed login attempt: {username} from {request.remote_addr}')
    return render_template('login.html', error='Invalid credentials')
```

### Detection Checklist

- [ ] Login attempts logged (success and failure)
- [ ] Access control failures logged
- [ ] Input validation failures logged
- [ ] Logs include timestamp, user, action, outcome
- [ ] Logs protected from tampering
- [ ] Log monitoring and alerting configured

---

## A10: Server-Side Request Forgery (SSRF)

### Description

Application fetches remote resources without validating user-supplied URLs.

### Common Patterns

**Unvalidated URL Fetching**:
```javascript
// ❌ Vulnerable
app.get('/fetch', async (req, res) => {
  const response = await fetch(req.query.url);
  const data = await response.text();
  res.send(data);
  // Attacker: ?url=http://localhost:6379/ (access internal Redis)
});

// ✅ Secure
const { URL } = require('url');
app.get('/fetch', async (req, res) => {
  const url = new URL(req.query.url);

  // Allowlist domains
  const allowedHosts = ['api.example.com', 'cdn.example.com'];
  if (!allowedHosts.includes(url.hostname)) {
    return res.status(400).json({ error: 'Invalid URL' });
  }

  // Block private IPs
  if (url.hostname === 'localhost' || url.hostname.startsWith('192.168.')) {
    return res.status(400).json({ error: 'Invalid URL' });
  }

  const response = await fetch(url.href);
  const data = await response.text();
  res.send(data);
});
```

### Detection Checklist

- [ ] URL allowlist implemented
- [ ] Private IP ranges blocked (localhost, 127.0.0.1, 192.168.x.x, 10.x.x.x)
- [ ] Cloud metadata endpoints blocked (169.254.169.254)
- [ ] URL validation before fetching
- [ ] Network segmentation to limit impact

---

## References

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
