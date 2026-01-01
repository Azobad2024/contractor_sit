from django.core.management.base import BaseCommand
from services.models import Service
from portfolio.models import Project, ProjectImage
from django.core.files.base import ContentFile
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Services
        services_data = [
            ('ديكورات داخلية', 'تصميم وتنفيذ أحدث الديكورات الداخلية للمنازل والفلل.'),
            ('أصباغ حديثة', 'تنفيذ أرقى أنواع الدهانات بألوان عصرية وجودة عالية.'),
            ('ترميم وصيانة', 'خدمات ترميم المباني وصيانتها بشكل شامل.'),
        ]
        
        for title, desc in services_data:
            Service.objects.get_or_create(title=title, defaults={'description': desc})
            
        # Projects
        projects_data = [
            ('فيلا حي النرجس', 'تشطيب كامل لفيلا سكنية فاخرة.', 'الرياض'),
            ('مجلس خارجي مودرن', 'تصميم وتنفيذ ملحق خارجي بتصميم عصري.', 'جدة'),
            ('ترميم شقة سكنية', 'تجديد كامل لشقة قديمة وتحويلها لتحفة فنية.', 'الدمام'),
        ]
        
        for title, desc, loc in projects_data:
            p, created = Project.objects.get_or_create(
                title=title, 
                defaults={
                    'description': desc,
                    'location': loc,
                    'is_featured': True
                }
            )
            # Add a placeholder image if created
            if created:
                ProjectImage.objects.create(project=p, is_cover=True, image='projects/sample.jpg')

        self.stdout.write(self.style.SUCCESS('Successfully seeded data.'))
