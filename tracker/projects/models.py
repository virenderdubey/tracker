from django.db import models
from auth.models import User
from auth.models import Team

# Create your models here.
class Project(object):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    lead = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={"status" : True})
    key = models.CharField(max_lenght=10, unique=True)
    sequence = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

class Permission(object):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

class Roles(object):
    pass