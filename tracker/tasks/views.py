from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http.response import HttpResponse
from home.base_views import BaseView
from tasks.models import TaskType, Task, Filters
from tasks.forms import TaskTypeForm, TaskForm, FiltersForm


# Create your views here.
class TaskTypeView(BaseView):
    form = TaskTypeForm
    model = TaskType
    app = "admin_tasks"
    model_name = "Task Type"


class FiltersView(BaseView):
    form = FiltersForm
    model = Filters
    app = "admin_tasks"
    model_name = "Filters"


class TaskView(View):
    template = "create.html"

    def create(self, request, *args, **kwargs):
        context={
            "form" : TaskForm()
        }
        return render(request, self.template, context)

    def get(self, request, action, *args, **kwargs):
        if action == "create":
            return self.create(request, *args, **kwargs)
        elif action == "search":
            return HttpResponse("Action is in Progress")
        

    def post(self, request, action, *args, **kwargs):
        return HttpResponse("Post Api Creation in Progress")
