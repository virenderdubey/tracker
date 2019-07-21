from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.CharField(max_length=50, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(blank=True, null=True)
    aboutme = models.TextField()
    mobile = models.CharField(max_length=12)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return f"{self.first_name}"

    def __str__(self):
        return self.get_full_name()


class Teams(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    members = models.ManyToManyField(User, limit_choices_to={"is_active": True}, related_name="members")

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="team_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="team_modified_by")
