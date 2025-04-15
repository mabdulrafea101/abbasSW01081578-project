

# Event Management & Review System

This Django-based web application provides a platform for creating, organizing, and participating in events with a comprehensive review system for event organizers.

## Setup Instructions

Follow these steps to set up and run the project successfully:

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd abbas_fyp/project/web
```

### Step 2: Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
# Create database tables based on models
python manage.py migrate
```

### Step 5: Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin user with manager privileges.

### Step 6: Set Up Badge System

```bash
python manage.py setup_badges
```

This command initializes the badge system by creating the default badge types that users can earn.

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## User Types and Registration

The system supports three user types:
- **Manager**: Administrators who manage the system
- **Teacher**: Can create and organize events
- **Student**: Can participate in events and provide reviews

New user accounts require confirmation by a manager before they can access the system.

## Project Structure

- **Core**: Main Django project configuration
- **User**: User management and authentication
- **Event**: Event creation, management, and participation
- **Review**: Rating and commenting system for events
- **Badge**: Achievement system for user activities
- **Leaderboard**: Rankings based on participation and organization
- **Notification**: User notification system

## Development Workflow

1. Run migrations when changing models:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create new app (if needed):
   ```bash
   python manage.py startapp new_app_name
   ```
   Don't forget to add the new app to INSTALLED_APPS in settings.py.

3. Collect static files for production:
   ```bash
   python manage.py collectstatic
   ```

## Media File Handling

The system supports profile images and other media uploads with size limits configured in settings.py:

```python
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
```

## Security Notes

For production deployment:
1. Change `DEBUG = False` in settings.py
2. Generate a new `SECRET_KEY`
3. Set appropriate `ALLOWED_HOSTS`
4. Configure a production database (PostgreSQL recommended)
5. Set up proper static and media file serving

## License

© 2025, Developer