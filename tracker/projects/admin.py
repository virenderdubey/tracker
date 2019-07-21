from django.contrib import admin

from projects.models import Project, Permission, Roles


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    pass