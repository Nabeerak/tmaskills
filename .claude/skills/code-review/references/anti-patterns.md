# Code Review Anti-Patterns

Common mistakes and anti-patterns to avoid during code reviews.

---

## Table of Contents

1. [Process Anti-Patterns](#process-anti-patterns)
2. [Communication Anti-Patterns](#communication-anti-patterns)
3. [Technical Anti-Patterns](#technical-anti-patterns)
4. [Coding Anti-Patterns](#coding-anti-patterns)

---

## Process Anti-Patterns

### 1. Iterative Nitpicking

**Problem**: Reviewer stops after finding one issue, waits for fix, then finds another issue they could have mentioned initially. Multiple unnecessary round trips.

**Impact**: Frustrates developers, slows velocity, wastes time

**Example**:
```
Round 1: "Please rename this variable"
[Author fixes]
Round 2: "Also, this function should be extracted"
[Author fixes]
Round 3: "And you need to add error handling"
[Author fixes]
```

**Solution**:
- Review the **entire PR once**
- Provide **all feedback together**
- Use review tools that let you draft comments before publishing

---

### 2. Scope Creep

**Problem**: Refusing to approve reasonable code until substantial refactors or redesigns of **unrelated** areas are completed.

**Impact**: Blocks progress, demoralizes team, creates huge PRs

**Example**:
```
PR: "Fix bug in user login"
Reviewer: "Before merging, please:
- Refactor the entire auth module
- Add caching layer
- Migrate to new ORM
- Update all tests
- Write migration guide"
```

**Solution**:
- **Accept the PR** if it solves its stated problem
- **File separate issues** for improvements
- Apply the **boy scout rule** (leave code slightly better), not a complete rewrite

---

### 3. Inconsistent Standards

**Problem**: Accepting code patterns in one PR, then rejecting identical patterns in another. Keeping developers off-balance by changing expectations without notice.

**Impact**: Confusion, frustration, distrust in review process

**Example**:
```
PR #123: Uses async/await - APPROVED
PR #124: Uses async/await - REJECTED ("use Promises")
PR #125: Uses Promises - REJECTED ("use async/await")
```

**Solution**:
- **Document** team coding standards
- **Automate** enforcement via linters
- **Update** standards document when decisions change
- Be **consistent** in feedback

---

### 4. Large Batch Reviews

**Problem**: Combining multiple unrelated code changes into a single massive PR.

**Impact**: Cluttered reviews, longer cycles, harder to understand, difficult to roll back

**Example**:
```
PR: "Q1 Updates"
- New user feature (500 lines)
- Bug fixes (200 lines)
- Dependency updates (100 files)
- Code cleanup (300 lines)
- Database migration (50 lines)
Total: 2000+ lines, 150+ files
```

**Solution**:
- **Split into separate PRs** by concern
- Keep PRs **under 400 lines**
- One PR = One logical change

---

### 5. Lack of Action on Findings

**Problem**: Code review findings are noted but not acted upon or followed up on. Same issues appear in subsequent PRs.

**Impact**: Review process becomes redundant, quality degrades

**Example**:
```
Every PR from Developer X:
"Please add input validation"
[No change in next PR]
"Please add input validation"
[No change in next PR]
"Please add input validation"
```

**Solution**:
- **Block merge** until issues fixed
- **Track** recurring issues
- **Coach** developers who repeatedly ignore feedback
- **Automate** common issues (linting, security scanning)

---

### 6. No Automated Feedback

**Problem**: Neglecting automated tools, requiring peers to focus on trivial issues rather than complex logic.

**Impact**: Wastes reviewer time, slows reviews, misses real issues

**Example**:
```
Manual reviews spent on:
- "Add semicolon here"
- "Fix indentation"
- "Remove unused import"
- "Line too long"

Instead of:
- Security vulnerabilities
- Logic errors
- Architecture issues
```

**Solution**:
- **Automate** formatting (Prettier, Black)
- **Automate** linting (ESLint, Pylint)
- **Automate** security scanning
- **Require** CI to pass before review

---

## Communication Anti-Patterns

### 1. Unconstructive Reviews

**Problem**: Code reviews with harsh, hostile tone or vague feedback that demoralize developers.

**Impact**: Damages team culture, reduces collaboration, creates fear of code review

**Example**:
```
❌ "This is terrible code."
❌ "Did you even think about this?"
❌ "This is obviously wrong."
❌ "Why would you do it this way?"
❌ "Everyone knows this is bad."
```

**Solution**:
```
✅ "This has a security vulnerability. Consider using
   parameterized queries to prevent SQL injection."

✅ "I'm not sure I understand the approach here. Could
   you explain why you chose this pattern?"

✅ "This works, but there's a built-in method that
   handles this case: Array.filter(). Would simplify
   the code."
```

---

### 2. Vague Feedback

**Problem**: Comments like "fix this" or "this is wrong" without explanation or guidance.

**Impact**: Developer doesn't know what's wrong or how to fix it

**Example**:
```
❌ "This needs work."
❌ "Not good."
❌ "Fix this."
❌ "Wrong approach."
```

**Solution**:
```
✅ "This function has high cyclomatic complexity (15).
   Consider extracting the validation logic into a
   separate function:

   function validateUser(user) {
     // validation logic
   }

   This would make the code more testable and readable."
```

---

### 3. Personal Attacks

**Problem**: Attacking the person instead of the code.

**Impact**: Hostile environment, reduced collaboration

**Example**:
```
❌ "You clearly don't understand async/await."
❌ "Are you even a developer?"
❌ "This is amateur work."
```

**Solution**:
- Focus on **code**, not person
- Use "we" language: "We should..." not "You should..."
- Assume **positive intent**
- Be **respectful** and **professional**

---

## Technical Anti-Patterns

### 1. Rubber Stamp Reviews

**Problem**: Approving without actually reviewing ("LGTM" without reading code).

**Impact**: Bugs slip through, security issues missed, quality degrades

**Solution**:
- **Actually read** the code
- **Run** the code locally if needed
- **Test** the changes
- Ask yourself: "Would I be comfortable maintaining this?"

---

### 2. Perfectionism

**Problem**: Blocking PRs over minor style preferences or subjective opinions.

**Impact**: Slows velocity, frustrates team, creates bike-shedding

**Example**:
```
PR blocked because:
- Variable named 'data' instead of 'userData'
- Using forEach instead of for...of
- Comment formatting preference
```

**Solution**:
- **Automate** style enforcement
- Use **"NITPICK"** label for optional suggestions
- Focus on **substance** over style
- Ask: "Is this blocking issue or preference?"

---

### 3. Not Testing Changes

**Problem**: Approving code without verifying it works.

**Impact**: Broken code merged, bugs in production

**Solution**:
- **Pull** the branch locally
- **Run** tests
- **Test** manually for UI changes
- Verify edge cases

---

## Coding Anti-Patterns

### 1. Copy and Paste

**Problem**: Repeating the same code in multiple places without abstraction.

**Impact**: Hard to maintain, bugs in multiple places, violates DRY

**Example**:
```javascript
// ❌ Copy-paste anti-pattern
function processUser(user) {
  if (!user.email || !user.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}

function updateUser(user) {
  if (!user.email || !user.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}

function createUser(user) {
  if (!user.email || !user.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}
```

**Solution**:
```javascript
// ✅ Extract to reusable function
function validateEmail(email) {
  if (!email || !email.includes('@')) {
    throw new Error('Invalid email');
  }
}

function processUser(user) {
  validateEmail(user.email);
  // ...
}
```

---

### 2. God Class

**Problem**: A class with too many responsibilities, methods, and dependencies.

**Impact**: Hard to understand, test, maintain; violates single responsibility

**Example**:
```python
# ❌ God class anti-pattern
class UserManager:
    def create_user(self): ...
    def delete_user(self): ...
    def send_email(self): ...
    def generate_report(self): ...
    def process_payment(self): ...
    def upload_file(self): ...
    def validate_input(self): ...
    # 50+ methods
```

**Solution**:
```python
# ✅ Split responsibilities
class UserService:
    def create_user(self): ...
    def delete_user(self): ...

class EmailService:
    def send_email(self): ...

class ReportService:
    def generate_report(self): ...

class PaymentService:
    def process_payment(self): ...
```

---

### 3. Magic Numbers

**Problem**: Literal values used without explanation.

**Impact**: Hard to understand, error-prone, hard to change

**Example**:
```javascript
// ❌ Magic numbers
if (user.age > 18) {
  if (account.balance < 10000) {
    if (attempts < 3) {
      // What do these numbers mean?
    }
  }
}
```

**Solution**:
```javascript
// ✅ Named constants
const LEGAL_AGE = 18;
const WITHDRAWAL_LIMIT = 10000;
const MAX_LOGIN_ATTEMPTS = 3;

if (user.age > LEGAL_AGE) {
  if (account.balance < WITHDRAWAL_LIMIT) {
    if (attempts < MAX_LOGIN_ATTEMPTS) {
      // Clear and maintainable
    }
  }
}
```

---

### 4. Premature Optimization

**Problem**: Optimizing code for performance before proving it's necessary.

**Impact**: Over-engineering, complexity, reduced readability

**Example**:
```python
# ❌ Premature optimization
class UserCache:
    def __init__(self):
        self.cache = {}
        self.lru_queue = deque()
        self.timestamps = {}

    def get(self, key):
        # Complex caching logic
        # But: only 10 users in system
        # Called once per day
```

**Solution**:
```python
# ✅ Simple until proven slow
def get_user(user_id):
    return db.query("SELECT * FROM users WHERE id = ?", user_id)

# Add caching AFTER profiling shows need
```

---

### 5. Spaghetti Code

**Problem**: Code with little structure, tangled control flow, hard to follow.

**Impact**: Unmaintainable, bug-prone, hard to test

**Example**:
```javascript
// ❌ Spaghetti code
function process(data) {
  for (let i = 0; i < data.length; i++) {
    if (data[i].type === 'A') {
      if (data[i].status === 'active') {
        for (let j = 0; j < data[i].items.length; j++) {
          if (data[i].items[j].valid) {
            // deeply nested logic
            if (condition1) {
              if (condition2) {
                // more nesting
              }
            }
          }
        }
      }
    }
  }
}
```

**Solution**:
```javascript
// ✅ Structured code
function process(data) {
  const activeTypeA = data.filter(isActiveTypeA);
  activeTypeA.forEach(processItems);
}

function isActiveTypeA(item) {
  return item.type === 'A' && item.status === 'active';
}

function processItems(data) {
  const validItems = data.items.filter(item => item.valid);
  validItems.forEach(processValidItem);
}
```

---

### 6. Dead Code

**Problem**: Code that is no longer executed or needed.

**Impact**: Confusion, maintenance burden, security risk

**Example**:
```python
# ❌ Dead code
def process_user(user):
    # This function is never called
    # Removed from all call sites 6 months ago
    # But still in codebase
    old_legacy_logic()
```

**Solution**:
- **Delete** unused code
- Use **version control** to recover if needed
- Don't comment out code "just in case"

---

### 7. Inconsistent Error Handling

**Problem**: Different error handling patterns throughout codebase.

**Impact**: Unpredictable behavior, hard to debug

**Example**:
```javascript
// ❌ Inconsistent error handling
function a() {
  return null; // Returns null on error
}

function b() {
  throw new Error(); // Throws on error
}

function c() {
  return { error: 'message' }; // Returns error object
}

function d() {
  console.error('Error'); // Logs error, returns undefined
}
```

**Solution**:
```javascript
// ✅ Consistent error handling
function a() {
  try {
    // ...
  } catch (error) {
    throw new ApiError('Operation failed', error);
  }
}

function b() {
  try {
    // ...
  } catch (error) {
    throw new ApiError('Operation failed', error);
  }
}

// Consistent pattern across codebase
```

---

## Detection in Code Review

### Red Flags to Watch For

| Anti-Pattern | Red Flags |
|--------------|-----------|
| **Copy-Paste** | Similar code blocks, repeated logic |
| **God Class** | Class >500 lines, >20 methods |
| **Magic Numbers** | Unexplained literals in conditions |
| **Premature Optimization** | Complex caching/optimization without profiling data |
| **Spaghetti Code** | Nesting >4 levels, cyclomatic complexity >10 |
| **Dead Code** | Unreachable code, unused imports, commented code |

---

## How to Provide Feedback on Anti-Patterns

### Template

```markdown
**Anti-Pattern Detected**: [Name]

**Issue**: [Specific problem in this code]

**Impact**: [Why this matters]

**Suggestion**:
```[language]
[Example fix]
```

**Reference**: [Link to documentation/best practice]
```

### Example

```markdown
**Anti-Pattern Detected**: God Class

**Issue**: UserService has 45 methods handling user management,
email sending, payment processing, and report generation.

**Impact**: Hard to test, maintain, and understand. Violates
single responsibility principle.

**Suggestion**:
Consider splitting into focused classes:
- UserService (user CRUD)
- EmailService (email sending)
- PaymentService (payment processing)
- ReportService (report generation)

**Reference**: https://refactoring.guru/smells/large-class
```

---

## Quick Reference

### Process Anti-Patterns

| Anti-Pattern | Solution |
|--------------|----------|
| Iterative Nitpicking | Review all at once |
| Scope Creep | Accept PR, file separate issues |
| Inconsistent Standards | Document standards, automate |
| Large Batch Reviews | Split PRs by concern |
| No Automated Feedback | Add linting, formatting to CI |

### Communication Anti-Patterns

| Anti-Pattern | Solution |
|--------------|----------|
| Unconstructive Reviews | Be specific, kind, actionable |
| Vague Feedback | Explain what and why |
| Personal Attacks | Focus on code, not person |

### Coding Anti-Patterns

| Anti-Pattern | Solution |
|--------------|----------|
| Copy-Paste | Extract to reusable function |
| God Class | Split by responsibility |
| Magic Numbers | Use named constants |
| Premature Optimization | Optimize when proven slow |
| Spaghetti Code | Extract functions, reduce nesting |
| Dead Code | Delete unused code |

---

## References

- [Code Review Anti-Patterns](https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/code-review-antipatterns/)
- [AWS DevOps Guidance: Anti-patterns](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-code-review.html)
- [Code Review Anti-Patterns - DEV Community](https://dev.to/adam_b/code-review-anti-patterns-2e6a)
- [Refactoring Guru: Code Smells](https://refactoring.guru/refactoring/smells)
