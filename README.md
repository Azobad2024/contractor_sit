# Contractor Portfolio Website

A production-ready, mobile-first Django website for a contractor, featuring a services showcase, project portfolio with image sliders, and contact form. Supports RTL (Arabic) and Dark Mode out of the box.

## Features
- **Responsive Design**: Built with Tailwind CSS (CDN for Development).
- **RTL Support**: Fully localized for Arabic users.
- **Project Portfolio**: Dynamic gallery with modal and swipeable image slider.
- **Admin Panel**: Manage Services, Projects, and view Contact Messages.
- **API**: Read-only REST API for Services and Projects.
- **Security**: Basic protection against spam and secure admin configuration.

## Setup Instructions

1. **Activate Environment**:
   ```bash
   ..\Scripts\activate
   ```

2. **Navigate to Project**:
   ```bash
   cd contractor_site
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Load Sample Data**:
   ```bash
   python manage.py seed_data
   # OR
   python manage.py loaddata fixtures/seed.json
   ```

6. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
- **Services**: `GET /api/services/`
- **Projects**: `GET /api/projects/`

## Admin Panel
Access the admin panel at `/admin/` to add projects and services.

## Deployment Guide

### Prerequisites
- Python 3.10+
- PostgreSQL
- Nginx & Gunicorn

### Steps
1. **Environment Variables**: creating a `.env` file with `DEBUG=False` and your `DATABASE_URL`.
2. **Collect Static**:
   ```bash
   python manage.py collectstatic
   ```
3. **Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn contractor_site.wsgi:application --bind 0.0.0.0:8000
   ```
4. **Nginx**:
   Configure Nginx to proxy pass to port 8000 and serve static/media files.

