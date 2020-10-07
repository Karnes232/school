from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User



class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')