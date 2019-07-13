from django.db import models
from workflow.models import Workflow
from project.models import Project
from auth.models import User


# Create your models here.
class TaskType(object):
    """ Model to create Task Types """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow state created by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Workflow state modified by")

class Task(object):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)