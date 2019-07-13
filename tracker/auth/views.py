from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import View

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

# Create your views here.
class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and passwor, not in used anymore
    """
    success_url = "/"
    form_class = AuthenticationForm
    redirect_field_name = "next"
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Login the User.
        username = form.get_user()
        login(self.request, username)

        # If the test cookie worked, go ahead and delete it since its no longer needed.
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(LoginView, self).form_valid(form)
    

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)

        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

class LogoutView(RedirectView):
    """
    Provides users the ability to logout, not in used anymore
    """
    url = settings.LOGOUT_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignUpView(View):
    pass


class UserView(View):
    pass