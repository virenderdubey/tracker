from django.urls import include, path

from projects.views import ProjectView, RolesView, PermissionsView

app_name = 'projects'

urlpatterns = [
    path('', ProjectView.as_view(), name='project-list'),
    path('add/', ProjectView.as_view(), {"action":"add"}, name='project-detail'),
    path('<int:pk>/change/', ProjectView.as_view(), {"action":"change"}, name='project-detail'),
    path('<int:pk>/delete/', ProjectView.as_view(), {"action":"delete"}, name='project-delete'),

    path('roles', RolesView.as_view(), name='roles-list'),
    path('roles/add/', RolesView.as_view(), {"action":"add"}, name='roles-detail'),
    path('roles/<int:pk>/change/', RolesView.as_view(), {"action":"change"}, name='roles-detail'),
    path('roles/<int:pk>/delete/', RolesView.as_view(), {"action":"delete"}, name='roles-delete'),

    path('permissions', PermissionsView.as_view(), name='permissions-list'),
    path('permissions/add/', PermissionsView.as_view(), {"action":"add"}, name='permissions-detail'),
    path('permissions/<int:pk>/change/', PermissionsView.as_view(), {"action":"change"}, name='permissions-detail'),
    path('permissions/<int:pk>/delete/', PermissionsView.as_view(), {"action":"delete"}, name='permissions-delete'),
]
