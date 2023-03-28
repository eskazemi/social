from django.shortcuts import (
    render,
    redirect,
)
from django.views import View
from .form import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages


class RegisterView(View):
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'account/register.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd["username"],
                                     email=cd["email"],
                                     password=cd["password"])
            messages.success(request, "you registered successfully", 'success')
            return redirect('home:home')
        return render(request, 'account/register.html', {"form": form})
