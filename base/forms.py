# base/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Example subclass (optional) — removes help_texts and lowercases username on save if you want
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        return self.cleaned_data['username'].lower()
