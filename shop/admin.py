from django.contrib import admin
from .models import Product, CarBrand, CarModel, Shop, Category
# Register your models here.


admin.site.register(CarBrand)
admin.site.register(CarModel)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'date_created']
    list_filter = ['date_created']
    search_fields = ['title', 'owner__username']
    list_per_page = 20
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price']
    list_filter = ['price', 'date_created']
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        return super().get_queryset(request).filter(shop__owner=request.user)
