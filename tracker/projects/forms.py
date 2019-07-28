from django import forms

from projects.models import Project, Roles, Permissions

class ProjectForm(forms.ModelForm):
    ui_fields = ['id', 'name']

    class Meta:
        model = Project
        exclude = ('created_on', 'modified_on', 'created_by', 'modified_by')


class RolesForm(forms.ModelForm):
    ui_fields = ['id', 'name']

    class Meta:
        model = Roles
        exclude = ('created_on', 'modified_on', 'created_by', 'modified_by')


class PermissionsForm(forms.ModelForm):
    ui_fields = ['id', 'name']

    class Meta:
        model = Permissions
        exclude = ('created_on', 'modified_on', 'created_by', 'modified_by')