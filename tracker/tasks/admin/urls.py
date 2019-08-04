from django.urls import include, path

from tasks.views import TaskTypeView, TaskView

app_name = 'admin_tasks'

urlpatterns = [
    path('types/', TaskTypeView.as_view(), name='tasktype-list'),
    path('type/add/', TaskTypeView.as_view(), {"action":"add"}, name='tasktype-detail'),
    path('type/<int:pk>/change/', TaskTypeView.as_view(), {"action":"change"}, name='tasktype-detail'),
    path('type/<int:pk>/delete/', TaskTypeView.as_view(), {"action":"delete"}, name='tasktype-delete'),
]
