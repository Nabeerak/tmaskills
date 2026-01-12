# Task Management API

A production-ready REST API built with FastAPI and SQLModel for managing tasks with full CRUD operations.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- 📊 Task status tracking (pending, in_progress, completed)
- 🎯 Priority levels (low, medium, high)
- 🔍 Filter by status and priority
- 📄 Pagination support
- 🗄️ Neon PostgreSQL database integration
- 📝 Automatic API documentation (Swagger/ReDoc)
- ⚡ Async/await for high performance
- 🛡️ Request validation with Pydantic
- 🌐 CORS support
- 🎨 Clean architecture with layered structure

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM with Pydantic integration
- **Neon PostgreSQL** - Serverless PostgreSQL database
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **asyncpg** - Async PostgreSQL driver

## Project Structure

```
task-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── core/
│   │   ├── config.py        # Configuration management
│   │   └── database.py      # Database connection
│   ├── models/
│   │   └── task.py          # SQLModel database models
│   ├── schemas/
│   │   └── task.py          # Pydantic request/response schemas
│   ├── api/
│   │   ├── deps.py          # Shared dependencies
│   │   └── v1/
│   │       ├── api.py       # Main API router
│   │       └── endpoints/
│   │           └── tasks.py # Task endpoints
│   ├── crud/
│   │   └── task.py          # CRUD operations
│   └── exceptions/
│       └── handlers.py      # Custom exception handlers
├── tests/                   # Test files (to be added)
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- Neon PostgreSQL account (or any PostgreSQL database)

## Setup Instructions

### 1. Clone or Navigate to Project Directory

```bash
cd task-management-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Neon PostgreSQL Database

1. Create a Neon account at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy your connection string

### 6. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and update the DATABASE_URL with your Neon PostgreSQL connection string:

```env
DATABASE_URL="postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/taskdb?sslmode=require"
```

### 7. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tasks/` | Create a new task |
| GET | `/api/v1/tasks/` | Get all tasks (with pagination and filters) |
| GET | `/api/v1/tasks/{id}` | Get a specific task |
| PUT | `/api/v1/tasks/{id}` | Update a task |
| PATCH | `/api/v1/tasks/{id}` | Partially update a task |
| DELETE | `/api/v1/tasks/{id}` | Delete a task |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API root and information |
| GET | `/health` | Health check |

## Usage Examples

### Create a Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "pending",
    "priority": "high"
  }'
```

### Get All Tasks

```bash
# Get all tasks with pagination
curl "http://localhost:8000/api/v1/tasks/?skip=0&limit=10"

# Filter by status
curl "http://localhost:8000/api/v1/tasks/?status=in_progress"

# Filter by priority
curl "http://localhost:8000/api/v1/tasks/?priority=high"
```

### Get a Specific Task

```bash
curl "http://localhost:8000/api/v1/tasks/1"
```

### Update a Task

```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "status": "completed",
    "priority": "medium"
  }'
```

### Delete a Task

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
```

## Task Model

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Auto | Unique identifier |
| title | string | Yes | Task title (1-200 chars) |
| description | string | No | Task description (max 2000 chars) |
| status | enum | No | pending, in_progress, completed (default: pending) |
| priority | enum | No | low, medium, high (default: medium) |
| created_at | datetime | Auto | Timestamp when task was created |
| updated_at | datetime | Auto | Timestamp when task was last updated |

### Status Values

- `pending` - Task is not started
- `in_progress` - Task is being worked on
- `completed` - Task is finished

### Priority Values

- `low` - Low priority task
- `medium` - Medium priority task (default)
- `high` - High priority task

## Response Format

### Success Response (Single Task)

```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "status": "in_progress",
  "priority": "high",
  "created_at": "2024-01-10T10:30:00Z",
  "updated_at": "2024-01-10T14:20:00Z"
}
```

### Success Response (List)

```json
{
  "items": [
    {
      "id": 1,
      "title": "Task 1",
      "description": "Description",
      "status": "pending",
      "priority": "high",
      "created_at": "2024-01-10T10:00:00Z",
      "updated_at": "2024-01-10T10:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### Error Response

```json
{
  "error": "Not Found",
  "message": "Task with id 999 not found",
  "path": "/api/v1/tasks/999"
}
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Quality

```bash
# Format code
pip install black
black app/

# Lint code
pip install ruff
ruff check app/
```

## Database Migrations (Optional)

For production, use Alembic for database migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Security Considerations

- ✅ CORS configured (update `CORS_ORIGINS` in `.env`)
- ✅ Environment variables for sensitive data
- ✅ Request validation with Pydantic
- ✅ SQL injection prevention (SQLModel uses parameterized queries)
- ✅ Error messages don't expose sensitive information
- ⚠️ Add authentication/authorization for production use
- ⚠️ Use HTTPS in production
- ⚠️ Add rate limiting for public endpoints

## Troubleshooting

### Database Connection Issues

**Error**: `asyncpg.exceptions.InvalidCatalogNameError: database "taskdb" does not exist`

**Solution**: Create the database in Neon dashboard or use an existing database name.

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Run uvicorn from the project root directory:
```bash
cd task-management-api
uvicorn app.main:app --reload
```

### SSL/TLS Errors with Neon

**Solution**: Ensure your DATABASE_URL includes `?sslmode=require`:
```
postgresql://user:pass@host/db?sslmode=require
```

## Production Deployment

### Environment Variables

Set these in your production environment:

```env
DATABASE_URL="your_production_database_url"
CORS_ORIGINS=["https://yourdomain.com"]
```

### Run with Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions, please create an issue in the repository.

---

**Built with FastAPI and SQLModel** 🚀
