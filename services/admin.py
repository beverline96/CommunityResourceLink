from django.contrib import admin
from .models import ServiceCategory, ServiceProvider, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_verified', 'location', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('name', 'user__username')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'category', 'price', 'availability', 'created_at')
    list_filter = ('category', 'availability', 'created_at')
    search_fields = ('name', 'provider__name')
