from django.urls import path
from .views import UserLoginView, UserProfileUpdateView, UserProfileView, UserRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("profile/update/", UserProfileUpdateView.as_view(), name="user-profile-update")

]