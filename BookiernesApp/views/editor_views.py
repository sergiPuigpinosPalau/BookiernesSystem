from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView

from BookiernesApp.decorators import editor_required, book_in_revision

from BookiernesApp.models import *


@method_decorator([login_required, editor_required], name='dispatch')
class EditorBookRevision(ListView):

    model = Book
    template_name = 'html_templates/Editor/Editor_BooksToRevise.html'
    #paginate_by = 100  # if pagination is desired


#TODO filepath to some folder
#TODO check if filter(,) is an AND or an OR
@method_decorator([login_required, editor_required, book_in_revision], name='dispatch')
class EditorBookDetail(DetailView):

    model = Book
    template_name = 'html_templates/Editor/Editor_DetailBookToRevise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        if book.new_book_version:
            context['latest_book'] = book.new_book_version
        else:
            context['latest_book'] = book
        return context


@login_required
@editor_required
def accept_or_reject(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.POST['action'] == 'accept':
        book.book_status = 'accepted'
    elif request.POST['action'] == 'reject':
        book.book_status = 'rejected'
        book.main_editor_comment = request.POST['editor_rejected_comment']
    book.save()
    #Redirect
    return redirect('BookiernesApp:editor_book_revision')
