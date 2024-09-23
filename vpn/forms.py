from django import forms
from django.contrib.auth.forms import UserCreationForm

from vpn.models import User, Site


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "password1",
            "password2",
        ]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "age"]


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["url", "title"]
