from django.core import paginator
from django.shortcuts import redirect, render
from .models import Order, Products
from django.core.paginator import Paginator
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


# Home Page View
def index(request):
    product_objects = Products.objects.all()

    #Search Code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    #Paginator Code
    paginator = Paginator(product_objects, 4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)
    return render(request, 'shop/index.html', {'product_objects': product_objects})


#Detail Code
def detail(request, id):
    product_object = Products.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})


#Checkout Code
def checkout(request):
    if request.method == "POST":
        items = request.POST.get('items', "")
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zipcode = request.POST.get('zipcode', "")
        total = request.POST.get('total', "")

        order = Order(items=items, name=name, email=email, address=address, city=city, state=state, zipcode=zipcode, total=total)
        order.save()
    return render(request, 'shop/checkout.html')


#Signin Code
def signin(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.info(request, 'password not matched')
            return redirect('signin')

        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signin')

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('signin')

        else:
            users = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            users.save();
            print('user created')
        

        return redirect('login')
    else:
        return render(request, 'register/signin.html')


#Login Code
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        users = auth.authenticate(username=username, password=password)

        if users is not None:
            auth.login(request, users)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'register/login.html')


#Logout Code
def logout(request):
    auth.logout(request)
    return redirect('/')