from django.urls import path
from accounts.views import SignUpView, UpdateProfileView, ResetPasswordView, LoginView, LogoutView, TeamView, UserView

app_name = 'accounts'

urlpatterns = [
        path('login/', LoginView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('signup/', SignUpView.as_view(), name='signup'),
        path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
        path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
        path('profile/', ResetPasswordView.as_view(), name='profile'),
        path('update_password/', ResetPasswordView.as_view(), name='update_password'),
        
        path('users/', UserView.as_view(), name='user-list'),
        path('user/add/', UserView.as_view(), {"action":"add"}, name='user-detail'),
        path('user/<int:pk>/change/', UserView.as_view(), {"action":"change"}, name='user-detail'),
        path('user/<int:pk>/delete/', UserView.as_view(), {"action":"delete"}, name='user-delete'),

        path('teams/', TeamView.as_view(), name='team-list'),
        path('team/add/', TeamView.as_view(), {"action": "add"}, name='team-detail'),
        path('team/<int:pk>/change/', TeamView.as_view(), {"action": "change"}, name='team-detail'),
        path('team/<int:pk>/delete/', TeamView.as_view(), {"action": "delete"}, name='team-delete'),
]
