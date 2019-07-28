from django.db import models
from accounts.models import User


# Create your models here.
class WorkflowStates(models.Model):
    """ Model to create Workflow State """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_state_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_state_modified_by")


class WorkflowTransitions(models.Model):
    """ Model to create Workflow Transition """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    from_state = models.ForeignKey(WorkflowStates, on_delete=models.PROTECT, related_name="workflow_transition_from")
    to_state = models.ForeignKey(WorkflowStates, on_delete=models.PROTECT, related_name="workflow_transition_to")

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_transition_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_transition_modified_by")


class Workflow(models.Model):
    """ Model to create Workflow """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    transitions = models.ManyToManyField(WorkflowTransitions)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_modified_by")
