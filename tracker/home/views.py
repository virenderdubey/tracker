import logging

from django.shortcuts import render
from django.views.generic import TemplateView, View
from tasks.models import Task
from projects.models import Project
from tasks.models import Filters
from accounts.models import User

logger = logging.getLogger(__name__)


# Create your views here.
class HomeView(View):
    template_name = "home.html"
    login_template_name = "dashboard.html"
    fields = ['id', 'name']
    task_fields = ['key', 'tasktype__name', 'summary', 'priority', 'state']
    task_ui_fields = ['key', 'type', 'summary', 'priority', 'state']

    def _get_all_projects(self):
        return list(Project.objects.filter(status=True).values(*self.fields))

    def _get_user_filters(self, user):
        return list(Filters.objects.filter(created_by=user, status=True).values(*self.fields))

    def _get_system_filters(self, username):
        try:
            user = User.objects.get(username=username)
            return list(Filters.objects.filter(created_by=user, status=True).values(*self.fields))
        except Exception as e:
            logger.exception(e)
            user = None
            return []

    def _get_user_assigned_tasks(self, user):
        queryset = Task.objects.filter(assignee=user).values(*self.task_fields)
        return queryset

    def _get_user_reported_tasks(self, user):
        queryset = Task.objects.filter(created_by=user).values(*self.task_fields)
        return queryset

    def get(self, request):
        context={}
        if request.user.is_authenticated:
            username = request.user.username
            projects = self._get_all_projects()
            system_filters = self._get_system_filters(username="tracker")
            user_filters = self._get_user_filters(request.user)
            request.session[username] = {
                "projects" : projects,
                "filters": system_filters + user_filters,
            }
            context["assigned_filters"] = self._get_user_assigned_tasks(request.user)
            context["reported_filters"] = self._get_user_reported_tasks(request.user)
            context["task_fields"] = self.task_ui_fields

            # Fetch all filters created by user and system and add in session.
            template = self.login_template_name
        else:
            try:
                error = request.session.pop("login_error")
            except KeyError:
                error = None
            if error:
                context["error"] = error
            template = self.template_name
        return render(request, template, context)

class AboutView(TemplateView):
    template_name = "about.html"

class AdminView(TemplateView):
    template_name = "admin.html"
