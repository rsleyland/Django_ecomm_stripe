# django_ecomm_stripe
Django eCommerce store with Stripe payments.


Features: Cart, Orders, Products, Accounts. Products can be added to store via django admin panel. Products can have multiple images. Orders are recorded after checkout request. Cart is linked to user account so will persist if logging into new device.

### Setup
- `git clone git@github.com:rsleyland/django_eccom_stripe.git`
- `cd django_eccom_stripe`
- create virtual env of your choice ex. `virtualenv -p python3 myenv`
- start virtual env ex. `source myenv/bin/activate`
- install dependencies from requirements.txt `pip install -r requirements.txt`
- migrate db models `python manage.py migrate --run-syncdb`
- create admin account `python manage.py createsuperuser`
- Start server `python manage.py runserver`
### Configuration:
- stripe api-keys need to be added in Carts/stripe_test.py, Carts/views.py
