# Todo API Documentation

## Base URL
All API endpoints are available under the base URL:
```
https://your-domain.com/api/v1
```

## Authentication
All authenticated endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Rate Limits
- Authentication endpoints (register, login): 5-10 requests per minute
- Task creation: 20 requests per minute
- Task retrieval: 30-50 requests per minute
- Task updates: 15 requests per minute
- Task patch: 20 requests per minute
- Task deletion: 10 requests per minute

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password_123",
  "first_name": "Optional",
  "last_name": "Optional"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "Optional",
    "last_name": "Optional",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

#### POST /auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "Optional",
    "last_name": "Optional",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

#### GET /auth/profile
Get authenticated user profile.

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "first_name": "Optional",
  "last_name": "Optional",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### POST /auth/refresh
Refresh JWT token using the current valid token.

**Response:**
```json
{
  "access_token": "new_jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "Optional",
    "last_name": "Optional",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

### Tasks

#### GET /tasks
Retrieve all tasks for the authenticated user.

**Query Parameters:**
- `completed` (optional): Filter by completion status (true/false)
- `limit` (optional): Number of tasks to return (default: 50, max: 100)
- `offset` (optional): Number of tasks to skip (for pagination)

**Response:**
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Optional description",
      "is_completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "due_date": "2023-12-31T23:59:59Z",
      "priority": "medium",
      "user_id": "user-uuid-string"
    }
  ],
  "total": 25,
  "limit": 50,
  "offset": 0
}
```

#### POST /tasks
Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Optional description",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "medium"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "medium",
  "user_id": "user-uuid-string"
}
```

#### GET /tasks/{task_id}
Retrieve a specific task for the authenticated user.

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "medium",
  "user_id": "user-uuid-string"
}
```

#### PUT /tasks/{task_id}
Update a specific task for the authenticated user.

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "is_completed": true,
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "high"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated description",
  "is_completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "high",
  "user_id": "user-uuid-string"
}
```

#### PATCH /tasks/{task_id}
Partially update a specific task for the authenticated user.

**Request Body:**
```json
{
  "is_completed": true
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "medium",
  "user_id": "user-uuid-string"
}
```

#### DELETE /tasks/{task_id}
Delete a specific task for the authenticated user.

**Response:**
```
Status: 200 OK
{
  "message": "Task deleted successfully"
}
```

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 422: Validation Error
- 429: Too Many Requests
- 500: Internal Server Error