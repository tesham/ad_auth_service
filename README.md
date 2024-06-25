## Django REST API for User Authentication with PostgreSQL
This project implements a RESTful API using Django and Django REST Framework (DRF) for user authentication with PostgreSQL as the database backend.
JWT token based authentication is used.
The API includes user registration, token generation, access token generation from refresh token and logout functionalities.

## Features

- User registration with email verification
- User login with JWT authentication
- Token-based authentication using Django REST Framework JWT
- Act as RabbitMQ producer. Send auth audit message to consumer
- PostgreSQL as the database backend

### Prerequisites

- Python 3.9
- PostgreSQL
- Django 4.1.0
- Django REST Framework 3.14

### Installation

1. clone the repository

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
    
    models :
    
    users : storing user info like : username, password, etc
    
    user_sessions : use to store user session after login to logout. Only one session can be active at a time
    class UserSession(models.Model):
        user = models.ForeignKey(
            AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='sessions'
        )
        login_time = models.DateTimeField(auto_now_add=True)
        is_active = models.BooleanField(default=True)
        logout_time = models.DateTimeField(null=True, blank=True)
        refresh_token = models.CharField(max_length=500)
      
     blacklisted_tokens: blacklist refresh token so that it can't be used
     class BlacklistedToken(models.Model):
        token = models.CharField(max_length=500, unique=True)
        blacklisted_at = models.DateTimeField(default=timezone.now)
```

6. Put RabbitMQ config in setting.py

```
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'guest'
    RABBITMQ_PASSWORD = 'guest'
```
    
7. Start the server:
```
    python manage.py runserver
```


### Configuration

Update the `settings.py` file with your configurations. Ensure you have the `SECRET_KEY`, `JWT_SECRET_KEY` and other necessary configurations set.

