from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView

from BookiernesApp.decorators import mainEditor_required, book_presented
from BookiernesApp.models import *


@method_decorator([login_required, mainEditor_required], name='dispatch')
class MainEditorBooksPresentedInEditorial(ListView):

    model = Book
    template_name = 'html_templates/MainEditor/MainEditor_PresentedBooks.html'
    #paginate_by = 100  # if pagination is desired


@method_decorator([login_required, mainEditor_required, book_presented], name='dispatch')
class MainEditorBookPresentedDetail(DetailView):

    model = Book
    template_name = 'html_templates/MainEditor/MainEditor_DetailPresentedBook.html'


@login_required
@mainEditor_required
def assign_or_reject(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.POST['action'] == 'assign':
        #Find editors with the same theme as the book
        possible_users = User.objects.all().filter(editor_profile__assigned_theme=book.theme)
        if not possible_users:
            return redirect('BookiernesApp:maineditor_books_presented_editorial')  #TODO test print error message, no users found with this theme
        #Find the least busy worker
        available_user = list(possible_users)[0]
        for user in possible_users:
            if available_user != user and user.editor_profile.get_availability() < available_user.editor_profile.get_availability():
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
