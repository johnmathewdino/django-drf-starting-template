# Django-DRF Starting Template

## Description

This repository provides a starting template for projects using Django and Django REST Framework (DRF) with a `dotenv` setup. It includes configurations for multiple databases, media, and static URLs. Additionally, the `.gitignore` file is pre-configured to exclude unnecessary files from version control.

## Features

- **Django & DRF Setup**: A boilerplate setup for Django and Django REST Framework.
- **Dotenv Configuration**: Environment variables management using `python-dotenv`.
- **Multiple Database Configurations**: Template supports multiple database setups.
- **Media and Static URL Configurations**: Basic configurations for handling media and static files.
- **Git Ignore**: `.gitignore` is set up to avoid tracking unnecessary files.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/johnmathewdino/https-github.com-johnmathewdino-Django-DRF-Starting-Template.git
cd django-drf-starting-template
```

### Setup Virtual Environment

1. Create a virtual environment using `venv` or `virtualenv`.
```bash
pyhton -m venv venv
```

2. Activate the virtual environment.
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install the dependencies.
```bash
pip install -r requirements.txt
```

### Setup Environment Variables

1. Rename the `.env.example` file to `.env`.
```bash
mv .env.example .env
```

2. Open the `.env` file and update the environment variables.

```bash
# DATABASE
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# EMAIL
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### Apply Migrations

Run the following commands to set up your database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser

Create a superuser to access the Django admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to create a superuser account.

### Run the Server

```bash
python manage.py runserver
```


## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)