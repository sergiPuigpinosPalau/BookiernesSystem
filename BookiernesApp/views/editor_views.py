from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from BookiernesApp.decorators import editor_required


@method_decorator([login_required, editor_required], name='dispatch')
class EditorBookRevision(TemplateView):
    template_name = 'html_templates/Editor/Editor_BooksToRevise.html'
