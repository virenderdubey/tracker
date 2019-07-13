from django.db import models
from django.contrib.auth.models import User as DjangoUser, Group as DjangoGroup


# Create your models here.
class User(DjangoUser):
    status = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    @property
    def is_admin(self):
        return self.is_superuser


class Team(DjangoGroup):
    description = models.CharField(max_length=765, default=None)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    @property
    def members(self):
        return self.user_set
