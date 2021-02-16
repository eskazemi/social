from django.urls import path
from .import views

app_name="account"
urlpatterns=[
    path('login/',views.user_login,name='login'),
    path('Register/',views.RegisterUser,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('dashboard/<int:user_id>/',views.user_dashboard,name='user_dashboard'),
    path('edit_profile/<int:user_id>/',views.edit_profile,name='edit_profile'),
    path('phone_login/',views.phone_login,name='phone_login'),
    path('verify/',views.verify,name='verify'),
    path('follow/',views.follow,name='follow'),
    path('unfollow/',views.unfollow,name='unfollow'),
]