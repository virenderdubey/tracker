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
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="TaskType created by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="TaskType modified by")

class Task(object):
    """ Create Task Model """
    TASK_PRIORITY = (
        ("P0", "P0"),
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3"),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tasknum = models.PositiveIntegerField()
    tasktype = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    summary = models.CharField(max_length=100, blank=False, null=False, unique=False)
    description = models.TextField()
    priority = models.CharField(choices=TASK_PRIORITY, max_length=3, default="P3")
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task created by")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task modified by")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task assigned to")
    due_date = models.DateTimeField(default=None)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

class DependencyTasks(object):
    """ Creating Task Dependencies """
    dependency_type = models.CharField(max_length=100, unique=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="Parent Task")
    dependent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="Dependent Task")

class Attachments(object):
    """ Attachments for a Task """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='attachments/')

class Comments(object):
    """ Comments Model """
    