from django.urls import path
from .views import (
    RegisterView, VerifyEmailView, LoginUserView, LogoutView, ProfileView,
    EditProfileView, ChangePasswordView, ReservationView, HomeView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<int:user_id>/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
]
