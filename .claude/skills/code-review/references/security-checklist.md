# Security Review Checklist

Comprehensive security checklist for code reviews based on OWASP and industry standards.

---

## Table of Contents

1. [Input Validation](#input-validation)
2. [Output Encoding](#output-encoding)
3. [Authentication](#authentication)
4. [Session Management](#session-management)
5. [Access Control](#access-control)
6. [Cryptography](#cryptography)
7. [Error Handling](#error-handling)
8. [Data Protection](#data-protection)
9. [Communication Security](#communication-security)
10. [Configuration](#configuration)
11. [Database Security](#database-security)
12. [File Management](#file-management)
13. [Memory Management](#memory-management)
14. [API Security](#api-security)

---

## Input Validation

### Validation Rules

- [ ] All input validated on server-side (never trust client-side validation alone)
- [ ] Allowlist validation used (define what's allowed, not what's forbidden)
- [ ] Input length limits enforced
- [ ] Data types validated
- [ ] Character sets validated
- [ ] Special characters properly escaped
- [ ] File uploads validated (type, size, content)
- [ ] URL/URI inputs validated against allowed schemes
- [ ] Numeric inputs range-checked

### Examples

```javascript
// ✅ Allowlist validation
function validateUsername(username) {
  const pattern = /^[a-zA-Z0-9_]{3,20}$/;
  return pattern.test(username);
}

// ✅ Type and range validation
function validateAge(age) {
  const numAge = parseInt(age, 10);
  return !isNaN(numAge) && numAge >= 0 && numAge <= 150;
}
```

---

## Output Encoding

### Encoding Rules

- [ ] Output encoded based on context (HTML, JavaScript, URL, CSS, SQL)
- [ ] No user input directly in HTML without escaping
- [ ] JSON responses properly escaped
- [ ] HTTP headers don't include unencoded user input
- [ ] Content-Type headers set correctly
- [ ] X-Content-Type-Options: nosniff header present

### Examples

```javascript
// ✅ Context-aware encoding
const escapeHtml = (str) =>
  str.replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[char]));

// ✅ JSON encoding
res.setHeader('Content-Type', 'application/json');
res.send(JSON.stringify({ message: userInput }));
```

---

## Authentication

### Authentication Requirements

- [ ] Strong password policy enforced (min 12 chars, complexity requirements)
- [ ] Passwords hashed with bcrypt/Argon2 (not MD5/SHA1)
- [ ] Account lockout after failed attempts (5-10 attempts)
- [ ] Multi-factor authentication available for sensitive accounts
- [ ] Password reset tokens expire (15-30 minutes)
- [ ] Passwords not sent over unencrypted channels
- [ ] "Remember me" functionality secure
- [ ] No default credentials
- [ ] Username enumeration prevented

### Examples

```python
# ✅ Secure password hashing
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash(password)

# Later: verify
try:
    ph.verify(hash, password)
    # Password correct
except:
    # Password incorrect
```

---

## Session Management

### Session Requirements

- [ ] Session IDs generated securely (cryptographically random)
- [ ] Session cookies have Secure flag (HTTPS only)
- [ ] Session cookies have HttpOnly flag (no JavaScript access)
- [ ] Session cookies have SameSite flag (CSRF protection)
- [ ] Session timeout implemented (idle and absolute)
- [ ] Session invalidated on logout
- [ ] Session regenerated after login
- [ ] No session IDs in URLs
- [ ] Concurrent session limits enforced

### Examples

```javascript
// ✅ Secure session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  name: 'sessionId',
  cookie: {
    secure: true,      // HTTPS only
    httpOnly: true,    // No JS access
    sameSite: 'strict', // CSRF protection
    maxAge: 1800000    // 30 minutes
  },
  resave: false,
  saveUninitialized: false
}));
```

---

## Access Control

### Authorization Requirements

- [ ] All resources have access control checks
- [ ] Authorization checked on server-side
- [ ] Principle of least privilege enforced
- [ ] Default deny (access denied unless explicitly granted)
- [ ] Direct object references checked (IDOR prevention)
- [ ] Function-level access control enforced
- [ ] Object-level access control enforced
- [ ] File permissions restrictive

### Examples

```python
# ✅ Object-level authorization
@app.route('/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    # Check ownership or permissions
    if doc.owner_id != current_user.id and not current_user.is_admin:
        abort(403)
    return jsonify(doc.to_dict())
```

---

## Cryptography

### Cryptographic Requirements

- [ ] Strong algorithms used (AES-256, RSA-2048+)
- [ ] Keys managed securely (not hardcoded)
- [ ] Key rotation implemented
- [ ] Random number generation cryptographically secure
- [ ] TLS 1.2+ used (disable SSL, TLS 1.0/1.1)
- [ ] Certificate validation enabled
- [ ] Sensitive data encrypted at rest
- [ ] Secure hashing for passwords (bcrypt, Argon2)

### Examples

```python
# ✅ Secure encryption
from cryptography.fernet import Fernet
import os

# Generate and store key securely
key = Fernet.generate_key()
# Store key in environment or key management service

# Later: use key
cipher = Fernet(os.environ['ENCRYPTION_KEY'].encode())
encrypted = cipher.encrypt(plaintext.encode())
```

---

## Error Handling

### Error Handling Requirements

- [ ] Generic error messages for users
- [ ] Detailed errors logged server-side only
- [ ] No stack traces exposed to users
- [ ] Error codes don't reveal system information
- [ ] 404 pages don't confirm file existence
- [ ] Exceptions properly caught and handled
- [ ] No sensitive data in error messages

### Examples

```javascript
// ✅ Secure error handling
app.use((err, req, res, next) => {
  // Log detailed error
  console.error({
    message: err.message,
    stack: err.stack,
    user: req.user?.id,
    timestamp: new Date()
  });

  // Send generic message to user
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    error: statusCode === 500
      ? 'Internal server error'
      : err.message
  });
});
```

---

## Data Protection

### Data Protection Requirements

- [ ] Sensitive data identified and classified
- [ ] PII/PHI encrypted at rest
- [ ] Sensitive data encrypted in transit (TLS)
- [ ] Data retention policies enforced
- [ ] Secure deletion of sensitive data
- [ ] No sensitive data in logs
- [ ] No sensitive data in URLs or query strings
- [ ] Credit card data handled per PCI DSS

### Examples

```python
# ✅ Sanitize sensitive data from logs
import logging

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        # Redact sensitive fields
        if hasattr(record, 'msg'):
            record.msg = re.sub(r'password=\S+', 'password=***', str(record.msg))
            record.msg = re.sub(r'ssn=\d+', 'ssn=***', record.msg)
        return True

logger = logging.getLogger()
logger.addFilter(SensitiveDataFilter())
```

---

## Communication Security

### Communication Requirements

- [ ] HTTPS enforced (HTTP redirects to HTTPS)
- [ ] HSTS header configured
- [ ] TLS 1.2+ enforced
- [ ] Strong cipher suites configured
- [ ] Certificate pinning for mobile apps
- [ ] No mixed content (HTTP resources on HTTPS page)
- [ ] Secure WebSocket connections (wss://)

### Examples

```javascript
// ✅ Enforce HTTPS
app.use((req, res, next) => {
  if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
    return res.redirect('https://' + req.get('host') + req.url);
  }
  next();
});

// ✅ HSTS header
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));
```

---

## Configuration

### Configuration Requirements

- [ ] Debug mode disabled in production
- [ ] Sensitive config in environment variables (not code)
- [ ] Default passwords changed
- [ ] Unnecessary features/services disabled
- [ ] Security headers configured
- [ ] CORS configured restrictively
- [ ] CSP (Content Security Policy) configured
- [ ] File upload directories not executable

### Examples

```javascript
// ✅ Security headers
const helmet = require('helmet');
app.use(helmet());
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'"],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"]
  }
}));
```

---

## Database Security

### Database Requirements

- [ ] Parameterized queries used (no string concatenation)
- [ ] ORM used correctly
- [ ] Least privilege database accounts
- [ ] Database credentials secured
- [ ] SQL injection prevented
- [ ] NoSQL injection prevented
- [ ] Database encryption enabled
- [ ] Database backups secured

### Examples

```python
# ✅ Parameterized query
from sqlalchemy import text

# Safe: parameterized
user = db.session.execute(
    text("SELECT * FROM users WHERE username = :username"),
    {"username": username}
).first()

# ❌ UNSAFE: string concatenation
# query = f"SELECT * FROM users WHERE username = '{username}'"
```

---

## File Management

### File Handling Requirements

- [ ] File upload types validated (allowlist)
- [ ] File upload sizes limited
- [ ] Uploaded files scanned for malware
- [ ] File paths validated (prevent traversal)
- [ ] Uploaded files stored outside webroot
- [ ] Uploaded files renamed (don't trust client filenames)
- [ ] File permissions restrictive

### Examples

```javascript
// ✅ Secure file upload
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');

const storage = multer.diskStorage({
  destination: '/var/uploads/', // Outside webroot
  filename: (req, file, cb) => {
    // Generate random filename
    const randomName = crypto.randomBytes(16).toString('hex');
    const ext = path.extname(file.originalname);
    cb(null, randomName + ext);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  }
});
```

---

## Memory Management

### Memory Requirements

- [ ] No sensitive data in memory longer than needed
- [ ] Sensitive variables cleared after use
- [ ] No memory leaks
- [ ] Buffer overflows prevented
- [ ] Integer overflows checked

### Examples

```javascript
// ✅ Clear sensitive data
function processPassword(password) {
  // Use password
  const hash = bcrypt.hashSync(password, 10);

  // Clear sensitive variable
  password = null;

  return hash;
}
```

---

## API Security

### API Requirements

- [ ] Authentication required for all endpoints
- [ ] Rate limiting implemented
- [ ] API keys secured (not in code)
- [ ] Input validation on all parameters
- [ ] CORS configured restrictively
- [ ] API versioning implemented
- [ ] Sensitive operations require additional verification
- [ ] GraphQL query depth limited
- [ ] Mass assignment prevented

### Examples

```javascript
// ✅ Rate limiting
const rateLimit = require('express-rate-limit');

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests'
});

app.use('/api/', apiLimiter);

// ✅ API key validation
app.use('/api/', (req, res, next) => {
  const apiKey = req.header('X-API-Key');
  if (!isValidApiKey(apiKey)) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  next();
});
```

---

## Quick Reference

| Category | Key Controls |
|----------|--------------|
| **Input** | Validate, sanitize, allowlist |
| **Output** | Encode per context, set headers |
| **Auth** | Strong passwords, MFA, lockout |
| **Sessions** | Secure/HttpOnly/SameSite flags |
| **Access** | Least privilege, object-level checks |
| **Crypto** | Strong algorithms, secure key management |
| **Errors** | Generic messages, log details |
| **Data** | Encrypt sensitive data, secure deletion |
| **Network** | HTTPS, TLS 1.2+, HSTS |
| **Config** | No debug mode, env variables |
| **Database** | Parameterized queries, least privilege |
| **Files** | Validate type/size, store outside webroot |
| **APIs** | Rate limit, validate, authenticate |

---

## References

- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
