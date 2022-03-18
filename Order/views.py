from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Order, OrderItem

# Create your views here.

def get_order(request, pk=None):

    data = ""
    user = request.user
    if user.username == '':
        print("USER NOT LOGGED IN")
    if pk == None:
        orders = Order.objects.all()
        for order in orders:
            data += f"<br>Owner: {order.owner}, Total Cost: {order.total_cost}<br>"
            items = OrderItem.objects.filter(from_order=order)
            for item in items:
                data += f"Item: {item.product.prod_name}, Price: {item.product.price}<br>"
        return HttpResponse("%s" % data)
    else:
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return HttpResponse("<div style='border: 2px solid blue'>Sorry Order not found</div>")

        data = {}
        data['owner'] = order.owner
        order_items = OrderItem.objects.filter(from_order=order)
        data['items'] = order_items
        return render(request, "order/order_detail.html", context={'data' : data})