# Django Strava Application Setup

## Live Demo
- Main site: https://strava06.pythonanywhere.com
- Admin interface: https://strava06.pythonanywhere.com/admin

## Local Development Setup

### 1. Clone and Setup Environment
```bash
# Clone repository
git clone https://github.com/pmourey/django-strava.git strava && cd strava

# Create and activate virtual environment
mkvirtualenv myvirtualenv --python=/usr/bin/python3.12

# Update pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations strava && python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### Deployment Notes
- For deployment instructions, see: https://help.pythonanywhere.com/pages/VirtualEnvForWebsites
- Ensure DEBUG=False in production 
- Configure your environment variables 
- Run collectstatic for production deployment
    ```bash
    python manage.py collectstatic
    ```

### Requirements
- Python 3.12+ 
- virtualenvwrapper (https://help.pythonanywhere.com/pages/VirtualEnvForWebsites)
- See requirements.txt for full dependencies

