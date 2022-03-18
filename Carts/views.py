from random import choice
from django.shortcuts import redirect, render
from .models import Cart, CartItem
from Products.models import Product
from Account.models import Customer_Address, MyUser
from Order.models import Order, OrderItem
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from Account.forms import UpdateAddressForm




def cart(request):

    if request.user.is_authenticated:
        cart = Cart.objects.get(owner=request.user)
        cart_items = CartItem.objects.filter(cart=cart).order_by('item')
        tax = round(float(cart.subtotal) * 0.15,2)
        after_tax = round(float(cart.subtotal) + tax,2)

        return render(request, 'cart/cart.html', {'items': cart_items, 'cart':cart, 'tax':tax, 'after_tax':after_tax})
    else:
        return redirect('../accounts/login')


def remove_from_cart(request, product_name):

    cart = Cart.objects.get(owner=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        if item.item.prod_name == product_name:
            item.quantity -= 1
            cart.subtotal -= item.item.price
            cart.save()
            if item.quantity == 0:
                item.delete()
                break
            item.total -= item.item.price
            item.save()
            break

    return redirect('cart')


def update_cart(request):
    cart = Cart.objects.get(owner=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart.subtotal = 0.00
    for item in cart_items:
        string = item.item.prod_name+'-quantity'
        item.quantity = request.POST[string]
        if item.quantity == '0':
            print("ZERO")
            item.delete()
            continue
        item.total = round((float(item.quantity) * float(item.item.price)),2)
        cart.subtotal += item.total
        item.save()
    cart.save()
    return redirect('cart')


def empty_cart(request):

    cart = Cart.objects.get(owner=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart.subtotal = 0
    cart.save()

    for item in cart_items:
        item.delete()

    return redirect('cart')


def add_to_cart(request):
    if request.user.is_authenticated:
        #ADD TO CART
        prod_to_add_to_cart = Product.objects.get(prod_name= request.GET.get("prod_name"))
        cart = Cart.objects.get(owner=request.user)
        cart.subtotal += prod_to_add_to_cart.price
        cart.save()
        #Check if already in cart, if so, increment quantity of cart item
        not_in_cart = True
        current_cart_items = CartItem.objects.filter(cart=cart)
        for item in current_cart_items:
            if item.item.prod_name == prod_to_add_to_cart.prod_name:
                item.quantity +=1
                item.total += item.item.price
                item.save()
                not_in_cart = False
                break

        if not_in_cart:
            new_item = CartItem(cart=cart, item=prod_to_add_to_cart, quantity=1, total=prod_to_add_to_cart.price)
            new_item.save()

        return JsonResponse({'message': "Success message"}, status=200)
    return JsonResponse({'message': "Error message"}, status=400)


#STRIPE PAYMENTS / CHECKOUT

def create_checkout_session(request):


    my_domain = "http://127.0.0.1:8000"
    stripe.api_key = ""


    
    cart = Cart.objects.get(owner=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items:
        return HttpResponse("EMPTY CART")


    #Clear old orders that user never completed checkout on - orders are created everytime user goes to checkout
    clear_unfinished_orders(request)
    #Saving new order as customer has gone to checkout - is_complete = false, is_paid = false
    new_order = Order(owner=request.user, subtotal=0.00, total=0.00)
    new_order.save()

    items = []
    for item in cart_items:
        new_order_item = OrderItem(from_order=new_order, product = item.item, quantity = item.quantity)
        new_order_item.save()
        product= product_find_or_create(request, item.item.prod_name)
        #Creating new stripe Product and Price to be passed to stripe session // Can create products on the fly
        newprice = price_find_or_create(request, item, product.id)
        items.append(
            {
                'price': newprice['id'],
                'quantity': item.quantity,
            }
        )

    #calculate tax-included total (15% rate)
    new_order.total = round((float(new_order.subtotal) * 1.15),2)
    new_order.save()

    #get customer information ready for session
    customer = customer_find_and_update_or_create(request)

    #create session
    try:
        checkout_session = stripe.checkout.Session.create(
            customer= customer,
            submit_type='pay',
            billing_address_collection='auto',
            shipping_address_collection={
                'allowed_countries': ['US', 'CA'],
            },
            line_items=items,
            customer_update={
                'name': 'auto',
                'address': 'auto',
                'shipping' :'auto',
            },
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url=my_domain + redirect('cart_success').url,
            cancel_url= my_domain + redirect('cart_cancel').url,
        )
    except Exception as e:
        return HttpResponse(str(e))
    return redirect(checkout_session.url, code=303)


def customer_find_and_update_or_create(request):

    try:
        cust_address = Customer_Address.objects.get(customer=request.user)
    except Customer_Address.DoesNotExist:
        cust_address = Customer_Address(    #INCASE there are no user address details in database
                    customer = request.user,
                    street = "Unknown",
                    city = "Unknown",
                    postcode = "Unknown",
                    country = "Unknown",
                    phone_number = "Unknown",
        )

    all_customers = stripe.Customer.list()
    customer = None
    unique_customer = True
    for cust in all_customers:
        if cust.email == request.user.email:
            #update current customer entry
            customer = stripe.Customer.modify(
                cust.id,
                name = request.user.first_name +" "+ request.user.last_name,
                shipping = {
                'name' : request.user.first_name +" "+ request.user.last_name,
                'address' : {
                    'line1' : cust_address.street,
                    'city': cust_address.city,
                    'postal_code': cust_address.postcode,
                    'country' : cust_address.country,
                    }
                }
            )
            unique_customer = False
            

    if unique_customer:
        customer = stripe.Customer.create(
            name= request.user.first_name +" "+ request.user.last_name,
            email= request.user.email,
            shipping = {
                'name' : request.user.first_name +" "+ request.user.last_name,
                'address' : {
                    'line1' : cust_address.street,
                    'city': cust_address.city,
                    'postal_code': cust_address.postcode,
                    'country' : cust_address.country,
                }
            }
        )

    return customer


def product_find_or_create(request, item_name):

    all_products = stripe.Product.list()
    new_product = True
    product = None

    for prod in all_products:
        if prod.name == item_name:
            product = prod
            new_product = False

    if new_product:
        product = stripe.Product.create(name=item_name)

    return product


def price_find_or_create(request, item, prod_id):



    all_prices = stripe.Price.list()
    new_price = True
    price = None

    for pri in all_prices:
        if pri.product == prod_id and pri.unit_amount == int((float(item.item.price)*1.15)*100):
            price = pri
            new_price = False
            break


    if new_price:
        price = stripe.Price.create(
            unit_amount=int((float(item.item.price)*1.15)*100),
            currency="cad",
            product= prod_id,
        )

    return price


endpoint_secret = 'q'

@csrf_exempt
def my_webhook(request):
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # print(payment_intent) #email of purchaser after confirmation, can use this to record order
        owner = MyUser.objects.get(email=payment_intent.charges.data[0].billing_details.email)
        order = Order.objects.filter(owner = owner).first()
        order.is_paid = True
        order.save()
    # elif event['type'] == 'checkout.session.completed':
    #     payment_intent = event['data']['object']
    #     # print(payment_intent) #email of purchaser after confirmation, can use this to record order
    #     owner = MyUser.objects.get(email=payment_intent.customer_details.email)
    #     order = Order.objects.filter(owner = owner).first()
    #     order.is_complete = True
    #     order.save()
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return JsonResponse({'data':"Success"},status=200)


def cart_success(request):
    #refresh users cart
    cart = Cart.objects.get(owner=request.user)
    cart.delete()
    cart = Cart(owner = request.user, subtotal=0.00)
    cart.save()
    return render(request, 'cart/success.html')


def cart_cancel(request):
    clear_unfinished_orders(request)
    return redirect('cart')


def clear_unfinished_orders(request):
    orders = Order.objects.filter(owner=request.user)

    for order in orders:
        if not order.is_paid:
            order.delete()


def pre_checkout(request):

    form = UpdateAddressForm()
    user_data = None
    try:
        user_data = Customer_Address.objects.get(customer = request.user)
    except Customer_Address.DoesNotExist:
        pass

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
            return redirect('checkout')
        else:
            return render(request, 'cart/pre_checkout.html', {'form' : form, 'data': user_data, 'errors': "All fields are required"})

    
    return render(request, 'cart/pre_checkout.html', {'form' : form, 'data' :user_data})