from django.urls import include, path

from workflows.views import WorkflowView, WorkflowStatesView, WorkflowTransitionsView

app_name = 'workflows'

urlpatterns = [
    path('config/', WorkflowView.as_view(), name='config'),
    path('states/', WorkflowStatesView.as_view(), name='states'),
    path('transitions/', WorkflowTransitionsView.as_view(), name='transitions')
]
