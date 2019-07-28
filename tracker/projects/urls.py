from django.urls import include, path

from projects.views import ProjectView, RolesView, PermissionsView

app_name = 'projects'

urlpatterns = [
    path('', ProjectView.as_view(), name='project-list'),
    path('add/', ProjectView.as_view(), {"action":"add"}, name='project-detail'),
    path('<int:pk>/change/', ProjectView.as_view(), {"action":"change"}, name='project-detail'),
    path('<int:pk>/delete/', ProjectView.as_view(), {"action":"delete"}, name='project-delete'),

    path('roles/', RolesView.as_view(), name='roles-list'),
    path('permissions/', PermissionsView.as_view(), name='permissions-list'),
]
