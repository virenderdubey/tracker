
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'avatar', 'aboutme', 'mobile')
