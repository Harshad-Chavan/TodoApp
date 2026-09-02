# TodoApp

A FastAPI-based Todo application with user authentication, task management, and a simple web UI.

## Prerequisites

- Python 3.9+
- uv (recommended)
- PostgreSQL (recommended) or SQLite for a quick local setup

## Run the project locally

### 1. Clone the repository

```bash
git clone https://github.com/Harshad-Chavan/TodoApp.git
cd TodoApp
```

### 2. Install uv

If you do not already have uv installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies

This project now uses uv-managed dependencies from `pyproject.toml`.

```bash
uv sync
```

To activate the environment manually:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Set up the database

This project is currently configured to use PostgreSQL by default in `database.py`.

Create a local PostgreSQL database named `TodoApplication` and make sure the connection string matches your local setup:

```python
POSTGRES_URL = "postgresql://postgres:postgres123#$@localhost:5432/TodoApplication"
```

If you want the quickest local setup, switch `USE_DB` to `"sqlite"` in `database.py` and use the built-in SQLite database file (`todos.db`).

### 5. Start the app

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or run the file directly:

```bash
uv run python main.py
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

You can also use Docker Compose:

```bash
docker-compose up --build
```

## Notes

- Dependency management is handled via `pyproject.toml` and `uv`.
- `requirements.txt` is not required for uv-based local development, though it may still exist for compatibility.
- If you change the database type in `database.py`, make sure the tables are created automatically by `models.Base.metadata.create_all(bind=engine)` in `main.py`.
