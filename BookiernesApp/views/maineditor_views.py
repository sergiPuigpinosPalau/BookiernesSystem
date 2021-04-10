from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from BookiernesApp.decorators import mainEditor_required
from BookiernesApp.models import *


@method_decorator([login_required, mainEditor_required], name='dispatch')
class MainEditorBooksPresentedInEditorial(ListView):

    model = Book
    template_name = 'html_templates/MainEditor/MainEditor_PresentedBooks.html'
    #paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all().filter(book_status="presented")
        return context
