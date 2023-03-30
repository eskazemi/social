from .views import (
    HomeView,
    PostDetailView,
)
from django.urls import path


app_name = "home"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/<int:post_id>/<slug:post_slug>/', PostDetailView.as_view(), name="detail")
]
