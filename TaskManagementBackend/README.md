# Task Management Backend API

A robust REST API built with **FastAPI** for managing user tasks with authentication and authorization. This application provides a complete task management system with user registration, login, and CRUD operations for tasks with JWT-based authentication.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Database Schema](#database-schema)
- [Error Handling](#error-handling)
- [Development](#development)
- [License](#license)

## ✨ Features

- **User Authentication**: User registration and login with JWT tokens
- **Password Security**: Passwords are hashed using `pwdlib` before storage
- **Task Management**: Create, read, update, and delete tasks
- **User Authorization**: Users can only access and modify their own tasks
- **Database Migrations**: Using Alembic for managing database schema changes
- **Input Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Comprehensive HTTP exception handling
- **Dependency Injection**: Clean architecture using FastAPI's dependency injection

## 🛠 Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.135.1
- **Database**: PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Authentication**: JWT (JSON Web Tokens) with [PyJWT](https://pyjwt.readthedocs.io/)
- **Password Hashing**: [pwdlib](https://github.com/caronc/pwdlib)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/) v2
- **Database Driver**: psycopg2-binary
- **Server**: Uvicorn

## 📁 Project Structure

```
TaskManagementBackend/
├── src/
│   ├── tasks/
│   │   ├── models.py           # Database model for Task
│   │   ├── dtos.py             # Pydantic schemas for request/response
│   │   ├── controller.py       # Business logic for task operations
│   │   └── router.py           # FastAPI routes for tasks
│   ├── user/
│   │   ├── models.py           # Database model for User
│   │   ├── dtos.py             # Pydantic schemas for user operations
│   │   ├── controller.py       # Business logic for user operations
│   │   ├── router.py           # FastAPI routes for user
│   │   └── Authentication.py   # Authentication utilities (reserved)
│   └── utils/
│       ├── db.py               # Database connection and session setup
│       ├── settings.py         # Environment configuration
│       └── helpers.py          # Helper functions (is_authenticated dependency)
├── migrations/                  # Alembic migration files
├── main.py                      # Application entry point
├── alembic.ini                  # Alembic configuration
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (not included)
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Virtual environment tool (venv, conda, etc.)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TaskManagementBackend
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DB_CONNECTION=postgresql://username:password@localhost:5432/task_management_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
EXP_TIME=30

# Environment
APP_ENV=development
```

### Configuration Details:

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_CONNECTION` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/dbname` |
| `SECRET_KEY` | JWT secret key for token encoding/decoding | `your-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `EXP_TIME` | Token expiration time in minutes | `30` |

## 🗄️ Database Setup

### Create Database

```bash
# Using PostgreSQL
createdb task_management_db
```

### Run Migrations

```bash
# From the project root directory
alembic upgrade head
```

### Create Initial Migration (if needed)

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## ▶️ Running the Application

### Start the server

```bash
# From the project root directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Docs (ReDoc)**: `http://localhost:8000/redoc`

## 📚 API Endpoints

### User Endpoints

All user endpoints are prefixed with `/user`

#### 1. Register User

**Endpoint**: `POST /user/register`

**Description**: Register a new user account

**Request Body**:
```json
{
  "name": "John Doe",
  "username": "johndoe",
  "password": "securepassword123",
  "email": "john@example.com"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com"
}
```

**Status Codes**:
- `201`: User created successfully
- `400`: Username or email already exists

---

#### 2. Login User

**Endpoint**: `POST /user/login`

**Description**: Authenticate user and receive JWT token

**Request Body**:
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOjEsImV4cCI6MTcyMzIzNzYzNn0.xxxxx"
}
```

**Status Codes**:
- `200`: Login successful
- `401`: Invalid username or password

---

#### 3. Check Authentication Status

**Endpoint**: `GET /user/is_auth`

**Description**: Verify if the token is valid and retrieve current user information

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com"
}
```

**Status Codes**:
- `200`: User is authenticated
- `401`: Invalid or expired token

---

#### 4. Get All Users

**Endpoint**: `GET /user/all_users`

**Description**: Retrieve all registered users

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "username": "janesmith",
    "email": "jane@example.com"
  }
]
```

**Status Code**: `200`

---

#### 5. Get Single User Details

**Endpoint**: `GET /user/one_user/{user_id}`

**Description**: Retrieve details of a specific user by ID

**Path Parameters**:
- `user_id` (integer): The ID of the user

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com"
}
```

**Status Codes**:
- `200`: User found
- `404`: User not found

---

#### 6. Delete User

**Endpoint**: `DELETE /user/delete/{user_id}`

**Description**: Delete a user account and all associated tasks

**Path Parameters**:
- `user_id` (integer): The ID of the user to delete

**Response**: No content

**Status Codes**:
- `204`: User deleted successfully
- `404`: User not found

---

### Task Endpoints

All task endpoints are prefixed with `/tasks` and require authentication

#### 1. Create Task

**Endpoint**: `POST /tasks/create`

**Description**: Create a new task for the authenticated user

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body**:
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API documentation",
  "is_completed": false
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API documentation",
  "is_completed": false,
  "user_id": 1
}
```

**Status Codes**:
- `201`: Task created successfully
- `401`: Unauthorized (token invalid/missing)

---

#### 2. Get All Tasks

**Endpoint**: `GET /tasks/all_tasks`

**Description**: Retrieve all tasks for the authenticated user (only user's own tasks)

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API documentation",
    "is_completed": false,
    "user_id": 1
  },
  {
    "id": 2,
    "title": "Deploy application",
    "description": "Deploy to production server",
    "is_completed": false,
    "user_id": 1
  }
]
```

**Status Codes**:
- `200`: Tasks retrieved successfully
- `401`: Unauthorized

---

#### 3. Get Single Task

**Endpoint**: `GET /tasks/one_task/{task_id}`

**Description**: Retrieve a specific task by ID

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `task_id` (integer): The ID of the task

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API documentation",
  "is_completed": false,
  "user_id": 1
}
```

**Status Codes**:
- `200`: Task found
- `401`: Unauthorized
- `404`: Task not found

---

#### 4. Update Task

**Endpoint**: `PUT /tasks/update_task/{task_id}`

**Description**: Update a specific task (only task owner can update)

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `task_id` (integer): The ID of the task to update

**Request Body**:
```json
{
  "title": "Complete project documentation",
  "description": "Updated description",
  "is_completed": true
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Updated description",
  "is_completed": true,
  "user_id": 1
}
```

**Status Codes**:
- `201`: Task updated successfully
- `401`: Unauthorized
- `404`: Task not found or user not authorized to update

---

#### 5. Delete Task

**Endpoint**: `DELETE /tasks/delete/{task_id}`

**Description**: Delete a specific task (only task owner can delete)

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `task_id` (integer): The ID of the task to delete

**Response**: No content

**Status Codes**:
- `204`: Task deleted successfully
- `401`: Unauthorized
- `404`: Task not found or user not authorized to delete

---

## 🔐 Authentication

### JWT Token Flow

1. **Registration**: User registers with username, password, email
2. **Login**: User provides credentials and receives JWT token
3. **Access**: User includes token in `Authorization` header for protected endpoints
4. **Validation**: Token is validated on each request to protected endpoints

### Token Structure

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Content

The JWT payload contains:
```json
{
  "_id": 1,
  "exp": 1723237636
}
```

- `_id`: User's unique identifier in database
- `exp`: Expiration timestamp (based on EXP_TIME setting)

### Key Security Features

- **Password Hashing**: Passwords are hashed using `pwdlib` recommended settings
- **Token Expiration**: Tokens expire after configured time (default: 30 minutes)
- **Authorization Checks**: Users can only access/modify their own tasks
- **Input Validation**: Pydantic validates all requests

## 🗂️ Database Schema

### Users Table (`user_table`)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `name` | String | - | User's full name |
| `username` | String | NOT NULL, Unique | Login username |
| `hash_password` | String | NOT NULL | Hashed password |
| `email` | String | Unique | User's email address |

### Tasks Table (`user_tasks`)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique task identifier |
| `title` | String | - | Task title |
| `description` | String | - | Detailed task description |
| `is_completed` | Boolean | Default: False | Task completion status |
| `user_id` | Integer | Foreign Key → `user_table.id` | Owner of the task |

### Relationships

- **One-to-Many**: One user can have many tasks
- **Cascade Delete**: Deleting a user deletes all associated tasks

## ⚠️ Error Handling

### HTTP Status Codes Used

| Code | Meaning | Common Causes |
|------|---------|---------------|
| `200` | OK | Successful GET request |
| `201` | Created | Successful POST/PUT request |
| `204` | No Content | Successful DELETE request |
| `400` | Bad Request | Duplicate username/email, invalid input |
| `401` | Unauthorized | Missing/invalid token, authentication failure |
| `404` | Not Found | Resource doesn't exist |
| `500` | Server Error | Internal server error |

### Example Error Response

```json
{
  "detail": "Username already exists..."
}
```

## 🔧 Development

### Running with Hot Reload

```bash
uvicorn main:app --reload
```

### Debugging

Enable debug logging by uncommenting `print()` statements in:
- `src/tasks/controller.py`
- `src/user/controller.py`
- `src/utils/helpers.py`

### Testing with Postman

1. Go to `http://localhost:8000/docs` (Swagger UI)
2. Or use Postman to test endpoints
3. For protected endpoints, add header:
   ```
   Authorization: Bearer <token_from_login>
   ```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Migration description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## 📦 Dependencies

Key dependencies:
- `fastapi` - Web framework
- `sqlalchemy` - ORM
- `psycopg2-binary` - PostgreSQL driver
- `pydantic` - Data validation
- `pyjwt` - JWT token handling
- `pwdlib` - Password hashing
- `alembic` - Database migrations
- `python-dotenv` - Environment variable management

For complete list, see [requirements.txt](requirements.txt)

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/feature-name`)
2. Commit your changes (`git commit -m 'Add feature'`)
3. Push to the branch (`git push origin feature/feature-name`)
4. Open a Pull Request

## 📜 License

This project is licensed under the MIT License.

## 📧 Support

For issues and questions, please create an issue in the repository.

---

**Last Updated**: March 2026
