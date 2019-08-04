import logging

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from projects.models import Project, Roles, Permissions
from projects.forms import ProjectForm, RolesForm, PermissionsForm
from home.base_views import BaseView

from django.http import HttpResponseRedirect
from django.urls import reverse


logger = logging.getLogger(__name__)


class ProjectView(BaseView):
    model = Project
    app = "projects"
    form = ProjectForm

class RolesView(BaseView):
    model = Roles
    app = "projects"
    form = RolesForm

class PermissionsView(BaseView):
    model = Permissions
    app = "projects"
    form = PermissionsForm
