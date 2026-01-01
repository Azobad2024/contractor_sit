from django import forms
from .models import ContactMessage
from django.utils.translation import gettext_lazy as _

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:ring-2 focus:ring-cyan-500 outline-none transition', 'placeholder': _('الاسم الكامل')}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:ring-2 focus:ring-cyan-500 outline-none transition', 'placeholder': _('البريد الإلكتروني')}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:ring-2 focus:ring-cyan-500 outline-none transition', 'placeholder': _('رقم الهاتف')}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:ring-2 focus:ring-cyan-500 outline-none transition', 'placeholder': _('اكتب رسالتك هنا...'), 'rows': 4}),
        }
