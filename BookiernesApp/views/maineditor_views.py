from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from BookiernesApp.decorators import mainEditor_required
from BookiernesApp.models import *

#
# @method_decorator([login_required, mainEditor_required], name='dispatch')
# class MainEditorBookRevision(TemplateView):
#     template_name = ''

#
# def MainEditorBookRevision(request):
#     book_list = Book.objects.filter(book_status="presented")
#     template = loader.get_template('html_templates/MainEditor/MainEditor_PresentedBooks.html')
#     context = {
#         'book_list': book_list,
#     }
#     return HttpResponse(template.render(context, request))

class MainEditorBookRevision(ListView):

    model = Book
    template_name = ''
    #paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context['book_list'] = Book.objects.all().filter(book_status="revised", assigned_to__user=user)
        return context
