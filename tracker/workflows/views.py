from django.shortcuts import render
from django.views.generic import TemplateView, View
from home.base_views import BaseView
from workflows.models import Workflow, WorkflowStates, WorkflowTransitions
from workflows.forms import WorkflowForm, WorkflowStatesForm, WorkflowTransitionsForm


# Create your views here.
class WorkflowView(BaseView):
    model = Workflow
    form = WorkflowForm
    app = "workflows"
    model_name = "Workflow"

class WorkflowStatesView(BaseView):
    model = WorkflowStates
    form = WorkflowStatesForm
    app = "workflows"
    model_name = "Workflow States"

class WorkflowTransitionsView(BaseView):
    model = WorkflowTransitions
    form = WorkflowTransitionsForm
    app = "workflows"
    model_name = "Workflow Transitions"
