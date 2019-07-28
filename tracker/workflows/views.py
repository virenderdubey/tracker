from django.shortcuts import render
from django.views.generic import TemplateView, View


# Create your views here.
class WorkflowView(View):
    template_name = "workflow.html"

class WorkflowStatesView(View):
    template_name = "states.html"

class WorkflowTransitionsView(View):
    template_name = "transitions.html"
