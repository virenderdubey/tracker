from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from projects.models import Project, Roles, Permissions
from projects.forms import ProjectForm, RolesForm, PermissionsForm


# Create your views here.
class BaseView(View):
    model = None
    app = "projects"
    keys = ['name']
    action = 'create'
    context={}
    form = None
    
    def get(self, request, pk=None, action=None, **kwargs):
        """ Used to serve all GET Request """
        # List View
        if pk and action is None:
            instance = get_object_or_404(self.model, pk=pk)
            self.context['instance'] = instance
        elif action=='add':
            self.context['form'] = self.form()
            self.context['template'] = "change.html"
            self.context["action"] = "create"
        elif action=='change':
            self.context['form'] = self.form(instance=instance)
            self.context['template'] = "change.html"
            self.context["action"] = "update"
        else:
            queryset = LOB.objects.all()



            



class ProjectView(View):
    model = Project
    app = ""
    template_name = "project.html"


class RolesView(View):
    template_name = "rules.html"

class PermissionView(View):
    template_name = "permissions.html"
