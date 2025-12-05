from django.shortcuts import render, get_object_or_404, redirect

# import the models from the services app
from services.models import ServiceProvider, ServiceCategory, Service
from django.core.paginator import Paginator


def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def services(request):
    # Query available services and include related provider and category to avoid extra queries
    qs = Service.objects.select_related('provider', 'category').filter(availability=True)

    # Search
    q = request.GET.get('q')
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(description__icontains=q) | qs.filter(provider__name__icontains=q)

    # Category filter
    category_id = request.GET.get('category')
    category = None
    if category_id:
        try:
            category = ServiceCategory.objects.get(id=category_id)
            qs = qs.filter(category=category)
        except ServiceCategory.DoesNotExist:
            category = None

    # Pagination (10 per page)
    paginator = Paginator(qs.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = ServiceCategory.objects.all()

    return render(request, 'services/services.html', {
        'services': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'q': q,
        'categories': categories,
        'selected_category': category,
    })





def my_requests(request):
    return render(request, 'core/my_requests.html')


def services_by_category(request, category_id):
    # Try to get the category; if it doesn't exist, redirect to the services list
    try:
        category = ServiceCategory.objects.get(id=category_id)
    except ServiceCategory.DoesNotExist:
        return redirect('services:index')

    # Find providers who have at least one Service in this category and are verified.
    providers = ServiceProvider.objects.filter(service__category=category, is_verified=True).distinct()

    return render(request, 'services/services_by_category.html', {
        'category': category,
        'providers': providers
    })
