from django.urls import path
from .views import (
    RegisterView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserResetPasswordView,
    UserPasswordResetDownView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
    UserFollowView,
    UserUnFollowView,
)

app_name = "account"
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name="profile"),
    path('reset/', UserResetPasswordView.as_view(), name="password_reset"),
    path('reset/done/', UserPasswordResetDownView.as_view(),
         name="password_reset_done"),
    path('confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('confirm/complete/', UserPasswordResetCompleteView.as_view(),
         name="password_reset_complate"),
    path('follow/<int:user_id>/', UserFollowView.as_view(),
         name="user_follow"),
    path('unfollow/<int:user_id>/', UserUnFollowView.as_view(),
         name="user_unfollow"),
]
