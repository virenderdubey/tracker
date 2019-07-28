from django.db import models
from workflows.models import Workflow
from projects.models import Project
from accounts.models import User


# Create your models here.
class TaskType(models.Model):
    """ Model to create Task Types """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasktype_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasktype_modified_by")


class Task(models.Model):
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
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_modified_by")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_assigned_to")
    due_date = models.DateTimeField(default=None)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class TaskDependency(models.Model):
    """ Creating Task Dependencies """
    dependency_type = models.CharField(max_length=100, unique=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="parent_task")
    dependent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="dependent_task")


class Attachments(models.Model):
    """ Attachments for a Task """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, unique=False)
    file_path = models.FileField(upload_to='attachments/')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attachements_created_by")


class Comments(models.Model):
    """ Comments Model """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, unique=False)
    comments = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments_modified_by")
