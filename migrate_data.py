"""
Script to migrate data from SQLite to PostgreSQL
Run this with: python migrate_data.py
"""
import os
import django

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contractor_site.settings')
os.environ['USE_SQLITE'] = 'True'
django.setup()

# Import models
from services.models import Service, ServiceImage
from portfolio.models import Project, ProjectImage
from contact.models import ContactMessage
from django.contrib.auth.models import User

# Export data from SQLite
print("📤 Exporting data from SQLite...")

services_data = []
for service in Service.objects.all():
    service_dict = {
        'id': service.id,
        'title': service.title,
        'description': service.description,
        'icon': service.icon.name if service.icon else None,
        'created_at': service.created_at
    }
    images = []
    for img in service.images.all():
        images.append(img.image.name)
    service_dict['images'] = images
    services_data.append(service_dict)
    print(f"  ✓ Service: {service.title}")

projects_data = []
for project in Project.objects.all():
    project_dict = {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'location': project.location,
        'completion_date': project.completion_date,
        'is_featured': project.is_featured,
        'created_at': project.created_at
    }
    images = []
    for img in project.images.all():
        images.append(img.image.name)
    project_dict['images'] = images
    projects_data.append(project_dict)
    print(f"  ✓ Project: {project.title}")

contacts_data = []
for contact in ContactMessage.objects.all():
    contacts_data.append({
        'name': contact.name,
        'email': contact.email,
        'phone': contact.phone,
        'message': contact.message,
        'created_at': contact.created_at
    })
    print(f"  ✓ Contact: {contact.name}")

users_data = []
for user in User.objects.all():
    users_data.append({
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined,
        'password': user.password,
    })
    print(f"  ✓ User: {user.username}")

print(f"\n✅ Exported: {len(services_data)} services, {len(projects_data)} projects, {len(contacts_data)} contacts, {len(users_data)} users\n")

# Switch to PostgreSQL
print("🔄 Switching to PostgreSQL...")
os.environ['USE_SQLITE'] = 'False'

# Reload Django settings
from importlib import reload
from django.conf import settings
reload(django.apps.registry)
django.setup()

# Re-import models for PostgreSQL
from services.models import Service, ServiceImage
from portfolio.models import Project, ProjectImage
from contact.models import ContactMessage
from django.contrib.auth.models import User

print("📥 Importing data to PostgreSQL...")

# Import Services
for service_dict in services_data:
    images = service_dict.pop('images')
    service, created = Service.objects.update_or_create(
        id=service_dict['id'],
        defaults=service_dict
    )
    for img_name in images:
        if img_name:
            ServiceImage.objects.get_or_create(
                service=service,
                image=img_name
            )
    print(f"  ✓ Imported service: {service.title}")

# Import Projects  
for project_dict in projects_data:
    images = project_dict.pop('images')
    project, created = Project.objects.update_or_create(
        id=project_dict['id'],
        defaults=project_dict
    )
    for img_name in images:
        if img_name:
            ProjectImage.objects.get_or_create(
                project=project,
                image=img_name
            )
    print(f"  ✓ Imported project: {project.title}")

# Import Contacts
for contact_dict in contacts_data:
    ContactMessage.objects.get_or_create(
        phone=contact_dict['phone'],
        created_at=contact_dict['created_at'],
        defaults=contact_dict
    )
    print(f"  ✓ Imported contact: {contact_dict['name']}")

# Import Users
for user_dict in users_data:
    User.objects.get_or_create(
        username=user_dict['username'],
        defaults=user_dict
    )
    print(f"  ✓ Imported user: {user_dict['username']}")

print(f"\n🎉 Migration complete!")
print(f"✅ Services: {Service.objects.count()}")
print(f"✅ Projects: {Project.objects.count()}")
print(f"✅ Contacts: {ContactMessage.objects.count()}")
print(f"✅ Users: {User.objects.count()}")
