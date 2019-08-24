import logging
from django.db import models
from workflows.models import Workflow
from projects.models import Project
from accounts.models import User

logger = logging.getLogger(__name__)


# Create your models here.
class TaskType(models.Model):
    """ Model to create Task Types """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasktype_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasktype_modified_by")

    def __str__(self):
        return self.name

    def get_avilable_transitions(self, transition):
        return self.workflow.get_avilable_transitions(transition)

class Task(models.Model):
    """ Create Task Model """
    TASK_PRIORITY = (
        ("P0", "P0"),
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3"),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tasktype = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    summary = models.CharField(max_length=100, blank=False, null=False, unique=False)
    description = models.TextField()
    priority = models.CharField(choices=TASK_PRIORITY, max_length=3, default="P3")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_assigned_to")
    due_date = models.DateField(default=None)
    
    key = models.CharField(max_length=20, unique=True, blank=False, null=False, editable=False)
    watchers = models.CharField(max_length=500, unique=False, blank=True, null=True, editable=False)
    state =models.CharField(max_length=100, unique=False, blank=False, null=False, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_modified_by")

    @property
    def reporter(self):
        return self.created_by

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def _get_initial_transition_state(self):
        try:
            return self.tasktype.get_avilable_transitions("Create")[0]
        except Exception as e:
            logger.exception(e)
            return "unknown"

    def create_task(self, user):
        # new object created, Get default Parameters
        self.created_by = user
        self.watchers = user.email
        self.state = self._get_initial_transition_state()
        sequence = Project.get_sequence(self.project.name)
        key = f"{self.project.key}-{sequence}"
        self.key = key
        self.save()
        return key

class TaskDependency(models.Model):
    """ Creating Task Dependencies """
    dependency_type = models.CharField(max_length=100, unique=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="parent_task")
    dependent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="dependent_task")


class Attachments(models.Model):
    """ Attachments for a Task """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, unique=False)
    file_path = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attachements_created_by")


class Comments(models.Model):
    """ Comments Model """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, unique=False)
    comments = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments_modified_by")

class Filters(models.Model):
    """ Model to create Search Filters """
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.CharField(max_length=500, null=True)
    fields = models.CharField(max_length=500, null=False, blank=False)
    ordering = models.CharField(max_length=500, default="modified_at")
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="filters_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="filters_modified_by")
