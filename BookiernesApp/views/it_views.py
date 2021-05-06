from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib import messages
from django.contrib.messages import constants

from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.conf import settings

from datetime import datetime
import os
from os import remove, rmdir
from shutil import rmtree

from BookiernesApp.decorators import it_required
from BookiernesApp.models import User , AbstractUser



#@method_decorator([login_required, it_required], name='dispatch')
class ItView(ListView):
    template_name = 'html_templates/IT/It_UserList.html'
    model = User
    paginate_by = 10

    def get_queryset(self):
        try:
            return User.objects.exclude(user_type = "subscribed_reader").exclude(username="admin")
        except:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_user_count'] = User.objects.exclude(user_type="subscribed_reader").exclude(
            username="admin").count()
        return context


#@method_decorator([login_required, it_required], name='dispatch')
class ItDetailUser(TemplateView):
    template_name = 'html_templates/IT/It_DadesUser.html'


    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['obj_user_count'] = User.objects.exclude(user_type = "subscribed_reader").exclude(username="admin").count()
            context['obj_user'] = User.objects.get(id=self.kwargs['pk'])
            return context
        except:
            raise Http404("I can't access this page.")


def active_user(request, pk):
    try:
        obj_user=User.objects.get(id = pk)
        message= ""
        url="BookiernesApp:user_list"

        if obj_user.is_active == 1:
            obj_user.is_active=0
            message = "El usuario %(nom)s se desactivado corectamente. " % {'nom': obj_user.username}
        else:
            obj_user.is_active = 1
            message = "El usuario %(nom)s se activo corectamente. " % {'nom': obj_user.username}

        obj_user.save()


        messages.add_message(request, constants.SUCCESS, message)

        return redirect(url)

    except:
        raise Http404("I can't access this page.")



