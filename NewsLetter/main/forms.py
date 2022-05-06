from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NLUserCreationForm(ModelForm):
    class Meta:
        model = NLUser
        fields = '__all__'
        exclude = ['user', 'favorite_posts', 'posts', 'liked_posts']

