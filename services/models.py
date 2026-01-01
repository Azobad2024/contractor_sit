from django.db import models
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    icon = models.ImageField(_("Icon"), upload_to='services/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


    def __str__(self):
        return self.title

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, verbose_name=_("Service"), related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to='services/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Service Image")
        verbose_name_plural = _("Service Images")

    def __str__(self):
        return f"{self.service.title} Image"
