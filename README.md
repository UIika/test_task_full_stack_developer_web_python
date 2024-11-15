# Test Task Full Stack Developer (Web, Python)

## How to run this app:

Clone this repository:

    git clone https://github.com/UIika/test_task_full_stack_developer_web_python
    cd test_task_full_stack_developer_web_python

Create ".env" file and add environment variables to it:
```dotenv
SQLITE_URL='sqlite+aiosqlite:///database.db'

SECRET_KEY = 'secretkey'

FIRST_SUPERUSER_EMAIL='admin@admin.com'
FIRST_SUPERUSER_NAME='admin'
FIRST_SUPERUSER_PASSWORD='admin'
```

Install poetry:

    pip install poetry

Create virtual environment and install project dependencies:

    poetry install

Activate virtual environment:

    poetry shell

Run alembic migrations:

    alembic upgrade head

Run app:

    uvicorn src.main:app --reload
