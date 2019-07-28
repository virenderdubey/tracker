from django.shortcuts import render
from django.views.generic import TemplateView, View


# Create your views here.
class HomeView(View):
    template_name = "home.html"
    login_template_name = "dashboard.html"

    def get(self, request, context=None):
        if request.user.is_authenticated:
            template = self.login_template_name
        else:
            template = self.template_name
        return render(request, template, context)

class AboutView(TemplateView):
    template_name = "about.html"

class AdminView(View):
    template_name = "admin.html"
    context = {}
    def get(self, request, *args, **kwargs):
        self.context["left_pane_items"] = [
            { "name" : "projects", "url" : "#" },
            { "name" : "Task Type", "url" : "#" },
            { "name" : "Permissions", "url" : "#" },
            { "name" : "roles", "url" : "#" },
            { "name" : "workflows", "url" : "#" },
            { "name" : "workflow states", "url" : "#" },
            { "name" : "workflow transition", "url" : "#" }   
        ]
        return render(request, self.template_name, self.context)
