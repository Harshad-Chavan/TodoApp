# TodoApp

A FastAPI-based Todo application with user authentication, task management, and a simple web UI.

## Prerequisites

- Python 3.9+
- pip
- Git
- PostgreSQL (recommended) or SQLite for a quick local setup

## Run the project locally

### 1. Clone the repository

```bash
git clone https://github.com/Harshad-Chavan/TodoApp.git
cd TodoApp
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set up the database

This project is currently configured to use PostgreSQL by default in `database.py`.

Create a local PostgreSQL database named `TodoApplication` and make sure the connection string matches your local setup:

```python
POSTGRES_URL = "postgresql://postgres:postgres123#$@localhost:5432/TodoApplication"
```

If you want the fastest local setup, you can change `USE_DB` to `"sqlite"` in `database.py` and keep the default SQLite database file (`todos.db`).

### 5. Start the app

Run the app with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or run the file directly:

```bash
python main.py
```

### 6. Open the app

Visit:

```text
http://localhost:8000
```

The app redirects `/` to `/todos`.

### 7. API docs

Swagger UI is available at:

```text
http://localhost:8000/docs
```

## Optional: Run with Docker

Build the image:

```bash
docker build -t todoapp .
```

Run the container:

```bash
docker run -p 8000:8000 todoapp
```

You can also use Docker Compose if needed:

```bash
docker-compose up --build
```

## Notes

- The app uses SQLAlchemy and FastAPI.
- If you change the database type in `database.py`, make sure the tables are created automatically by `models.Base.metadata.create_all(bind=engine)` in `main.py`.
- If you run into database connection issues, confirm PostgreSQL is running locally and the database credentials match the values in `database.py`.

