import logging

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http.response import HttpResponse
from home.base_views import BaseView
from projects.models import Project
from tasks.models import TaskType, Task, Filters
from tasks.forms import TaskTypeForm, TaskForm, FiltersForm
from projects.models import Project
from django.db.models import Q
from django.shortcuts import redirect, reverse
from tasks.filters.task_filters import TaskFilters


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
    template = "task-create.html"
    fields = ['key', 'project__name', 'tasktype__name', 'summary', 'priority', 'state']
    form = TaskForm

    def create(self, request, *args, **kwargs):
        context={
            "form" : self.form()
        }
        return render(request, self.template, context)

    def get_filter_data(self, request, task_filter):
        filter_obj = Filters.objects.get(id=task_filter)
        fields = filter_obj.fields.split(", ")
        fields_list = [row.strip().split("=") for row in fields]
        fields_pattern = {k:v for k,v in fields_list}
        for k, v in fields_pattern.items():
            if v.endswith('()'):
                fields_pattern[k] = getattr(TaskFilters, v.rstrip('()'))(request)
            elif "," in v:
                fields_pattern[k] = v.split(",")
        queryset = Task.objects.filter(**fields_pattern).values(*self.fields)
        return list(queryset)

    def get_tasks_by_project(self, name):
        try:
            project = Project.objects.get(name=name)        #noqa : Django Queryset
            queryset = Task.objects.filter(project=project)   #noqa : Django Queryset
            queryset = list(queryset.values(*self.fields))
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

    def get_tasks_by_tasktype(self, name):
        try:
            tasktype = TaskType.objects.get(name=name)        #noqa : Django Queryset
            queryset = Task.objects.filter(tasktype=tasktype)   #noqa : Django Queryset
            queryset = list(queryset.values(*self.fields))
        except Exception as e:
            logger.exception(e)
            queryset = []
        finally:
            return queryset

    def get_tasks(self):
        return list(Task.objects.all().values_list(*self.fields))

    def browse(self, request, task_key, *args, **kwargs):
        template="task-browse.html"
        context={}
        obj = None
        error = None
        buttons = []
        try:
            obj = Task.objects.get(key=task_key)
            transitions = obj.tasktype.get_avilable_transitions(obj.state)
            task_options = [
                { "name" : "edit", },
                { "name" : "create subtask" },
            ]
            for row in transitions:
                buttons.append(
                    { "name": row }
                )
            workflow_options = buttons
            context["task_options"] = task_options
            context["workflow_options"] = workflow_options
        except Exception as e:
            logger.exception(e)
            error = f"The requested resource {task_key} is either invalid or not found.!!!"
        finally:
            context["obj"] = obj
            context["error"] = error
            print(context)
            return render(request, template, context)

    def get_tasks_detail(self, project_name, tasktype):
        try:
            project = Project.objects.get(name=project_name)        #noqa : Django Queryset
            tasktype = TaskType.objects.get(name=tasktype)        #noqa : Django Queryset
            queryset = Task.objects.filter(project=project, tasktype=tasktype)   #noqa : Django Queryset
            queryset = list(queryset.values(*self.fields))
        except Exception as e:
            logger.exception(e)
            queryset = []
        finally:
            return queryset

    def search(self, request, *args, **kwargs):
        context = {}
        try:
            template="task-list.html"
            project_name = request.GET.get("project")
            task_filter = request.GET.get("filter")
            task_key = request.GET.get("key")
            text = request.GET.get("text")
            tasktype = request.GET.get("tasktype")

            name = f"{project_name} Tasks"

            if project_name and tasktype:
                queryset = self.get_tasks_detail(project_name, tasktype)
                name = f"{project_name} - {tasktype}"
            elif task_filter:
                queryset = self.get_filter_data(request, task_filter)
                name = "%s Tasks" %(Filters.objects.get(id=task_filter).name)
            elif project_name:
                queryset = self.get_tasks_by_project(name=project_name)
            elif tasktype:
                queryset = self.get_tasks_by_tasktype(name=tasktype)
                name = f"{tasktype} Tasks"
            elif task_key:
                queryset = self.get_task_by_key(key=task_key)
            elif text:
                queryset = self.get_task_by_text(text=text)
            else:
                queryset = self.get_tasks()
            context={
                "name": name,
                "queryset": queryset,
                "keys": self.fields,
                "link": "key"
            }
            return render(request, template, context)
        except Exception as e:
            logger.exception(e)
            template = "task-error.html"
            context["error"] = str(e)
            return render(request, template, context)


    def get(self, request, action, task_key=None, *args, **kwargs):
        if action == "create":
            return self.create(request, *args, **kwargs)
        elif action == "search":
            return self.search(request, *args, **kwargs)
        elif action == 'browse':
            return self.browse(request, task_key, *args, **kwargs)
        else:
            return HttpResponse("Unknown Action Receieved.")

    def post(self, request, action, pk=None, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            key = self.form_valid(form, pk)
            return redirect(reverse('tasks:browse', kwargs={"task_key": key}))
        else:
            context = {
                "form": form,
            }
            return render(request, self.template, context)

    def form_valid(self, form, pk):
        user = self.request.user
        obj = form.save(commit=False)
        obj.modified_by = user
        if not pk:
            # New Object being Created.
            key = obj.create_task(user)
        return key
