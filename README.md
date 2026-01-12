# TMA Skills

A comprehensive collection of production-grade skills for Claude Code and a FastAPI task management system.

## Repository Contents

This repository contains:
- **7 Production-Ready Claude Skills** for AI-assisted development
- **Task Management API** - A FastAPI-based REST API built using the skills in this collection

---

## Skills Overview

| # | Skill | Description | Status |
|---|-------|-------------|--------|
| 1 | [fastapi-builder](.claude/skills/fastapi-builder/) | Build production-ready REST APIs with FastAPI | Used in Task API |
| 2 | [pytest-tdd](.claude/skills/pytest-tdd/) | Implement Test-Driven Development workflows with pytest | Used in Task API |
| 3 | [sqlmodel-database](.claude/skills/sqlmodel-database/) | Design and implement database schemas with SQLModel | Used in Task API |
| 4 | [skill-creator-pro](.claude/skills/skill-creator-pro/) | Create production-grade, reusable skills | Core Tool |
| 5 | [code-review](.claude/skills/code-review/) | Security-focused code reviews with OWASP alignment | Built with skill-creator-pro |
| 6 | [web-theme-builder](.claude/skills/web-theme-builder/) | Build production-ready website themes with Tailwind CSS | Built with skill-creator-pro |
| 7 | [skill-validator](.claude/skills/skill-validator/) | Validate skills against production-level criteria | Quality Assurance |

---

## Task Management API

A production-ready REST API built using the **fastapi-builder**, **pytest-tdd**, and **sqlmodel-database** skills.

**Tech Stack**:
- FastAPI (REST API framework)
- SQLModel (Database ORM)
- Pytest (Testing framework)
- SQLite (Database)

**Features**:
- Full CRUD operations for tasks
- Request/response validation with Pydantic
- Comprehensive test suite (unit + integration tests)
- Proper error handling and exception management
- OpenAPI documentation

**Location**: [task-management-api/](task-management-api/)

---

## Skill Details

### 1. fastapi-builder

**Purpose**: Build production-ready REST APIs with FastAPI following best practices.

**Key Features**:
- Proper project structure (models, schemas, CRUD, endpoints)
- Request/response validation with Pydantic
- Dependency injection patterns
- Error handling and custom exceptions
- Database integration with SQLModel
- CORS and security configuration

**Use When**: Creating FastAPI applications, building REST APIs, implementing CRUD operations.

---

### 2. pytest-tdd

**Purpose**: Implement Test-Driven Development workflows with pytest.

**Key Features**:
- Unit and integration test patterns
- Fixtures and parametrization
- Mocking and dependency injection
- AAA pattern (Arrange-Act-Assert)
- Async testing support
- Code coverage measurement

**Use When**: Writing tests, setting up pytest, implementing TDD workflows, measuring coverage.

---

### 3. sqlmodel-database

**Purpose**: Design and implement database schemas with SQLModel.

**Key Features**:
- Model definitions with type safety
- Relationships (one-to-many, many-to-many)
- CRUD operations with sessions
- Complex queries with joins
- Alembic migrations
- FastAPI integration

**Use When**: Creating database models, implementing relationships, writing queries, setting up migrations.

---

### 4. skill-creator-pro

**Purpose**: Create production-grade, reusable skills that extend Claude's capabilities.

**Key Features**:
- Gathers context from codebase and authentic sources
- Structured skill creation workflow
- Domain-specific intelligence building
- Reusability and adaptability patterns
- Quality enforcement

**Use When**: Building new skills for domain-specific tasks.

**Success Stories**: Used to create the **code-review** and **web-theme-builder** skills in this repository.

---

### 5. code-review

**Purpose**: Performs security-focused code reviews with OWASP alignment.

**Key Features**:
- OWASP Top 10 security vulnerability detection
- JavaScript/TypeScript and Python security patterns
- Anti-patterns and best practices validation
- Automated scanning scripts (secret detection, dependency checks)
- Actionable recommendations

**Use When**: Reviewing code, checking for security vulnerabilities, auditing code quality.

**Built With**: skill-creator-pro

---

### 6. web-theme-builder

**Purpose**: Build production-ready website themes with pre-configured design systems.

**Key Features**:
- 8 aesthetic styles (Modern/Minimalist, Corporate, Creative, Dark/Tech, etc.)
- Pre-configured color palettes and typography pairings
- Component libraries (buttons, cards, forms, navigation)
- Tailwind CSS configurations
- Responsive design patterns

**Use When**: Creating website themes, designing landing pages, building component libraries.

**Built With**: skill-creator-pro

---

### 7. skill-validator

**Purpose**: Validate skills against production-level quality criteria.

**Key Features**:
- 9-category scoring system (Structure, Content, User Interaction, etc.)
- Production-level validation criteria
- Actionable improvement recommendations
- Scores from 0-100

**Use When**: Reviewing, auditing, or improving skills to ensure quality standards.

---

## Installation

### Installing Skills

Copy the skill folders to your Claude Code skills directory:

```bash
# macOS/Linux
cp -r .claude/skills/* ~/.claude/skills/

# Windows
xcopy /E /I .claude\skills\* %USERPROFILE%\.claude\skills\
```

### Running the Task Management API

```bash
cd task-management-api

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

API will be available at `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Repository Structure

```
tmaskills/
├── README.md                              # This file
├── .claude/
│   └── skills/                           # Claude Code skills
│       ├── fastapi-builder/              # FastAPI development skill
│       ├── pytest-tdd/                   # Testing skill
│       ├── sqlmodel-database/            # Database design skill
│       ├── skill-creator-pro/            # Skill creation tool
│       ├── code-review/                  # Code review skill
│       ├── web-theme-builder/            # Theme building skill
│       └── skill-validator/              # Skill validation tool
└── task-management-api/                  # FastAPI project
    ├── app/
    │   ├── api/                          # API endpoints
    │   ├── core/                         # Configuration & database
    │   ├── crud/                         # CRUD operations
    │   ├── models/                       # SQLModel models
    │   ├── schemas/                      # Pydantic schemas
    │   └── main.py                       # FastAPI application
    ├── tests/
    │   ├── unit/                         # Unit tests
    │   └── integration/                  # Integration tests
    └── requirements.txt                  # Python dependencies
```

---

## How This Repository Was Built

1. **skill-creator-pro** was used to create the **code-review** and **web-theme-builder** skills
2. **fastapi-builder**, **pytest-tdd**, and **sqlmodel-database** skills were used to build the **task-management-api**
3. **skill-validator** was used to ensure all skills meet production-level quality standards

This demonstrates the power of reusable AI skills - once created, they can be used to build other skills and production applications.

---

## Contributing

1. Fork this repository
2. Create your skill using `skill-creator-pro`
3. Validate with `skill-validator` (aim for 90+ score)
4. Submit a pull request

---

## License

MIT License - See individual skill folders for details.

---

## Related Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
