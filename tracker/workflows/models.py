from django.db import models
from auth.models import User
from auth.models import Team

# Create your models here.
class WorkflowStates(object):
    """ Model to create Workflow State """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow state created by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow state modified by")

class WorkflowTransitions(object):
    """ Model to create Workflow Transition """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    from_state = models.ForeignKey(WorkflowStates, on_delete=models.PROTECT, related_name="Workflow Transition created by")
    to_state = models.ForeignKey(WorkflowStates, on_delete=models.PROTECT, related_name="Workflow Transition modified by")

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow state created by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow state modified by")

class Workflow(object):
    """ Model to create Workflow """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    transitions = models.ManyToManyField(WorkflowTransitions)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow created by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow modified by")
