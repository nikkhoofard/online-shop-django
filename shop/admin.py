from django.contrib import admin
from .models import Product, CarBrand, CarModel, Shop, Category
# Register your models here.
admin.site.register(Product)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(Shop)
admin.site.register(Category)

