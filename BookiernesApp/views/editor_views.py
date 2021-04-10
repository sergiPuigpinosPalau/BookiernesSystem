from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from BookiernesApp.decorators import editor_required

#
# @method_decorator([login_required, editor_required], name='dispatch')
# class EditorBookRevision(TemplateView):
#     template_name = 'html_templates/Editor/Editor_BooksToRevise.html'
from BookiernesApp.models import *


class EditorBookRevision(ListView):

    model = Book
    template_name = 'html_templates/Editor/Editor_BooksToRevise.html'
    #paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context['book_list'] = Book.objects.all().filter(book_status="revised", assigned_to__user=user)
        context['user_type'] = user.user_type
        return context
