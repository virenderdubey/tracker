# Generated by Django 2.2.3 on 2019-08-04 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkflowStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_state_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_state_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WorkflowTransitions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_transition_created_by', to=settings.AUTH_USER_MODEL)),
                ('from_state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_transition_from', to='workflows.WorkflowStates')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_transition_modified_by', to=settings.AUTH_USER_MODEL)),
                ('to_state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_transition_to', to='workflows.WorkflowStates')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workflow_modified_by', to=settings.AUTH_USER_MODEL)),
                ('transitions', models.ManyToManyField(to='workflows.WorkflowTransitions')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
