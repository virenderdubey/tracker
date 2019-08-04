from django.urls import include, path

from workflows.views import WorkflowView, WorkflowStatesView, WorkflowTransitionsView

app_name = 'workflows'

urlpatterns = [
    path('', WorkflowView.as_view(), name='workflow-list'),
    path('add/', WorkflowView.as_view(), {"action":"add"}, name='workflow-detail'),
    path('<int:pk>/change/', WorkflowView.as_view(), {"action":"change"}, name='workflow-detail'),
    path('<int:pk>/delete/', WorkflowView.as_view(), {"action":"delete"}, name='workflow-delete'),

    path('states/', WorkflowStatesView.as_view(), name='workflowstates-list'),
    path('states/add/', WorkflowStatesView.as_view(), {"action":"add"}, name='workflowstates-detail'),
    path('states/<int:pk>/change/', WorkflowStatesView.as_view(), {"action":"change"}, name='workflowstates-detail'),
    path('states/<int:pk>/delete/', WorkflowStatesView.as_view(), {"action":"delete"}, name='workflowstates-delete'),

    path('transitions/', WorkflowTransitionsView.as_view(), name='workflowtransitions-list'),
    path('transitions/add/', WorkflowTransitionsView.as_view(), {"action":"add"}, name='workflowtransitions-detail'),
    path('transitions/<int:pk>/change/', WorkflowTransitionsView.as_view(), {"action":"change"}, name='workflowtransitions-detail'),
    path('transitions/<int:pk>/delete/', WorkflowTransitionsView.as_view(), {"action":"delete"}, name='workflowtransitions-delete'),    
]
