from django import forms
from django_countries.fields import CountryField
from django_countries import Countries
from django_countries.widgets import CountrySelectWidget
from django.core.validators import RegexValidator

class RegistrationForm(forms.Form):

    email = forms.EmailField(label='Email', max_length=120, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    image = forms.ImageField(required=False)


    
    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if len(password) < 8:
            raise forms.ValidationError(
                "password too short - must be at least 8 characters"
            )

        if password != password_confirm:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
            
        return password_confirm

    # def clean_password(self):
    #     password = self.cleaned_data.get("password")
    #     if len(password) < 8:
    #         raise forms.ValidationError(
    #             "password too short - must be at least 8 characters"
    #         )
    #     return password

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         MyUser.objects.get(email=email)
    #         auth = authenticate(self, email=email, password=self.cleaned_data.get['password'])
    #         if auth is None:
    #             raise forms.ValidationError(
    #                 mark_safe("<h5>Email is already registered please <a href='../login'>Login</a></h5> ")
    #             )
    #     except MyUser.DoesNotExist:
    #         pass
    #     return email


class ConfirmationForm(forms.Form):

    code = forms.CharField(max_length=40, required=True)


class UpdateAddressForm(forms.Form):

    class CountriesList(Countries):
        only = [
            'CA', 'US'
            ]


    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)
    email = forms.EmailField(max_length=120)
    street = forms.CharField(max_length=120)
    city  = forms.CharField(max_length=40)
    postcode = forms.CharField(max_length=7)
    country = CountryField(default='CA', countries = CountriesList).formfield()
    country.widget.attrs.update({"class": "form-control"})
    phone_number = forms.CharField(max_length=12, validators=[RegexValidator(r'^\d{1,10}$')])
