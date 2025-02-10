# Task Manager

## Description
Task Manager is a web application for managing projects and tasks. Users can create projects, add tasks to them, update task statuses, and manage deadlines.

## Requirements
- Python 3.10+
- Django 5.1
- PostgreSQL (via Docker)
- Docker and Docker Compose

## Installation and Running Locally

### 1. Clone the Repository
Clone the project repository to your local machine:
```bash
git clone https://github.com/ALuiell/TaskManager.git
cd task-manager
```

### 2. Install Dependencies
Create a virtual environment and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

### 3. Configure the Database
Create a `.env` file based on `.env.example` and specify your database settings:
```env
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 4. Apply Migrations
Run migrations to set up the database:
```bash
python manage.py migrate
```

### 5. Run the Project
Start the development server:
```bash
python manage.py runserver
```

Visit in your browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 6. Run with Docker (Optional)
If Docker is installed, you can run the project using Docker Compose:
1. Open the `settings.py` file.
2. Comment out the local SQLite database configuration.
3. Uncomment the PostgreSQL database configuration for Docker.
4. Then, run the following command:
```bash
docker-compose up --build
```

## Testing
Run the test suite:
```bash
python manage.py test
```

## Features
- Project Management:
  - Create, update, and delete projects.
- Task Management:
  - Add tasks to projects.
  - Update task status, priority, and deadlines.
  - Delete tasks.
- Authentication:
  - User registration and authentication via `django-allauth`.

## Technologies
- **Backend**: Django 5.1
- **Frontend**: Bootstrap 5, HTMX
- **Database**: PostgreSQL (SQLite locally)
- **Tools**: Docker, Docker Compose
