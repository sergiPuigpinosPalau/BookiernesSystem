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

from BookiernesApp.decorators import it_required
from BookiernesApp.forms import FormularioUsuario

from BookiernesApp.models import User, Theme


@method_decorator([login_required, it_required], name='dispatch')
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


@method_decorator([login_required, it_required], name='dispatch')
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

@method_decorator([login_required, it_required], name='dispatch')
class ITCrateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'html_templates/IT/It_CreateUser.html'
    form_class = FormularioUsuario
    success_url = reverse_lazy('BookiernesApp:user_list')

    def get_success_message(self, cleaned_data):
        return "L'usuari %(name)s s'ha creat correctament. " % {'name': self.object.username}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_user_count'] = User.objects.exclude(user_type="subscribed_reader").exclude(
            username="admin").count()
        context['Theme'] = Theme.objects.all()
        return context

@method_decorator([login_required, it_required], name='dispatch')
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
            raise Http404("No puc accedir a aquesta pàgina.")


@login_required
@it_required
def postEditPass(request):
    if request.method == "POST":

        message = ""
        ok=0
        id = request.POST['pk']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        obj_user = User.objects.get(id=id)

        if pass1 != pass2 or (len(pass1)<8 and len(pass2)<8):
            message = "La contrasenya ha de tenir 8 caràcters i els dos camps han de ser iguals. "
        else:
            message = "A l'usuari %(nom)s se li ha canviat la contrasenya. " % {'nom': obj_user.username}
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
        raise Http404("No puc accedir a aqueta pàgina.")


@method_decorator([login_required, it_required], name='dispatch')
class ViewResetPass(TemplateView):
    template_name = 'html_templates/IT/It_PeticonCabio.html'

@login_required
@it_required
def resetPass(request):
    return redirect("/")

@login_required
@it_required
def active_user(request, pk):
    try:
        obj_user=User.objects.get(id = pk)
        message= ""
        url="BookiernesApp:user_list"

        if obj_user.is_active == 1:
            obj_user.is_active=0
            message = "L'usuari %(nom)s s'ha desactivat correctament. " % {'nom': obj_user.username}
        else:
            obj_user.is_active = 1
            message = "L'usuari %(nom)s s'ha activat correctament. " % {'nom': obj_user.username}

        obj_user.save()


        messages.add_message(request, constants.SUCCESS, message)

        return redirect(url)

    except:
        raise Http404("No puc accedir a aquesta pàgina")



