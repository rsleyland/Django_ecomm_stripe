from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Product, ProductImage
from Carts.models import CartItem, Cart


def product_detail(request, prod_name):

    try:
        product = Product.objects.get(prod_name=prod_name)
        prod_images = ProductImage.objects.filter(product=product)
        context = {'prod':product, 'images':prod_images}
        return render(request, 'product/product_detail.html', {'item': context})
    except Product.DoesNotExist:
        return HttpResponse("<div style='border: 2px solid blue'>Sorry Product not found</div>")

        

def product_all(request):

    message = add_to_cart(request)

    if message == "no_auth":
        return redirect('login')

    #Display products
    prods = Product.objects.all()
    context = []
    for prod in prods:
        prod_images = ProductImage.objects.filter(product=prod)
        context.append({'prod':prod, 'images':prod_images})
    return render(request, 'product/product_all.html', context={'context': context, 'message':message} )


def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            #ADD TO CART
            prod_to_add_to_cart = Product.objects.get(prod_name= request.POST['product_name'])
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
                cart_item = CartItem(cart=cart, item=prod_to_add_to_cart, quantity=1, total=prod_to_add_to_cart.price)
                cart_item.save()

            return f"Added {prod_to_add_to_cart.prod_name} to Cart"
        return "no_auth"
    return None