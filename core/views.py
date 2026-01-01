from django.shortcuts import render, redirect
from django.contrib import messages
from services.models import Service
from portfolio.models import Project
from contact.forms import ContactMessageForm

def home(request):
    services = Service.objects.all()[:6]
    projects = Project.objects.filter(is_featured=True)[:6]
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.')
            return redirect('home')
        else:
            messages.error(request, 'حدث خطأ أثناء إرسال الرسالة. يرجى التحقق من البيانات.')
    else:
        form = ContactMessageForm()

    context = {
        'services': services,
        'projects': projects,
        'form': form,
    }
    return render(request, 'home.html', context)
