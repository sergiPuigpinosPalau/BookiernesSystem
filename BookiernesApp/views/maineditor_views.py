from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from BookiernesApp.decorators import mainEditor_required


@method_decorator([login_required, mainEditor_required], name='dispatch')
class MainEditorBookRevision(TemplateView):
    template_name = 'html_templates/MainEditor/MainEditor_LibrosARevisa.html'
