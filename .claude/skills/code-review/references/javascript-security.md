# JavaScript/TypeScript Security Patterns

Security-specific patterns and vulnerabilities for JavaScript and TypeScript code review.

---

## Table of Contents

1. [Injection Vulnerabilities](#injection-vulnerabilities)
2. [Prototype Pollution](#prototype-pollution)
3. [DOM-Based XSS](#dom-based-xss)
4. [Insecure Deserialization](#insecure-deserialization)
5. [Client-Side Security](#client-side-security)
6. [npm/Dependencies](#npm-dependencies)
7. [Node.js Specific](#nodejs-specific)
8. [TypeScript Considerations](#typescript-considerations)

---

## Injection Vulnerabilities

### eval() and Function() Constructor

**Never use with user input:**

```javascript
// ❌ CRITICAL: Remote code execution
const userInput = req.query.code;
eval(userInput); // Attacker can execute ANY code

// ❌ CRITICAL: Same risk
const func = new Function(userInput);
func();

// ✅ Safe alternative: Use JSON parsing
const data = JSON.parse(userInput);

// ✅ For calculations: Use a safe expression evaluator
const math = require('mathjs');
const result = math.evaluate('2 + 2'); // Limited scope
```

### Template Literals

```javascript
// ❌ SQL injection via template literals
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// ✅ Use parameterized queries
db.query('SELECT * FROM users WHERE id = ?', [userId]);

// ❌ Command injection
const { exec } = require('child_process');
exec(`ls ${userInput}`);

// ✅ Use array form (doesn't invoke shell)
const { execFile } = require('child_process');
execFile('ls', [userInput]);
```

### NoSQL Injection

```javascript
// ❌ MongoDB injection
const user = await User.findOne({
  username: req.body.username,
  password: req.body.password
});
// Attacker sends: {"username": {"$ne": null}, "password": {"$ne": null}}

// ✅ Validate input types
if (typeof req.body.username !== 'string' || typeof req.body.password !== 'string') {
  return res.status(400).json({ error: 'Invalid input' });
}

// ✅ Use strict schema validation
const userSchema = Joi.object({
  username: Joi.string().alphanum().min(3).max(30).required(),
  password: Joi.string().min(8).required()
});
```

---

## Prototype Pollution

### Object Assignment

```javascript
// ❌ Prototype pollution vulnerability
function merge(target, source) {
  for (let key in source) {
    target[key] = source[key]; // Can modify Object.prototype
  }
  return target;
}

// Attacker payload: {"__proto__": {"isAdmin": true}}
merge({}, JSON.parse(attackerInput));

// ✅ Safe merge - check for prototype keys
function safeMerge(target, source) {
  for (let key in source) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      continue;
    }
    if (source.hasOwnProperty(key)) {
      target[key] = source[key];
    }
  }
  return target;
}

// ✅ Use Object.assign with Object.create(null)
const obj = Object.assign(Object.create(null), source);

// ✅ Or use libraries with protection
const _ = require('lodash');
_.merge({}, source); // Lodash v4.17.21+ has protection
```

### Object Destructuring

```javascript
// ❌ Vulnerable to prototype pollution
const { __proto__, ...safe } = userInput; // __proto__ still accessible

// ✅ Use allowlist approach
const allowedKeys = ['name', 'email', 'age'];
const sanitized = {};
for (const key of allowedKeys) {
  if (userInput[key] !== undefined) {
    sanitized[key] = userInput[key];
  }
}
```

---

## DOM-Based XSS

### innerHTML and outerHTML

```javascript
// ❌ XSS vulnerability
const username = new URLSearchParams(location.search).get('name');
document.getElementById('welcome').innerHTML = `Hello ${username}`;
// Attack: ?name=<img src=x onerror=alert('XSS')>

// ✅ Use textContent (doesn't parse HTML)
document.getElementById('welcome').textContent = `Hello ${username}`;

// ✅ Or sanitize HTML
import DOMPurify from 'dompurify';
document.getElementById('welcome').innerHTML = DOMPurify.sanitize(`Hello ${username}`);
```

### DOM Manipulation

```javascript
// ❌ XSS via setAttribute
const url = new URLSearchParams(location.search).get('url');
link.setAttribute('href', url);
// Attack: ?url=javascript:alert('XSS')

// ✅ Validate URL scheme
function isSafeUrl(url) {
  try {
    const parsed = new URL(url, window.location.origin);
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch {
    return false;
  }
}

if (isSafeUrl(url)) {
  link.href = url;
}
```

### Event Handlers

```javascript
// ❌ XSS via event handler
element.setAttribute('onclick', userInput);

// ✅ Use addEventListener
element.addEventListener('click', () => {
  // Safe handler
});
```

---

## Insecure Deserialization

### JSON.parse with Prototype Pollution

```javascript
// ❌ Accepts __proto__ pollution
const data = JSON.parse(untrustedInput);

// ✅ Validate against schema
const Ajv = require('ajv');
const ajv = new Ajv();
const schema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    age: { type: 'number' }
  },
  additionalProperties: false // Reject extra properties
};

const validate = ajv.compile(schema);
const data = JSON.parse(untrustedInput);
if (!validate(data)) {
  throw new Error('Invalid data');
}
```

### Node.js Serialization

```javascript
// ❌ NEVER use node-serialize or similar with untrusted data
const serialize = require('node-serialize');
const obj = serialize.unserialize(untrustedInput); // RCE vulnerability

// ✅ Use JSON only
const obj = JSON.parse(untrustedInput);
```

---

## Client-Side Security

### localStorage/sessionStorage

```javascript
// ❌ Storing sensitive data in localStorage
localStorage.setItem('sessionToken', token); // Accessible via XSS

// ✅ Use HttpOnly cookies for tokens (server-side)
// Or encrypt sensitive data before storing
import CryptoJS from 'crypto-js';
const encrypted = CryptoJS.AES.encrypt(
  data,
  userProvidedKey
).toString();
localStorage.setItem('data', encrypted);
```

### postMessage Security

```javascript
// ❌ No origin validation
window.addEventListener('message', (event) => {
  processData(event.data);
});

// ✅ Validate origin
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://trusted-site.com') {
    return;
  }
  processData(event.data);
});
```

### Client-Side Authorization

```javascript
// ❌ Client-side authorization only
if (user.role === 'admin') {
  showAdminPanel(); // Can be bypassed in dev tools
}

// ✅ Always verify on server
fetch('/api/admin/users', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(res => {
  if (res.ok) {
    showAdminPanel(); // Server verified authorization
  }
});
```

---

## npm/Dependencies

### Vulnerable Packages

```bash
# Check for vulnerabilities
npm audit
npm audit fix

# Lock dependencies
npm ci # Uses package-lock.json exactly
```

### Common Vulnerable Patterns

```json
// ❌ Vulnerable versions
{
  "dependencies": {
    "lodash": "4.17.15",      // CVE-2020-8203: Prototype pollution
    "jquery": "2.2.4",        // Multiple XSS vulnerabilities
    "axios": "0.19.0",        // CVE-2020-28168
    "express": "3.0.0",       // Very old, many CVEs
    "handlebars": "4.0.0"     // CVE-2019-19919
  }
}

// ✅ Updated versions
{
  "dependencies": {
    "lodash": "^4.17.21",
    "jquery": "^3.7.1",
    "axios": "^1.6.0",
    "express": "^4.18.0",
    "handlebars": "^4.7.8"
  }
}
```

### Dependency Confusion

```json
// ✅ Use exact registry
{
  "publishConfig": {
    "registry": "https://registry.npmjs.org/"
  }
}
```

---

## Node.js Specific

### Command Injection

```javascript
// ❌ Shell injection
const { exec } = require('child_process');
exec(`convert ${userFilename} output.pdf`); // Injection via filename

// ✅ Use execFile (no shell)
const { execFile } = require('child_process');
execFile('convert', [userFilename, 'output.pdf']);

// ✅ Or sanitize strictly
const path = require('path');
const filename = path.basename(userFilename); // Remove directory traversal
```

### Path Traversal

```javascript
// ❌ Directory traversal
const fs = require('fs');
const filepath = `/uploads/${req.params.filename}`;
fs.readFile(filepath, callback);
// Attack: GET /file/../../etc/passwd

// ✅ Validate path
const path = require('path');
const filename = path.basename(req.params.filename); // Remove path components
const filepath = path.join(__dirname, 'uploads', filename);

// Ensure path is still within uploads directory
const uploadsDir = path.join(__dirname, 'uploads');
if (!filepath.startsWith(uploadsDir)) {
  return res.status(400).send('Invalid path');
}

fs.readFile(filepath, callback);
```

### Regular Expression Denial of Service (ReDoS)

```javascript
// ❌ ReDoS vulnerability
const pattern = /^(a+)+$/;
const input = 'a'.repeat(50) + 'b'; // Takes exponential time
pattern.test(input); // Application hangs

// ✅ Use safe patterns
const pattern = /^a+$/; // Linear time

// ✅ Or use safe-regex library
const safeRegex = require('safe-regex');
if (!safeRegex(pattern)) {
  throw new Error('Unsafe regex');
}
```

### Server-Side Request Forgery (SSRF)

```javascript
// ❌ SSRF vulnerability
const axios = require('axios');
const url = req.query.url;
const response = await axios.get(url);
// Attack: ?url=http://localhost:6379/ (access internal services)

// ✅ Validate URL
const { URL } = require('url');
const allowedHosts = ['api.example.com', 'cdn.example.com'];

function isSafeUrl(urlString) {
  try {
    const url = new URL(urlString);

    // Check allowed hosts
    if (!allowedHosts.includes(url.hostname)) {
      return false;
    }

    // Block private IPs
    const privateRanges = [
      /^127\./,
      /^10\./,
      /^172\.(1[6-9]|2[0-9]|3[0-1])\./,
      /^192\.168\./,
      /^169\.254\./ // AWS metadata
    ];

    if (privateRanges.some(range => range.test(url.hostname))) {
      return false;
    }

    return true;
  } catch {
    return false;
  }
}

if (isSafeUrl(url)) {
  const response = await axios.get(url);
}
```

---

## TypeScript Considerations

### Type Safety for Security

```typescript
// ✅ Use strict types to prevent injection
type UserId = string & { __brand: 'UserId' };

function createUserId(id: string): UserId {
  // Validate format
  if (!/^[a-zA-Z0-9-]+$/.test(id)) {
    throw new Error('Invalid user ID');
  }
  return id as UserId;
}

function getUser(userId: UserId) {
  // userId is guaranteed to be validated
  return db.query('SELECT * FROM users WHERE id = ?', [userId]);
}

// Usage
const userId = createUserId(req.params.id); // Validation enforced
const user = await getUser(userId);
```

### Avoid 'any' Type

```typescript
// ❌ Loses type safety
function processData(data: any) {
  // No type checking
  return eval(data.code); // Dangerous
}

// ✅ Use specific types
interface UserInput {
  name: string;
  age: number;
}

function processData(data: UserInput) {
  // Type-safe
  return `${data.name} is ${data.age} years old`;
}
```

### Runtime Validation

```typescript
// ✅ Validate at runtime (types are compile-time only)
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().max(150)
});

app.post('/users', (req, res) => {
  try {
    const user = UserSchema.parse(req.body); // Runtime validation
    // user is type-safe and validated
  } catch (error) {
    return res.status(400).json({ error: 'Validation failed' });
  }
});
```

---

## Framework-Specific Patterns

### Express.js

```javascript
// ✅ Security middleware
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

app.use(helmet()); // Security headers
app.use(express.json({ limit: '10kb' })); // Limit body size

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use('/api/', limiter);

// ✅ CSRF protection
const csrf = require('csurf');
app.use(csrf({ cookie: true }));
```

### React

```jsx
// ❌ XSS via dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ Use text content
<div>{userInput}</div>

// ✅ Or sanitize HTML
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{
  __html: DOMPurify.sanitize(userInput)
}} />
```

### Vue.js

```vue
<!-- ❌ XSS via v-html -->
<div v-html="userInput"></div>

<!-- ✅ Use text interpolation -->
<div>{{ userInput }}</div>

<!-- ✅ Or sanitize -->
<div v-html="$sanitize(userInput)"></div>
```

---

## Security Tools for JavaScript

### Linting

```javascript
// .eslintrc.js
module.exports = {
  plugins: ['security'],
  extends: ['plugin:security/recommended'],
  rules: {
    'security/detect-eval-with-expression': 'error',
    'security/detect-non-literal-regexp': 'warn',
    'security/detect-unsafe-regex': 'error',
    'security/detect-object-injection': 'warn'
  }
};
```

### Static Analysis

```bash
# npm audit
npm audit --audit-level=moderate

# Snyk
npx snyk test

# RetireJS (outdated libraries)
npm install -g retire
retire --path /path/to/project
```

---

## Quick Reference

| Vulnerability | Pattern | Mitigation |
|---------------|---------|------------|
| **eval() RCE** | `eval(userInput)` | Never use eval, use JSON.parse |
| **Prototype Pollution** | `obj[key] = val` | Check for __proto__, use allowlist |
| **DOM XSS** | `.innerHTML = userInput` | Use `.textContent` or sanitize |
| **NoSQL Injection** | `{$ne: null}` | Validate input types |
| **Command Injection** | `exec(\`cmd ${input}\`)` | Use execFile with array args |
| **Path Traversal** | `fs.readFile(userPath)` | Use path.basename(), validate |
| **SSRF** | `axios.get(userUrl)` | Validate URL, allowlist hosts |
| **ReDoS** | `/(a+)+$/` | Use safe-regex, limit input |

---

## References

- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [OWASP NodeGoat](https://github.com/OWASP/NodeGoat)
- [npm Security Best Practices](https://docs.npmjs.com/packages-and-modules/securing-your-code)
- [Snyk JavaScript Security](https://snyk.io/learn/javascript-security/)
