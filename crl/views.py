from django.shortcuts import render, get_object_or_404
from .views import ServiceCategory

def category_detail(request, category_id):
    category = get_object_or_404(ServiceCategory, id=category_id)
    return render(request, 'services/category_detail.html', {'category': category})

def request_assistance(request):
    return render(request, 'services/request_assistance.html')