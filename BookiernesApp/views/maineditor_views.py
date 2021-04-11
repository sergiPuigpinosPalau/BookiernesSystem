from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView

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


@method_decorator([login_required, mainEditor_required], name='dispatch')
class MainEditorBookPresentedDetail(DetailView):

    model = Book
    template_name = 'html_templates/MainEditor/MainEditor_DetailPresentedBook.html'
    #paginate_by = 100  # if pagination is desired


#TODO mirar comentari queda guardat entre <p>??
@login_required
@mainEditor_required
def assign_or_reject(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.POST['action'] == 'assign':
        #Find editors with the same theme as the book
        possible_users = User.objects.all().filter(editor_profile__assigned_theme=book.theme)
        if not possible_users:
            print("BRUH")#TODO print error message, no users found with this theme
            return
        #Find the least busy worker
        available_user = list(possible_users)[0]
        for user in possible_users:
            if user.editor_profile.books_assigned.count() < available_user.editor_profile.books_assigned.count():
                available_user = user
        #Modify book attributes
        book.assigned_to = available_user.editor_profile
        book.book_status = 'revised'
        book.main_editor_comment = request.POST['maineditor_approved_comment']
    elif request.POST['action'] == 'reject':
        book.book_status = 'rejected'
        book.main_editor_comment = request.POST['maineditor_rejected_comment']
    book.save()
    #Redirect
    return redirect('BookiernesApp:maineditor_books_presented_editorial')
