from django.urls import include, path

from tasks.views import TaskTypeView, TaskView, FiltersView

app_name = 'admin_tasks'

urlpatterns = [
    path('types/', TaskTypeView.as_view(), name='tasktype-list'),
    path('type/add/', TaskTypeView.as_view(), {"action":"add"}, name='tasktype-detail'),
    path('type/<int:pk>/change/', TaskTypeView.as_view(), {"action":"change"}, name='tasktype-detail'),
    path('type/<int:pk>/delete/', TaskTypeView.as_view(), {"action":"delete"}, name='tasktype-delete'),

    path('filters/', FiltersView.as_view(), name='filters-list'),
    path('filters/add/', FiltersView.as_view(), {"action":"add"}, name='filters-detail'),
    path('filters/<int:pk>/change/', FiltersView.as_view(), {"action":"change"}, name='filters-detail'),
    path('filters/<int:pk>/delete/', FiltersView.as_view(), {"action":"delete"}, name='filters-delete'),
]
