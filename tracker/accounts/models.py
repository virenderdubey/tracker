from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def clean(self):
        model_error={}
        super().clean()
        if '@' not in self.email:
            model_error["email"] = ValidationError(_("Invalid format of Email..!!"), code="invalid")
        if model_error:
            raise ValidationError(model_error)

    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.CharField(max_length=50, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    avatar = models.ImageField(blank=True, null=True)
    aboutme = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name}"

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if not self.first_name:
            self.first_name = self.username
        if not self.last_name:
            self.last_name = self.username
        super().save(*args, **kwargs)

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    members = models.ManyToManyField(User, limit_choices_to={"is_active": True}, related_name="members")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="team_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="team_modified_by")

    def __str__(self):
        return self.name
