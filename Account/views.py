from django.shortcuts import redirect, render
from .forms import RegistrationForm, ConfirmationForm, UpdateAddressForm
from .models import MyUser, Customer_Address
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.utils.safestring import mark_safe
from random import randint, choice
from Carts.models import Cart
from Account.models import MyUser
from django.http import JsonResponse
from Order.models import Order, OrderItem


def register(request):
    form = RegistrationForm()
    #POST REQUEST - REGISTRATION ATTEMPT
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                MyUser.objects.get(email=request.POST['email'])
            except MyUser.DoesNotExist:
                #IF USER ACCOUNT DOES NOT EXIST -> CREATE USER ACCOUNT, SAVE and LOGIN
                user = MyUser.objects.create()
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.confirmation_code = generate_confirm_code()
                if 'image' in request.FILES:
                    user.image = request.FILES['image']
                cart = Cart.objects.create(owner=user, subtotal=0.00)
                user.save()
                cart.save()
                auth = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
                login(request, auth)
                
                return render(request, 'account/response_template.html', {'response':'Thank you for registering.'})
            
            # IF USER ACCOUNT ALREADY EXISTED -> LOG USER IN (IF password matches ofc)
            auth = authenticate(request, email=request.POST['email'], password=request.POST['password'])
            if auth is not None:
                login(request, auth)
                return render(request, 'account/response_template.html', {'response':'Email already registered, You have been logged in.'})
            else:
                return render(request, 'account/response_template.html', {'response':mark_safe("Email already registered, Password was incorrect - <a href='../login'>Login</a></h5>")})
        else:
            return render(request, 'registration/register.html', {'form':form, 'errors':form.errors.values()})

    #GET REQUEST -> FORM WILL BE EMPTY
    #DISPLAY ERRORS IF form.isnotvalid
    
    return render(request, 'registration/register.html', {'form':form})


def profile(request):
    user_data = None
    order_data = []
    if request.user.is_authenticated:
        try:
            orders = Order.objects.filter(owner=request.user)
            for order in orders:
                order_items = OrderItem.objects.filter(from_order=order)
                order_data.append({
                    'order': order,
                    'items' : order_items
                })
            user_data = Customer_Address.objects.get(customer = request.user)
            
        except Customer_Address.DoesNotExist:
            pass
    else:
        return redirect('../accounts/login')

    if request.method == 'POST':
        #update request.POST to include disabled user email field
        POST = request.POST.copy()
        POST['email'] = request.user.email
        form = UpdateAddressForm(POST)

        if form.is_valid():
            address = Customer_Address.objects.get_or_create(customer=request.user)[0]
            address.customer = request.user
            address.street = form.cleaned_data['street']
            address.city = form.cleaned_data['city']
            address.postcode = form.cleaned_data['postcode']
            address.country = form.cleaned_data['country']
            address.phone_number = form.cleaned_data['phone_number']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            address.save()
            user_data = Customer_Address.objects.get(customer = request.user)
            return render(request, 'account/user_profile.html', {'form' : form, 'data': user_data, 'order_data':order_data})
        else:
            return render(request, 'account/user_profile.html', {'form' : form, 'data': user_data, 'order_data':order_data, 'errors': "Missing Fields"})
    
    form = UpdateAddressForm()
    return render(request, 'account/user_profile.html', {'form' : form, 'data': user_data, 'order_data':order_data})


def generate_confirm_code():    #ascii 48-57 = 0-9, 65-90 = A-Z,  97-122 = a-z, 
    code = ''
    for _ in range(20):
        code += chr(choice([randint(48,57), randint(65,90), randint(97,122)]))
    return code


def confirm_code(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)

        if form.is_valid():
            if request.POST['code'] == request.user.confirmation_code:
                user = MyUser.objects.get(email=request.user.email)
                user.email_confirmed = True
                user.save()
                return render(request, 'account/response_template.html', {'response':"User account confirmed"})
            

    form = ConfirmationForm()
    return render(request, 'registration/confirm_email.html', {'form':form})


def delete_acc(request):

    if request.user.is_authenticated:

        account = MyUser.objects.get(email = request.user.email)
        account.delete()

    return redirect('register')

def update_email(request):
    email = request.POST.get("email")
    passw = request.POST.get("pass")

    auth = authenticate(request, email=request.user.email, password=passw)
    if auth is not None:
        user = MyUser.objects.get(email=request.user.email)
        user.email = email
        user.save()
        return JsonResponse({'message': 'success'}, status=200)
    return JsonResponse({'message': 'failed'}, status=400)


def update_password(request):
    passw = request.POST.get("pass")
    passw_new = request.POST.get("pass_new")
    passw_new_confirm = request.POST.get("pass_new_confirm")


    if passw_new != passw_new_confirm:
        return JsonResponse({'message': "not match"}, status=400)
    elif len(passw_new) < 8:
        return JsonResponse({'message': "too short"}, status=400)


    auth = authenticate(request, email=request.user.email, password=passw)
    if auth is not None:
        user = MyUser.objects.get(email=request.user.email)
        user.set_password(passw_new)
        user.save()
        auth = authenticate(request, email=request.user.email, password=passw_new)
        login(request, auth)
        return JsonResponse({'message': 'success'}, status=200)
    return JsonResponse({'message': 'failed'}, status=400)