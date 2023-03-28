from django.urls import path
from .views import (
    RegisterView,
    UserLoginView,
    UserLogoutView
)

app_name = "account"
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout")
]
