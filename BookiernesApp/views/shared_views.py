from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.views import View
from django.views.generic import CreateView, TemplateView

from BookiernesApp.forms import SignUpForm
from BookiernesApp.models import *


@login_required
def mainView(request):
    user = User.objects.get(username=request.user.username)
    if user.user_type == 'writer':
        return redirect('BookiernesApp:writer_published_books')
    elif user.user_type == 'editor':
        return redirect('BookiernesApp:signup')
    pass


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'forms/form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('BookiernesApp:home')
