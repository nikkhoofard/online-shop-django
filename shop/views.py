from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from shop.models import Product, Category
from cart.forms import QuantityForm


def categories_processor(request):
    categories = Category._default_manager.all()
    return {'categories': categories}


def paginat(request, list_objects):
	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except django.core.paginator.PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj


def home_page(request):
	products = Product.objects.all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	shop = product.shop
	related_products = Product.objects.filter(category=product.category).all()[:5]
	context = {
		'title':product.title,
		'product':product,
	#	'favorites':'favorites',
		'related_products':related_products,
		'shop':shop	
	}
	#if request.user.likes.filter(id=product.id).first():
	#	context['favorites'] = 'remove'
	return render(request, 'product_detail.html', context)


#here is the product detail view add when want to add shoping app
"""
@login_required
def product_detail(request, slug):
	form = QuantityForm()
	product = get_object_or_404(Product, slug=slug)
	related_products = Product.objects.filter(category=product.category).all()[:5]
	context = {
		'title':product.title,
		'product':product,
		'form':form,
		'favorites':'favorites',
		'related_products':related_products
	}
	if request.user.likes.filter(id=product.id).first():
		context['favorites'] = 'remove'
	return render(request, 'product_detail.html', context)
"""

@login_required
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:favorites')


@login_required
def favorites(request):
	products = request.user.likes.all()
	context = {'title':'Favorites', 'products':products}
	return render(request, 'favorites.html', context)


def search(request):
	query = request.GET.get('q', '').strip()
	products = Product.objects.none()
	message = ''
	if query:
		products = Product.objects.filter(
			Q(title__icontains=query) |
			Q(description__icontains=query) |
			Q(brand__icontains=query) |
			Q(manufacturer__icontains=query)
		).distinct()
		if not products.exists():
			message = "محصولی با این مشخصات پیدا نشد."
	else:
		message = "لطفاً عبارت مورد نظر خود را وارد کنید."
	context = {
		'products': paginat(request, products),
		'query': query,
		'message': message,
	}
	return render(request, 'home_page.html', context)




def filter_by_category(request, slug):
    category = Category.objects.filter(slug=slug).first()
    if not category:
        context = {'products': []}
        return render(request, 'home_page.html', context)
    category_ids = get_all_subcategory_ids(category)
    products = Product.objects.filter(category_id__in=category_ids)
    context = {'products': paginat(request, products)}
    return render(request, 'home_page.html', context)



def categories_processor(request):
	main_categories = Category.objects.filter(is_sub=False).all()
	return {'main_categories': main_categories}


def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        products = Product.objects.filter(title__icontains=query)[:10]
        results = list(products.values('id', 'title'))
    return JsonResponse({'results': results})



def get_all_subcategory_ids(category):
    ids = [category.id]
    for sub in category.sub_categories.all():
        ids.extend(get_all_subcategory_ids(sub))
    return ids