from django.contrib import admin

from projects.models import Project, Permissions, Roles


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    pass
