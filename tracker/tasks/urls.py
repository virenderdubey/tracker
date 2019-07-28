from django.urls import include, path

from tasks.views import TaskTypeView

app_name = 'tasks'

urlpatterns = [
    path('type/', TaskTypeView.as_view(), name='type'),
]
