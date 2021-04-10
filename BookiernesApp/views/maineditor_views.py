from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from BookiernesApp.decorators import mainEditor_required
from BookiernesApp.models import *

#
# @method_decorator([login_required, mainEditor_required], name='dispatch')
# class MainEditorBookRevision(TemplateView):
#     template_name = 'html_templates/MainEditor/MainEditor_LibrosARevisa.html'


def MainEditorBookRevision(request):
    book_list = Book.objects.filter(book_status="presented")
    template = loader.get_template('html_templates/MainEditor/MainEditor_LibrosARevisa.html')
    context = {
        'book_list': book_list,
    }
    return HttpResponse(template.render(context, request))
