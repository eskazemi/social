from django.urls import path
from .views import RegisterView

app_name = "account"
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register")
]
