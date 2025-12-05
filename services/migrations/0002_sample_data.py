from django.db import migrations


def create_sample_data(apps, schema_editor):
    ServiceCategory = apps.get_model('services', 'ServiceCategory')
    ServiceProvider = apps.get_model('services', 'ServiceProvider')
    Service = apps.get_model('services', 'Service')
    User = apps.get_model('auth', 'User')

    # Create users for providers
    u1 = User.objects.create_user(username='provider1', email='provider1@example.com', password='password123')
    u2 = User.objects.create_user(username='provider2', email='provider2@example.com', password='password123')
    u3 = User.objects.create_user(username='provider3', email='provider3@example.com', password='password123')

    # Create categories
    c1 = ServiceCategory.objects.create(name='Food', description='Food assistance and delivery')
    c2 = ServiceCategory.objects.create(name='Transport', description='Transport and rides')
    c3 = ServiceCategory.objects.create(name='Health', description='Health and wellness services')

    # Create providers
    p1 = ServiceProvider.objects.create(user=u1, name='Good Eats', contact_info='good-eats@example.com', location='Downtown', is_verified=True)
    p2 = ServiceProvider.objects.create(user=u2, name='Fast Rides', contact_info='fast-rides@example.com', location='Uptown', is_verified=True)
    p3 = ServiceProvider.objects.create(user=u3, name='Wellness Center', contact_info='wellness@example.com', location='Midtown', is_verified=False)

    # Create services
    Service.objects.create(provider=p1, category=c1, name='Meal delivery', description='Deliver meals to home', price=5.00, availability=True)
    Service.objects.create(provider=p1, category=c1, name='Grocery pickup', description='Pickup groceries', price=None, availability=True)
    Service.objects.create(provider=p2, category=c2, name='Local ride', description='Short distance rides', price=10.00, availability=True)
    Service.objects.create(provider=p3, category=c3, name='Counseling session', description='1-hour counseling', price=30.00, availability=True)


def remove_sample_data(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    ServiceProvider = apps.get_model('services', 'ServiceProvider')
    ServiceCategory = apps.get_model('services', 'ServiceCategory')
    User = apps.get_model('auth', 'User')

    Service.objects.filter(name__in=['Meal delivery', 'Grocery pickup', 'Local ride', 'Counseling session']).delete()
    ServiceProvider.objects.filter(name__in=['Good Eats', 'Fast Rides', 'Wellness Center']).delete()
    ServiceCategory.objects.filter(name__in=['Food', 'Transport', 'Health']).delete()
    User.objects.filter(username__in=['provider1', 'provider2', 'provider3']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, remove_sample_data),
    ]
