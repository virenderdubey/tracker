
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User, Team

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'avatar', 'aboutme', 'mobile')

class UserForm(forms.ModelForm):
    ui_fields = ['id', 'username', 'email', 'is_superuser']
    link = "username"

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_superuser', 'mobile', 'avatar', 'aboutme')

class TeamForm(forms.ModelForm):
    ui_fields = ['id', 'name']
    link = "name"

    class Meta:
        model = Team
        exclude = ('created_at', 'modified_at', 'created_by', 'modified_by')
