from django.contrib.auth import login
from django.shortcuts import render, redirect
from product.models import Product, Category
from django.db.models import Q

from .forms import SignUpForm

# Create your views here.

def frontpage(request):
    products = Product.objects.all()[0:8]
    return render(request, 'core/frontpage.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            
            return redirect('/')
    else:
        form = SignUpForm()
        
    return render(request, 'core/signup.html', {'form': form})

def login_old(request):
    return render(request, 'core/login.html')

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    active_category = request.GET.get('category', '')
    
    if active_category:
        products = products.filter(category__slug=active_category) # nos quedamos con los productos que tengan relacion donde el objeto categoria
                                                                   # tenga el campo (slug) en activo
        
    query = request.GET.get('query', '')
    
    # Filtrar por nombre sin distinguir entre mayusculas y minusculas (icontains)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query)) # Buscamos por nombre y descripcion
    
    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
    }
    
    return render(request, 'core/shop.html', context)
