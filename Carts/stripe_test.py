import stripe
from Account.models import Customer_Address


my_domain = "http://127.0.0.1:8000"
stripe.api_key = ""

#create customer
stripe.Customer.create(
  name="First Customer",
  email='admin@admin.com',
  shipping = {
      'name' : "First Customer",
      'address' : {
          'line1' : "1181 main st",
          'line2' : 'empty',
          'city': "Montreal",
          'postal_code': "H3L 3D5",
          'country' : "Canada",
      }
  }
)

all_customers = stripe.Customer.list()

for cust in all_customers:
    if cust.email == "admin@admin.com":
        print(cust.shipping.address.line1)


def customer_find_and_update_or_create(request):
    try:
        cust_address = Customer_Address.objects.get(customer=request.user)
    except Customer_Address.DoesNotExist:
        cust_address = None

    all_customers = stripe.Customer.list()
    unique_customer = True
    for cust in all_customers:
        if cust.email == request.user.email:
            #update current customer entry
            cust['shipping'] = {
                'name' : request.user.first_name +" "+ request.user.first_name,
                'address' : {
                    'line1' : cust_address.street,
                    'city': cust_address.city,
                    'postal_code': cust_address.postcode,
                    'country' : cust_address.country,
                }
            }
            unique_customer = False
            

    if unique_customer:
        stripe.Customer.create(
            name= request.user.first_name +" "+ request.user.first_name,
            email= request.user.email,
            shipping = {
                'name' : request.user.first_name +" "+ request.user.first_name,
                'address' : {
                    'line1' : cust_address.street,
                    'city': cust_address.city,
                    'postal_code': cust_address.postcode,
                    'country' : cust_address.country,
                }
            }
        )