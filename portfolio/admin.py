from django.contrib import admin
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'completion_date', 'is_featured')
    list_filter = ('is_featured', 'completion_date')
    search_fields = ('title', 'description', 'location')
    inlines = [ProjectImageInline]
