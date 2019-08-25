from django.urls import include, path

from tasks.views import TaskTypeView, TaskView

app_name = 'tasks'

urlpatterns = [
    path('create/', TaskView.as_view(), {"action": "create" }, name='create'),
    path('search/', TaskView.as_view(), {"action": "search" }, name='search'),
    path('browse/<task_key>/', TaskView.as_view(), {"action":"browse"}, name='browse'),
    path('browse/<task_key>/edit/', TaskView.as_view(), {"action":"edit"}, name='edit'),
]
