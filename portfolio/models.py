from django.db import models
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    location = models.CharField(_("Location"), max_length=200, blank=True)
    completion_date = models.DateField(_("Completion Date"), blank=True, null=True)
    is_featured = models.BooleanField(_("Featured"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, verbose_name=_("Project"), related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to='projects/')
    is_cover = models.BooleanField(_("Is Cover"), default=False)
    
    class Meta:
        verbose_name = _("Project Image")
        verbose_name_plural = _("Project Images")

    def __str__(self):
        return f"{self.project.title} Image"
