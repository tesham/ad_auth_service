## Django REST API for User Authentication with PostgreSQL
This project implements a RESTful API using Django and Django REST Framework (DRF) for user authentication with PostgreSQL as the database backend.
JWT token based authentication is used.
The API includes user registration, token generation, access token generation from refresh token and logout functionalities.

## Features

- User registration with email verification
- User login with JWT authentication
- Token-based authentication using Django REST Framework JWT
- PostgreSQL as the database backend

### Prerequisites

- Python 3.9
- PostgreSQL
- Django 4.1.0
- Django REST Framework 3.14

### Installation

1. clone the repository from develop branch

2. Create and activate a virtual environment if it doesn't exist in the project folder:
```
    python -m venv venv
    source venv/bin/activate
```

3. Install all the requirements using `pip`:
```
    pip install -r requirements.txt
```

4. Add database connection information in main `settings.py` 
```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
```

5. Apply migrations from terminal
```
    python manage.py makemigrations
    python manage.py migrate
```

6. Create a superuser (admin)
```
    python manage.py createsuperuser
```
    
7. Start the server:
```
    python manage.py runserver
```


### Configuration

Update the `settings.py` file with your configurations. Ensure you have the `SECRET_KEY`, `JWT_SECRET_KEY` and other necessary configurations set.

### Usage

#### Endpoints

- **User Registration:**
-  Only superuser has access to create user

    ```http
    POST /api/register/
    ```

    Request body:
    ```json
    {
        "username": "yourusername",
        "password": "yourpassword",
        "email": "youremail@example.com"
    }
    ```
  
    Response:
    ```json
    {
      "is_error": 0,
      "message": "success"
    }
    ```

- **User Login:**

    ```http
    POST /api/auth/token/
    ```

    Request body:
    ```json
    {
        "username": "yourusername",
        "password": "yourpassword"
    }
    ```

    Response:
    ```json
    {
        "access_token": "youraccesstoken",
        "refresh_token": "yourrefreshtoken"
    }
    ```

- **Refresh Token:**

    ```http
    POST /api/auth/token/refresh/
    ```

    Request body:
    ```json
    {
        "refresh_token": "yourrefreshtoken"
    }
    ```

    Response:
    ```json
    {
        "access_token": "newaccesstoken"
    }
    ```

- **Logout (Blacklist Refresh Token):**

    ```http
    POST /api/auth/logout/
    ```

    Request body:
    ```json
    {
        "refresh_token": "yourrefreshtoken"
    }
    ```

    Response:
    ```json
    {
        "message": "Successfully logged out."
    }
    ```