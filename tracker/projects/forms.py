from django import forms

from projects.models import Project, Roles, Permissions

class ProjectForm(forms.ModelForm):
    ui_fields = ['id', 'name', 'owner__username','key']
    link = "name"

    class Meta:
        model = Project
        exclude = ('created_at', 'modified_at', 'created_by', 'modified_by')


class RolesForm(forms.ModelForm):
    ui_fields = ['id', 'name','permission__name', 'project__name']
    link = "name"

    class Meta:
        model = Roles
        exclude = ('created_at', 'modified_at', 'created_by', 'modified_by')


class PermissionsForm(forms.ModelForm):
    ui_fields = ['id', 'name']
    link = "name"

    class Meta:
        model = Permissions
        exclude = ('created_at', 'modified_at', 'created_by', 'modified_by')
