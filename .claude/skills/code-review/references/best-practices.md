# Code Review Best Practices

Industry best practices for conducting effective code reviews based on research and 2025-2026 standards.

---

## Core Principles

### 1. Keep Pull Requests Small

**Guideline**: Aim for PRs under 400 lines of code.

**Why**: Review quality drops sharply beyond ~400 lines. Teams that keep PRs small see:
- Up to 40% fewer production defects
- 3× faster review cycles
- Better reviewer focus and thoroughness

**How to achieve**:
```
✅ Good PR sizes:
- Single feature: 100-250 lines
- Bug fix: 10-50 lines
- Refactoring: 150-300 lines

❌ Avoid:
- Multiple features: 1000+ lines
- Mixed concerns: feature + refactor + bug fixes
- "Cleanup" commits that touch many files
```

---

### 2. Automate Trivial Feedback

**Guideline**: Wire linting, formatting, and static analysis into CI so humans review logic, not style.

**Tools to automate**:

```yaml
# .github/workflows/ci.yml
name: CI
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: |
          npm run lint          # ESLint, Prettier
          npm run type-check    # TypeScript
          npm audit             # Security scan
          npm test              # Unit tests
```

**What to automate**:
- Code formatting (Prettier, Black)
- Linting rules (ESLint, Pylint)
- Type checking (TypeScript, mypy)
- Security scanning (npm audit, Bandit)
- Test coverage
- Build verification

---

### 3. Focus on Business Value

**Guideline**: Every line of code should serve a purpose tied to product requirements or business outcomes.

**Review questions**:
- Does this solve the actual problem?
- Is this the right solution for the requirements?
- Does this align with product goals?
- Is the complexity justified by the value?

**Example**:
```javascript
// ❌ Over-engineered for simple requirement
class UserNameFormatterFactory {
  createFormatter(type) {
    return new ConcreteUserNameFormatter(type);
  }
}

// ✅ Simple solution for simple requirement
function formatUserName(user) {
  return `${user.firstName} ${user.lastName}`;
}
```

---

### 4. Review Speed Matters

**Guideline**: Respond to review requests within 24 hours (ideally same day).

**Why**: Fast reviews:
- Increase team velocity
- Reduce context switching
- Maintain developer momentum
- Improve collaboration

**Best practices**:
- Block time daily for reviews
- Prioritize reviews over new work
- Use asynchronous communication
- Batch similar reviews together

---

### 5. Be Kind and Constructive

**Guideline**: Provide specific, actionable feedback with context.

**Good feedback patterns**:
```
✅ "Consider using Array.map() here instead of forEach with push.
    It's more idiomatic and returns a new array:
    `const ids = users.map(u => u.id)`"

✅ "This could expose user data if the session isn't validated.
    Should we add an auth check here?"

✅ "Nice use of early returns to reduce nesting!
    This is much more readable."

❌ "This is wrong."

❌ "Why didn't you use map()?"

❌ "Everyone knows you shouldn't do it this way."
```

---

## Review Checklist

### Functionality

- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error cases handled appropriately
- [ ] No unintended side effects
- [ ] Backwards compatible (if applicable)

### Design & Architecture

- [ ] Fits with existing architecture
- [ ] Follows SOLID principles
- [ ] Appropriate level of abstraction
- [ ] No premature optimization
- [ ] No over-engineering

### Code Quality

- [ ] Readable and self-documenting
- [ ] Variables/functions named clearly
- [ ] No code duplication (DRY)
- [ ] Functions are single-purpose
- [ ] Complexity is manageable

### Security

- [ ] No security vulnerabilities (see OWASP Top 10)
- [ ] Input validated
- [ ] Output encoded
- [ ] Authentication/authorization correct
- [ ] No sensitive data exposed

### Tests

- [ ] Tests added/updated
- [ ] Tests cover happy path and edge cases
- [ ] Tests are maintainable
- [ ] No flaky tests
- [ ] Test coverage adequate

### Performance

- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No N+1 queries
- [ ] Caching used appropriately
- [ ] Resource usage reasonable

### Documentation

- [ ] Complex logic documented
- [ ] API changes documented
- [ ] README updated if needed
- [ ] Comments explain "why", not "what"

---

## Review Workflow

### 1. Before Requesting Review

**Author checklist**:
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Linting passes
- [ ] PR description explains what and why
- [ ] Screenshots/videos added (for UI changes)
- [ ] Breaking changes noted
- [ ] Migration plan documented (if needed)

### 2. During Review

**Reviewer actions**:
1. Read PR description and linked issues
2. Understand the context and requirements
3. Review tests first (understand expected behavior)
4. Review main logic
5. Check edge cases and error handling
6. Look for security issues
7. Consider maintainability and future changes
8. Leave specific, actionable comments
9. Approve or request changes with clear guidance

### 3. After Review

**Author actions**:
- Respond to all comments
- Make requested changes
- Re-request review
- Merge when approved

---

## Review Focus Areas by PR Type

### New Features

Focus on:
- Architecture fit
- Test coverage
- Documentation
- Edge cases
- Security implications

### Bug Fixes

Focus on:
- Root cause addressed (not symptoms)
- No regression
- Test added to prevent recurrence
- Similar bugs elsewhere?

### Refactoring

Focus on:
- Behavior unchanged
- Improvement justification
- No unrelated changes
- Tests still pass

### Performance Optimization

Focus on:
- Benchmarks/metrics provided
- No premature optimization
- Readability not sacrificed
- Complexity justified

---

## PR Size Guidelines

| Size | Lines Changed | Review Time | Best For |
|------|---------------|-------------|----------|
| **Tiny** | 1-10 | <5 min | Typos, config tweaks |
| **Small** | 10-100 | 10-15 min | Bug fixes, small features |
| **Medium** | 100-400 | 30-60 min | Features, refactors |
| **Large** | 400-1000 | 2+ hours | Avoid if possible |
| **Huge** | 1000+ | 4+ hours | Split into smaller PRs |

---

## Comment Types and Examples

### 1. Must Fix (Blocking)

Use for: Security issues, bugs, breaking changes

```
🚨 BLOCKING: This allows SQL injection. Use parameterized queries:
```sql
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```
```

### 2. Suggestion (Non-blocking)

Use for: Improvements, alternative approaches

```
💡 SUGGESTION: Consider extracting this to a helper function
for reusability:

```javascript
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```
```

### 3. Question

Use for: Clarification, understanding intent

```
❓ QUESTION: Why do we need to cache this data?
Is it called frequently enough to justify the complexity?
```

### 4. Nitpick (Minor, optional)

Use for: Style preferences, minor improvements

```
🔧 NITPICK (optional): Could use destructuring here:
`const { name, email } = user;`
```

### 5. Praise

Use for: Good patterns, clever solutions

```
👍 NICE: Great use of early returns here.
Much more readable than nested if statements.
```

---

## Managing Disagreements

### When You Disagree with Feedback

1. **Understand**: Ask clarifying questions
2. **Context**: Explain your reasoning
3. **Evidence**: Provide data or references
4. **Compromise**: Suggest alternatives
5. **Escalate**: Involve tech lead if needed

**Example dialogue**:
```
Author: "I chose Promise.all() here for parallel execution
to improve performance. Running them sequentially would take
3× longer based on profiling."

Reviewer: "Good point. Could you add a comment explaining
why parallel execution is needed here?"

Author: "Done! Added comment with profiling results."
```

---

## AI-Assisted Code Review (2025-2026)

### Challenges with AI-Generated Code

- **Volume**: 84% of developers use AI tools, generating more code
- **Quality**: 46% distrust AI output accuracy
- **Context**: AI lacks business context
- **Security**: AI may generate vulnerable patterns

### Best Practices for Reviewing AI Code

1. **Extra scrutiny on security**
   - Verify input validation
   - Check for injection vulnerabilities
   - Validate authentication/authorization

2. **Test thoroughly**
   - Don't trust AI-generated tests alone
   - Add edge case tests
   - Test error conditions

3. **Check for anti-patterns**
   - Over-engineering
   - Unnecessary complexity
   - Outdated patterns

4. **Verify business logic**
   - Ensure requirements met
   - Validate assumptions
   - Check edge cases

---

## Metrics and Goals

### Healthy Review Metrics

| Metric | Target | Warning |
|--------|--------|---------|
| **Review turnaround** | <24 hours | >48 hours |
| **PR size** | 100-400 LOC | >1000 LOC |
| **Comments per PR** | 5-15 | >30 |
| **Approval time** | <2 hours | >1 day |
| **Iterations** | 1-2 | >4 |

### Measuring Effectiveness

- **Defect rate**: Bugs found in review vs. production
- **Cycle time**: Time from PR open to merge
- **Coverage**: % of code reviewed
- **Engagement**: % of team participating
- **Learning**: Knowledge shared through reviews

---

## Common Pitfalls to Avoid

### 1. Iterative Nitpicking

**Problem**: Reviewing in multiple passes, mentioning issues one at a time

**Solution**: Review the entire PR once, provide all feedback together

### 2. Scope Creep

**Problem**: Requesting refactors unrelated to the PR

**Solution**: File separate issues for improvements, approve PR if it solves its problem

### 3. Inconsistent Standards

**Problem**: Accepting patterns in one PR, rejecting in another

**Solution**: Document team standards, automate enforcement

### 4. Perfectionism

**Problem**: Blocking PRs for minor style issues

**Solution**: Use "NITPICK" labels, focus on substance over style

### 5. Review Fatigue

**Problem**: Large PRs cause rushed, incomplete reviews

**Solution**: Enforce PR size limits, split large changes

---

## Tools and Automation

### Review Tools

```javascript
// .github/CODEOWNERS
# Auto-assign reviewers
/src/auth/*           @security-team
/src/api/*            @backend-team
/src/components/*     @frontend-team
*.sql                 @database-team
```

### Review Templates

```markdown
## PR Template

### What
[Brief description of changes]

### Why
[Business context and motivation]

### How
[Technical approach]

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manually tested

### Screenshots
[For UI changes]

### Checklist
- [ ] No console.logs or debug code
- [ ] No hardcoded credentials
- [ ] Documentation updated
- [ ] Backwards compatible
```

---

## References

- [Google's Code Review Developer Guide](https://google.github.io/eng-practices/review/)
- [Top Code Review Best Practices 2026](https://zencoder.ai/blog/code-review-best-practices)
- [SmartBear Code Review Best Practices](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)
- [Swarmia Complete Guide to Code Reviews](https://www.swarmia.com/blog/a-complete-guide-to-code-reviews/)
