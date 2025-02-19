from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=200,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    admins = models.ManyToManyField(User, on_delete=models.CASCADE, related_name='Admins')

    def __str__(self):
        return self.title


class Category(models.Model):

    title = models.CharField(max_length=200, unique=True,db_collation='utf8_persian_ci')
    slug = models.SlugField(max_length=200, unique=True,allow_unicode=True,db_collation='utf8_persian_ci',default='default-slug')

    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs): # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop')
    image = models.ImageField(upload_to='products')
    #title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    #slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=200, unique=True,db_collation='utf8_persian_ci')
    slug = models.SlugField(max_length=200, unique=True,allow_unicode=True,db_collation='utf8_persian_ci',default='default-slug')
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)