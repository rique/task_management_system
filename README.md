# Task Manager API

This project is a RESTful API for a simple task management system built with Django REST Framework, SQLite, and JWT authentication.

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd task_manager
    ```

2.  **Build and run the Docker containers:**

    ```bash
    docker-compose up --build
    ```

3.  **Access the API:**

    The API will be available at `http://localhost:8000/api/`.

4.  **Create a superuser:**

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5.  **Obtain a JWT token:**

    Send a POST request to `http://localhost:8000/api/token/` with your username and password to obtain an access token.

6.  **Use the API:**

    Include the access token in the `Authorization` header of your API requests (e.g., `Authorization: Bearer <your_token>`).

## Key Implementation Decisions

* **Django REST Framework:** Chosen for its robust API development capabilities and built-in features like serializers and generic views.
* **SQLite:** Used for simplicity and ease of setup in a development environment.
* **JWT Authentication (Simple JWT):** Implemented for secure API authentication.
* **Dockerization:** Used to containerize the application and simplify setup.
* **pytest:** Used for unit testing, ensuring code quality and reliability.
* **drf-yasg:** Used to generate API Documentation.

## API Endpoints

* **`POST /api/token/`:** Obtain a JWT token.
* **`POST /api/token/refresh/`:** Refresh a JWT token.
* **`GET /api/tasks/`:** List tasks (with pagination and filtering).
* **`POST /api/tasks/`:** Create a task.
* **`GET /api/tasks/{id}/`:** Retrieve a task.
* **`PUT/PATCH /api/tasks/{id}/`:** Update a task.
* **`DELETE /api/tasks/{id}/`:** Delete a task.

## Running Tests

```bash
docker-compose exec web pytest
```

