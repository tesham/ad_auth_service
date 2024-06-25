## Django REST API for User Authentication with PostgreSQL
This project implements a RESTful API using Django and Django REST Framework (DRF) for user authentication with PostgreSQL as the database backend.
JWT token based authentication is used.
The API includes user registration, token generation, access token generation from refresh token and logout functionalities.

## Features

- User registration with email verification
- Token-based authentication using Django REST Framework JWT
- User login with JWT authentication, return access and refresh token
- Can return access token from refresh token
- Act as a RabbitMQ producer. Send auth audit message to consumer[Auth Service]
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
    
    users : storing user info
    -- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

    -- Table Definition
    CREATE TABLE "public"."users" (
        "id" int8 NOT NULL,
        "password" varchar NOT NULL,
        "last_login" timestamptz,
        "is_superuser" bool NOT NULL,
        "username" varchar NOT NULL,
        "first_name" varchar NOT NULL,
        "last_name" varchar NOT NULL,
        "email" varchar NOT NULL,
        "is_staff" bool NOT NULL,
        "is_active" bool NOT NULL,
        "date_joined" timestamptz NOT NULL,
        "name" varchar,
        "contact_number" varchar,
        PRIMARY KEY ("id")
    );
    
    user_sessions : use to store user session after login till logout. Only one session can be active at a time
    -- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

    -- Table Definition
    CREATE TABLE "public"."user_sessions" (
        "id" int8 NOT NULL,
        "login_time" timestamptz NOT NULL,
        "logout_time" timestamptz,
        "refresh_token" varchar NOT NULL,
        "user_id" int8,
        "is_active" bool NOT NULL,
        CONSTRAINT "user_sessions_user_id_43ce9642_fk_users_id" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id"),
        PRIMARY KEY ("id")
    );
      
     blacklisted_tokens: blacklist refresh token so that it can't be used
     -- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

    -- Table Definition
    CREATE TABLE "public"."blacklisted_tokens" (
        "id" int8 NOT NULL,
        "token" varchar NOT NULL,
        "blacklisted_at" timestamptz NOT NULL,
        PRIMARY KEY ("id")
    );
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

