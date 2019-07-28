from django.urls import include, path

from projects.views import ProjectView, RulesView, PermissionsView

app_name = 'projects'

urlpatterns = [
    path('config/', ProjectView.as_view(), name='config'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('permissions/', PermissionsView.as_view(), name='permission')
]
