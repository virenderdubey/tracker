from django.urls import path
from accounts.views import SignUpView, UpdateProfileView, ResetPasswordView, LoginView, LogoutView, TeamsView

app_name = 'accounts'

urlpatterns = [
        path('login/', LoginView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('signup/', SignUpView.as_view(), name='signup'),
        path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
        path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
        path('profile/', ResetPasswordView.as_view(), name='profile'),
        path('update_password/', ResetPasswordView.as_view(), name='update_password'),
        path('teams/', TeamsView.as_view(), name='teams'),
]
