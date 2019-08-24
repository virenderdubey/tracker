from django import forms

from tasks.models import TaskType, Task, Filters, Attachments, Comments

class TaskTypeForm(forms.ModelForm):
    ui_fields = ['id', 'name']
    link = "name"

    class Meta:
        model = TaskType
        exclude = ('created_on', 'modified_on', 'created_by', 'modified_by')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('created_on', 'modified_on', 'created_by', 'modified_by')

class FiltersForm(forms.ModelForm):
    ui_fields = ['id', 'name']
    link = "name"
    
    class Meta:
        model = Filters
        exclude = ('created_on', 'modified_on', 'created_by', 'modified_by')


class AttachmentsForm(forms.ModelForm):
    class Meta:
        model = Attachments
        exclude = ('task', 'created_on', 'created_by')


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        widgets = {
            'comment': forms.Textarea(attrs={"rows": 3})
        }
        exclude = ('task', 'created_on', 'modified_on', 'created_by', 'modified_by')
