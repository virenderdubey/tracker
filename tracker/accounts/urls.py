from django.urls import path
from accounts.views import SignUp, UpdateProfile, ResetPassword

app_name = 'accounts'

urlpatterns = [
        path('signup/', SignUp.as_view(), name='signup'),
        path('update_profile/', UpdateProfile.as_view(), name='update_profile'),
        path('reset_password/', ResetPassword.as_view(), name='reset_password'),
]
