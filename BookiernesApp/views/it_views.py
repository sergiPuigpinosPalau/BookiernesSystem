from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib import messages
from django.contrib.messages import constants

from django.urls import  reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.conf import settings




from BookiernesApp.forms import FormularioUsuario

from BookiernesApp.models import User



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
    model = User
    template_name = 'html_templates/IT/It_DadesUser.html'


    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['obj_user_count'] = User.objects.exclude(user_type = "subscribed_reader").exclude(username="admin").count()
            context['obj_user'] = User.objects.get(id=self.kwargs['pk'])
            return context
        except:
            raise Http404("I can't access this page.")

class ITCrateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'html_templates/IT/It_CreateUser.html'
    form_class = FormularioUsuario
    success_url = reverse_lazy('BookiernesApp:user_list')

    def get_success_message(self, cleaned_data):
        return "El usuario %(name)s se creo corectamente. " % {'name': self.object.username}


class ItPassword(TemplateView):
    template_name = 'html_templates/IT/ItEditPassword.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['obj_user_count'] = User.objects.exclude(user_type="subscribed_reader").exclude(
                username="admin").count()
            context['obj_user'] = User.objects.get(id=self.kwargs['pk'])
            return context
        except:
            raise Http404("I can't access this page.")

def postEditPass(request):
    if request.method == "POST":

        message = ""
        ok=0
        id = request.POST['pk']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        obj_user = User.objects.get(id=id)

        if pass1 != pass2 or (len(pass1)<8 and len(pass2)<8):
            message = "La contraseña debe tenr 8 caracteres y los dos capos debe ser iguales. "
        else:
            message = "El usuario %(nom)s se le cabio la contraseña. " % {'nom': obj_user.username}
            ok = 1



        if ok == 1:
            messages.add_message(request, constants.SUCCESS, message)
            obj_user.set_password(pass2)
            obj_user.save()
            return redirect("BookiernesApp:user_list")
        else:
            messages.add_message(request, constants.ERROR, message)
            url = "/it_view/edit_pass/" + str(obj_user.id)
            return redirect(url)

    else:
        raise Http404("I can't access this page.")



class ViewResetPass(TemplateView):
    template_name = 'html_templates/IT/It_PeticonCabio.html'

def resetPass(request):
    return redirect("/")


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



