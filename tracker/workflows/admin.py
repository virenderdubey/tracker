from django.contrib import admin

from workflows.models import WorkflowStates, WorkflowTransitions, Workflow

@admin.register(WorkflowStates)
class WorkflowStatesAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkflowTransitions)
class WorkflowTransitionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass

