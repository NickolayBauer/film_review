from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from main.models import User, Comment

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'autofocus': True}), label='Email')


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'nick', 'description')

class CommentForm(forms.ModelForm):

    class Meta:
        model  = Comment
        fields = ('title', 'content')
