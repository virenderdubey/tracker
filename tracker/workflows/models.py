import logging
from django.db import models
from accounts.models import User

logger = logging.getLogger(__name__)

# Create your models here.
class WorkflowStates(models.Model):
    """ Model to create Workflow State """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_state_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_state_modified_by")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class WorkflowTransitions(models.Model):
    """ Model to create Workflow Transition """
    name = models.CharField(max_length=100, unique=False, null=False, blank=False)
    description = models.CharField(max_length=500, null=True)
    from_state = models.ForeignKey(WorkflowStates, on_delete=models.PROTECT, related_name="workflow_transition_from")
    to_state = models.ForeignKey(WorkflowStates, on_delete=models.PROTECT, related_name="workflow_transition_to")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_transition_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_transition_modified_by")

    def __str__(self):
        return "%s : %s" %(self.name, self.description)

    class Meta:
        ordering = ['modified_at', 'name']


class Workflow(models.Model):
    """ Model to create Workflow """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    transitions = models.ManyToManyField(WorkflowTransitions)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workflow_modified_by")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_avilable_transitions(self, transition):
        next_transition = []
        try:
            for row in self.transitions.get_queryset():
                if row.from_state.name == transition:
                    next_transition.append(row.to_state.name)
        except Exception as e:
            logger.exception(e)
        finally:
            return next_transition
