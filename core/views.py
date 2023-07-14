from django.shortcuts import redirect, render, HttpResponse
from core.models import item, UserCreation
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from core.Banking_System import Bank, Transaction

def index(request):
    items = item.objects.all()
    for i in items:
        if not str(i.image).startswith('media'):
            image = f"media/{i.image}"
        else:
            image = i.image

    context = {"task": "Home-Page", "items": items, "image": image }
    return render(request, 'core/index.html', context)    

def base(request):
    return render(request, 'base/base.html')


def items(request, id):
    display_item = item.objects.filter(iid=id).first()
    return render(request, 'core/items.html', {'item': display_item})
    
@login_required
def payment(request, id):
    shopkeeper = Bank('Shopkeeper', '09/10/2014')
    try:
        username = request.user.username
        user_creation = UserCreation.objects.get(username=username)
        dob = str(user_creation.dob)
        new_dob = '/'.join(dob.split('-')[::-1])
        data = (username, new_dob, id)
        user = Bank(username, new_dob)
        itemp = item.objects.filter(iid=id).first()
        price = itemp.price
        trans = Transaction(user, shopkeeper, price)
        trans.transfer(u=True)
        return HttpResponse(f'Done {data}')
    except UserCreation.DoesNotExist:
        # Handle the case when the UserCreation object does not exist
        return HttpResponse('UserCreation object does not exist')
    
def signup(request):
    if request.method == "POST":
        data = request.POST
        user = UserCreation(username=data.get('name'), email=data.get('email'), password=data.get('password'), dob=data.get('dob'))
        user.save()
        id = user.create()
        return redirect('/login')
    
    return render(request, 'core/signup.html')

def logins(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')    
            else:
                return render(request, 'core/login.html')
        
        return render(request, 'core/login.html')
    else:
        return redirect('/')


def logouted(request):
    logout(request)
    return redirect('/')