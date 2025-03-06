from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

"""
adrees
phone number 
location gis
نمایندگی کجاها دارد
description
"""

class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=200,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    description = models.TextField()
    phone_number = models.CharField(max_length=20)
    admins = models.ManyToManyField(User, related_name='Admins')

class Category(models.Model):
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs): # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

"""
for which car
brand 
company name
price date 
garanty darad ya na
چند ماه گارانتی دارد 
"""

class CarBrand(models.Model):
    """Car manufacturers like Toyota, Honda, BMW, etc."""
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    """Specific car models like Corolla, Civic, 3-Series, etc."""
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=100)
    year_start = models.PositiveIntegerField(null=True, blank=True)  # Optional start year
    year_end = models.PositiveIntegerField(null=True, blank=True)    # Optional end year
    
    class Meta:
        unique_together = ('brand', 'name')
        
    def __str__(self):
        return f"{self.brand} {self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop')
    image = models.ImageField(upload_to='products')
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    compatible_cars = models.ManyToManyField(CarModel, related_name='compatible_products')
    brand = models.CharField(max_length=100, help_text="Brand of the product")
    manufacturer = models.CharField(max_length=100, help_text="Company that manufactured the product")
    price_valid_until = models.DateField(null=True, blank=True)
    has_warranty = models.BooleanField(default=False)
    warranty_months = models.PositiveIntegerField(default=0, help_text="Number of months of warranty")
    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)