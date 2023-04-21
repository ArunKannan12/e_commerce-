from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
class CustomUserForm(UserCreationForm):
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter user name'}))
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'enter E-mail'}))
    password1=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter password'}))
    password2=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Re-enter password'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email 