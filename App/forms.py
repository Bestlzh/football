from django.contrib.auth.forms import UserCreationForm
from django import forms
from App.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(min_length=6, max_length=32)
    # password1 = forms.CharField(min_length=6, max_length=16)
    # password2 = forms.CharField(required=False)
    class Meta(UserCreationForm.Meta):
        model = User
        filter = ('username','email')
