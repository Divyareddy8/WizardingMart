from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class SignUpForm(ModelForm):
    class Meta:
        model = User
        field = ['name', 'username', 'email', 'password']

class createProduct(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

