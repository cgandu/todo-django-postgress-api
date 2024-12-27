
# Todo App - Django + Docker + PostgreSQL

A To-Do app built with Django, using Docker and PostgreSQL. Supports JWT-based authentication and provides APIs for basic task management

## Prerequisites


- **Docker**
- **Docker Compose**

## Setup

### env:

Suggested .env file located in root directory (see .example_env)


### Build and start the containers:

```bash
docker-compose up -d --build
```

### Run database migrations:

```bash
docker-compose exec web python manage.py migrate
```

### Collect static files (for production):

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Create a superuser (optional):

```bash
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### User Registration:

- **POST** `/api/register/`
  
  ```bash
  curl -X POST http://localhost:8000/api/register/   -H "Content-Type: application/json"   -d '{"username": "user1", "password": "your_password"}'
  ```

### Get JWT Token:

- **POST** `/api/token/`
  
  ```bash
  curl -X POST http://localhost:8000/api/token/   -H "Content-Type: application/json"   -d '{"username": "user1", "password": "your_password"}'
  ```

### Create a Task:

- **POST** `/api/tasks/` (Requires Bearer Token)

  ```bash
  curl -X POST http://localhost:8000/api/tasks/   -H "Authorization: Bearer <access_token>"   -H "Content-Type: application/json"   -d '{"content": "New Task"}'
  ```

### List Tasks:

- **GET** `/api/tasks/` (Requires Bearer Token)

  ```bash
  curl -X GET http://localhost:8000/api/tasks/   -H "Authorization: Bearer <access_token>"
  ```

### Update Task (partial):

- **PATCH** `/api/tasks/<id>/` (Requires Bearer Token)

  ```bash
  curl -X PATCH http://localhost:8000/api/tasks/1/   -H "Authorization: Bearer <access_token>"   -H "Content-Type: application/json"   -d '{"completed": true}'
  ```

### Delete Task:

- **DELETE** `/api/tasks/<id>/` (Requires Bearer Token)

  ```bash
  curl -X DELETE http://localhost:8000/api/tasks/1/   -H "Authorization: Bearer <access_token>"
  ```

