from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # optional but useful for URLs

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
