from django.db import models
from auth.models import User, Team


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={"status": True})
    key = models.CharField(max_length=10, unique=True)
    sequence = models.PositiveIntegerField()
    status = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="project_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="project_modified_by")


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="permission_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="permission_modified_by")

class Roles(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, limit_choices_to={"status": True})
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)
    team = models.ManyToManyField(Team)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="roles_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="roles_modified_by")
