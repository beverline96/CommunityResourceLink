 
 
 
from django.shortcuts import render, get_object_or_404
from .models import Service


def index(request):
    # Keep a simple index that shows available services when accessed directly
    services = Service.objects.select_related('provider', 'category').filter(availability=True)
    return render(request, 'services/services.html', {'services': services})


def detail(request, pk):
    service = get_object_or_404(Service.objects.select_related('provider', 'category'), pk=pk)
    return render(request, 'services/detail.html', {'service': service})


def request_assistance(request):
    """View for users to request assistance from service providers."""
    service = None
    service_id = request.GET.get('service') or request.POST.get('service_id')
    if service_id:
        try:
            service = Service.objects.select_related('provider').get(pk=service_id)
        except Service.DoesNotExist:
            service = None

    if request.method == 'POST':
        # Basic handling: for now, just pretend we accept the request and show a simple confirmation.
        # In a full implementation we'd validate input, save a Request model or send email.
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # TODO: persist or email this request
        return render(request, 'services/request_assistance.html', {
            'service': service,
            'sent': True,
            'name': name,
        })

    return render(request, 'services/request_assistance.html', {'service': service})
