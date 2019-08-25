import logging

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http.response import HttpResponse
from home.base_views import BaseView
from projects.models import Project
from tasks.models import TaskType, Task, Filters, Comments, TaskDependency, Attachments
from tasks.forms import TaskTypeForm, TaskForm, FiltersForm, CommentsForm, AttachmentsForm
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

    def create(self, request, task_key=None, *args, **kwargs):
        parent = request.GET.get("key")
        if task_key is None:
            form = self.form()
            action = action_button="Add New"
        else:
            task = Task.objects.get(key = task_key)
            form = self.form(instance=task)
            action = "Change"
            action_button = "Update"
        context={
            "form" : form,
            "action": action,
            "action_button": action_button,
            "parent": parent,
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
            tasktype = TaskType.objects.get(name=name)          # noqa : Django Queryset
            queryset = Task.objects.filter(tasktype=tasktype)   # noqa : Django Queryset
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
            comments = Comments.objects.filter(task=obj.id).values('comment', 'created_by__username')
            attachments = Attachments.objects.filter(task=obj.id).values('file_path')
            childs = TaskDependency.objects.filter(task=obj, dependency_type="subtask")
            childs = [ { "key": row.dependent_task.key, "summary": row.dependent_task.summary, "type": row.dependency_type } for row in subtasks ]

            new_comments_form = CommentsForm()
            upload_attachments_form = AttachmentsForm()

            task_options = [
                { "name" : "edit", },
                { "name" : "create subtask" }
            ]
            for row in transitions:
                buttons.append(
                    { "name": row }
                )

            workflow_options = buttons
            context["task_options"] = task_options
            context["workflow_options"] = workflow_options
            context["comments"] = comments
            context["attachments"] = attachments
            context["new_comments_form"] = new_comments_form
            context["upload_attachments_form"] = upload_attachments_form
            context["subtasks"] = subtasks

        except Exception as e:
            logger.exception(e)
            error = f"The requested resource {task_key} is either invalid or not found.!!!"
        finally:
            context["obj"] = obj
            context["error"] = error
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
            return self.create(request, task_key)
        elif action == "search":
            return self.search(request, *args, **kwargs)
        elif action == 'browse':        
            return self.browse(request, task_key, *args, **kwargs)
        elif action == 'edit':
            return self.create(request, task_key)
        else:
            return HttpResponse("Unknown Action Receieved.")

    def post(self, request, action, task_key=None, pk=None, *args, **kwargs):
        if action in [ "create", "edit" ]:
            parent_key = request.GET.get("key")
            parent=Task.objects.get(key=parent_key)
            try:
                instance = Task.objects.get(key=task_key)
                form = self.form(request.POST, instance=instance)
            except:
                instance = None
                form = self.form(request.POST)

            if form.is_valid():
                key = self.form_valid(form, instance, parent)
                return redirect(reverse('tasks:browse', kwargs={"task_key": key}))
            else:
                context = {
                    "form": form,
                }
            return render(request, self.template, context)
        elif action == 'browse':
            task_obj = Task.objects.get(key=task_key)
            user = self.request.user
            comment = request.POST.get("comment")
            
            # Uploading Attachments
            if request.FILES:
                form = AttachmentsForm(request.POST, request.FILES)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.created_by = user
                    obj.task = task_obj
                    obj.save()

            # Adding Comments
            if comment:
                form = CommentsForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.task=task_obj
                    obj.modified_by = user
                    obj.created_by = user
                    obj.save()
            return redirect('tasks:browse', task_key=task_key)

    def form_valid(self, form, pk, parent):
        user = self.request.user
        obj = form.save(commit=False)
        obj.modified_by = user
        if not pk:
            # New Object being Created.
            key = obj.create_task(user)
        if parent:
            TaskDependency.objects.create(dependency_type="subtask", task=parent, dependent_task=obj)
        return key
