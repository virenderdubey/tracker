from django.shortcuts import render
from django.views.generic import TemplateView, View
from projects.models import Project
from tasks.models import Filters
from accounts.models import User


# Create your views here.
class HomeView(View):
    template_name = "home.html"
    login_template_name = "dashboard.html"

    def _get_all_projects(self):
        return list(Project.objects.filter(status=True).values_list('name', flat=True))
    
    def _get_user_filters(self, user):
        return list(Filters.objects.filter(created_by=user, status=True).values_list('name', flat=True))
    
    def _get_system_filters(self, username):
        try:
            user = User.objects.get(username=username)
            return list(Filters.objects.filter(created_by=user, status=True).values_list('name', flat=True))
        except Exception as e:
            user = None
            return []

    def get(self, request, context=None):
        if request.user.is_authenticated:
            username = request.user.username
            projects = self._get_all_projects()
            system_filters = self._get_system_filters(username="tracker")
            user_filters = self._get_user_filters(request.user)
            request.session[username] = {
                "projects" : projects,
                "filters": system_filters + user_filters,
            }
            # Fetch all filters created by user and system and add in session.
            template = self.login_template_name
        else:
            template = self.template_name
        return render(request, template, context)

class AboutView(TemplateView):
    template_name = "about.html"

class AdminView(TemplateView):
    template_name = "admin.html"
