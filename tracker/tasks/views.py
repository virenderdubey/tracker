import logging

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http.response import HttpResponse
from home.base_views import BaseView
from tasks.models import TaskType, Task, Filters
from tasks.forms import TaskTypeForm, TaskForm, FiltersForm
from projects.models import Project
from django.db.models import Q


logger = logging.getLogger(__name__)

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
    fields = ['id', 'project__name', 'tasktype__name', 'summary', 'priority']

    def create(self, request, *args, **kwargs):
        context={
            "form" : TaskForm()
        }
        return render(request, self.template, context)

    def get_filter_data(self, request, task_filter):
        return []
    
    def get_tasks_by_project(self, name):
        try:
            project = Project.objects.get(name=name)        #noqa : Django Queryset
            queryset = list(Task.objects.filters(project=project))    #noqa : Django Queryset
        except Exception as e:
            logger.exception(e)
            queryset = []
        finally:
            return queryset
    
    def get_task_by_key(self, key):
        try:
            name, task_id = key.split("-")
            project = Project.objects.get(key=name)         #noqa : Django Queryset
            queryset = Task.objects.filter(project=project, tasknum=task_id)    #noqa : Django Queryset
            queryset = list(queryset)
        except Exception as e:
            logger.exception(e)
            queryset = []
        finally:
            return queryset

    def get_task_by_text(self, text):
        return list(Task.objects.filter(Q(summary__contains = text) | Q(description__contains = text)).values_list(*self.fields))
    
    def get_tasks(self):
        return list(Task.objects.all().values_list(*self.fields))

    def search(self, request, *args, **kwargs):
        template="tasks-list.html"
        project_name = request.GET.get("project")
        task_filter = request.GET.get("filter")
        task_key = request.GET.get("key")
        text = request.GET.get("text")

        if task_filter:
            queryset = self.get_filter_data(request, task_filter)
        elif project_name:
            queryset = self.get_tasks_by_project(name=project_name)
        elif task_key:
            queryset = self.get_task_by_key(key=task_key)
        elif text:
            queryset = self.get_task_by_text(text=text)
        else:
            queryset = self.get_tasks()
        context={
            "project": project_name,
            "queryset": queryset
        }
        return render(request, template, context)

    def get(self, request, action, *args, **kwargs):
        if action == "create":
            return self.create(request, *args, **kwargs)
        elif action == "search":
            return self.search(request, *args, **kwargs)
        else:
            return HttpResponse("Unknown Action Receieved.")

    def post(self, request, action, *args, **kwargs):
        return HttpResponse("Post Api Creation in Progress")

