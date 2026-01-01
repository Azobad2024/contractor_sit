from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=20)
    email = models.EmailField(_("Email"), blank=True)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(_("Is Read"), default=False)

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"
