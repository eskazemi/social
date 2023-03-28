from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control",
                                          "placeholder": "your password"}))
    password_confirm = forms.CharField(label="confirm_password",
                                       widget=forms.PasswordInput(
                                           attrs={"class": "form-control",
                                                  "placeholder": "your password"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("this email already exists")
        return email

    def clean(self):
        cd = super().clean()
        pass_1 = cd.get("password")
        pass_2 = cd.get("password_confirm")
        if pass_1 and pass_2 and pass_1 != pass_2:
            raise ValidationError("password and password confirm must match")

