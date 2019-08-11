from django import forms

from workflows.models import WorkflowStates, WorkflowTransitions, Workflow

class WorkflowStatesForm(forms.ModelForm):
    ui_fields = ['id', 'name']
    link = "name"

    class Meta:
        model = WorkflowStates
        exclude = ('created_at', 'modified_at', 'created_by', 'modified_by')

class WorkflowTransitionsForm(forms.ModelForm):
    ui_fields = ['id', 'name']
    link = "name"

    class Meta:
        model = WorkflowTransitions
        exclude = ('created_at', 'modified_at', 'created_by', 'modified_by')

class WorkflowForm(forms.ModelForm):
    ui_fields = ['id', 'name']
    link = "name"

    class Meta:
        model = Workflow
        exclude = ('created_at', 'modified_at', 'created_by', 'modified_by')
