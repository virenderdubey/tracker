from django.contrib import admin

from tasks.models import TaskType, Task, Comments, Attachments, TaskDependency


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Attachments)
class AttachmentsAdmin(admin.ModelAdmin):
    pass
