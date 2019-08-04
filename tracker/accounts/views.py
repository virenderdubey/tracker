from django.contrib.auth.forms import UserCreationForm
from accounts.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View, RedirectView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.conf import settings

from accounts.forms import UserForm, TeamForm
from accounts.models import User, Team
from home.base_views import BaseView

import logging

logger = logging.getLogger(__name__)


class LogoutView(RedirectView):
    url = settings.LOGIN_URL
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home:home')
    template_name = 'signup.html'

class UpdateProfileView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('logip-=[pn')
    template_name = 'signup.html'

class ResetPasswordView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class LoginView(View):
    error = None

    def _update_session(self, request, username, **kwargs):
        print(self.request.session)
        print(self.request.session.items())

        if username not in self.request.session:
            self.request.session[username] = {}
        self.request.session[username].update(**kwargs)
        self.request.session.modified=True

    def post(self, request, *args, **kwargs):
        error="Invalid Credentials.!!"
        context={}
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is None:
                raise Exception(error)
            else:
                login(self.request, user)
                self._update_session(request, username, auth=True)
        except Exception as e:
            logging.exception(e)
            self._update_session(request, username, error=error)
            context["error"] = str(e)
        finally:
            return redirect('home:home')


class AboutView(TemplateView):
    template_name = "about.html"

class TeamView(BaseView):
    form = TeamForm
    model = Team
    app = "accounts"

class UserView(BaseView):
    form = UserForm
    model = User
    app = "accounts"
