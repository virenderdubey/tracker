from django.db import models
from accounts.models import User, Team


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.CharField(max_length=500, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={"is_active": True})
    key = models.CharField(max_length=10, unique=True, null=False, blank=False)
    sequence = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="project_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="project_modified_by")

    def __str__(self):
        return self.name


class Permissions(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.CharField(max_length=500, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="permission_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="permission_modified_by")

    def __str__(self):
        return self.name


class Roles(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.CharField(max_length=500, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, limit_choices_to={"status": True})
    permission = models.ForeignKey(Permissions, on_delete=models.PROTECT)
    team = models.ManyToManyField(Team)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="roles_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="roles_modified_by")

    def __str__(self):
        return "%s:%s" %(self.project, self.permission)
