import logging

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from projects.models import Project, Roles, Permissions
from projects.forms import ProjectForm, RolesForm, PermissionsForm

from django.http import HttpResponseRedirect
from django.urls import reverse


logger = logging.getLogger(__name__)


# Create your views here.
class BaseView(View):
    model = None
    app = "projects"
    action = 'create'
    context={}
    form = None
    model_name = None

    def get(self, request, pk=None, action=None, **kwargs):
        """ Used to serve all GET Request """
        logger.info("Parameters Receieved, PK - %s, Action - %s" % (pk, action))

        if action=='add':
            self.context['form'] = self.form()
            self.context['template'] = "change.html"
            self.context["action"] = "create"
        elif action=='change':
            instance = get_object_or_404(self.model, pk=pk)
            self.context['instance'] = instance
            self.context['form'] = self.form(instance=instance)
            self.context['template'] = "change.html"
            self.context["action"] = "update"
        else:
            queryset = self.model.objects.all()
            request_params = request.GET
            request_params = dict(request_params.lists())
            search_params={}
            for key, val in request_params.items():
                if type(val) is list:
                    p_key="%s__in" %(key)
                else:
                    p_key=key
                search_params[p_key] = val
            self.context["request_params"] = request_params

            if search_params:
                queryset = queryset.filter(**search_params)
            keys = self.form.ui_fields
            if "id" not in keys:
                keys += ["id"]
            queryset_data = queryset.order_by('id').values(*keys)

            # Get Link Objects
            try:
                self.context["link"] = self.form.link
            except: # noqa
                self.context["link"] = self.link

            self.context["keys"] = keys
            self.context['queryset'] = queryset_data
            self.context['template'] = "list.html"

        self.context["model"] = self.model_name if self.model_name else str(self.model.__name__).lower()
        self.context["namespace"] = self.app

        # Return all requests
        return render(request, self.context.get("template"), self.context)

    def post(self, request, pk=None, action=None, **kwargs):
        logger.info("Params Receieved - pk - %s, Action - %s" %(pk, action))
        form = None
        try:
            instance = get_object_or_404(self.model, id=pk)
        except:  # noqa
            instance = None

        # Get Redirect URI
        uri = f"{self.app}:{self.model.__name__.lower()}-list"

        if instance:
            """ This is either Update or Delete Request """
            if action == 'change':
                form = self.form(request.POST, instance=instance)
            elif action == 'delete':
                instance.delete()
                return HttpResponseRedirect(reverse(uri))
        else:
            """ This is Create Request """
            form = self.form(request.POST)

        self.context['form'] = form
        self.context['instance'] = instance
        self.context['template'] = 'change.html'

        if form.is_valid():
            self.save_form(form, pk)
            return HttpResponseRedirect(reverse(uri))
        else:
            return render(request, self.context.get("template"), self.context)

    def save_form(self, form, pk):
        user = self.request.user
        form._save_m2m()
        obj = form.save(commit=False)
        obj.modified_by = user
        if not pk:
            # new object created
            obj.created_by = user
        obj.save()
