from django.shortcuts import render
from django.views.generic import TemplateView, View


# Create your views here.
class TaskTypeView(View):
    template_name = "tasktype.html"

