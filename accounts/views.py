from django.contrib.auth import login
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as LoginVU
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.http import HttpResponse
import time
from .tasks import send_email

# Create your views here.

# ویوهای ابتدایی حساب کاربری همراه با سفارشی سازی کلاسهای موجود در پکیجهای افزوده شده ضروری


class LoginView(LoginVU):
    """استفاده از تمپلتهای موجود در مثال"""

    template_name = "accounts/login.html"
    fields = "username", "password"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:list_tasks")


class RegisterView(FormView):
    """استفاده از تمپلتهای موجود در مثال"""

    template_name = "accounts/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:list_tasks")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("list_tasks")
        return super(RegisterPage, self).get(*args, **kwargs)


def sendEmail(request):
    send_email.delay()
    return HttpResponse("<h1>Sending Done...</h1>")
