from django.urls import path, re_path

from shop import views

app_name = "shop"

urlpatterns = [
	path('', views.home_page, name='home_page'),
	#path('<slug:slug>', views.product_detail, name='product_detail'),
    re_path(r'v/(?P<slug>[^/]+)/?$', views.product_detail, name='product_detail'),
	path('add/favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
	path('remove/favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
	path('favorites/', views.favorites, name='favorites'),
	path('search/', views.search, name='search'),
    re_path(r'filter/(?P<slug>[^/]+)/?$',  views.filter_by_category, name='filter_by_category'),
	#path('filter/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
]


