from django.urls import include, path

from home.views import HomeView, AboutView, AdminView

app_name = 'home'

urlpatterns = [
    path('admin/', AdminView.as_view(), name='admin'),
    path('about/', AboutView.as_view(), name='about'),
    path('', HomeView.as_view(), name='home')
]
