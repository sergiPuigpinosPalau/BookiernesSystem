from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import TemplateView
from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime

from BookiernesApp.decorators import editor_required, book_in_revision

from BookiernesApp.models import *
from BookiernesApp.decorators import editor_required
from BookiernesApp.models import Book, User, Writer, Notification, Message


@method_decorator([login_required, editor_required], name='dispatch')
class EditorBookRevision(ListView):
    model = Book
    template_name = 'html_templates/Editor/Editor_BooksToRevise.html'
    # paginate_by = 100  # if pagination is desired


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
    # Redirect
    return redirect('BookiernesApp:editor_book_revision')


@method_decorator([login_required, editor_required], name='dispatch')
class Editor_Chat_Book(TemplateView):
    model = Book
    template_name = 'html_templates/Editor/Chat.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            notification = Notification.objects.filter(destination_user_id=self.request.user.id)
            context['notification_numbers'] = notification.count()
            context['notifications'] = notification
            context['book_numbers'] = Book.objects.count()
            book = Book.objects.get(Q(pk=self.kwargs['pk']))

            if ((book.assigned_to == None and book.author == None) or book.assigned_to.user.id != self.request.user.id):
                raise Http404("I can't access this page.")

            context['book'] = book
            # book.assigned_to
            messages = Message.objects.filter(Q(book_id=book.id) & Q(
                Q(Q(user_id=self.request.user.id) & Q(destination_user_id=book.author.user.id)) | Q(
                    Q(user_id=book.author.user.id) & Q(destination_user_id=self.request.user.id))))

            context['messages'] = messages
            context['messages_numbers'] = messages.count()
            return context
        except:
            raise Http404("I can't access this page.")


@login_required
@editor_required
def editor_post_chat(request, pk):
    if request.method == "POST":
        content = request.POST['content']
        date_received = datetime.now()
        book_id = pk
        user_id = request.user.id
        destination_user_id = Book.objects.get(id=pk).author.user.pk
        notification_type = 'message'
        content_notification = 'Has recibido un mensaje.'
        url = 'maineditor_message/get_book/' + book_id

        if destination_user_id == None:
            raise Http404("I can't access this page.")
        try:
            message = Message.objects.create(content=content, date_received=date_received, book_id=book_id,
                                             user_id=user_id, destination_user_id=destination_user_id)
            message.save()

            notification = Notification.objects.create(notification_type=notification_type,
                                                       content=content_notification, url=url,
                                                       date_received=date_received, user_id=user_id,
                                                       destination_user_id=destination_user_id)
            notification.save()
        except:
            raise Http404("Sa producido un error a la bbdd.")

        url = '/editor_message/get_book/' + pk
        return redirect(url)
    else:
        raise Http404("I can't access this page.")


@login_required
@editor_required
def editor_notification(request, pk):
    if pk != None:
        try:
            notification = Notification.objects.get(Q(id=pk) & Q(destination_user_id=request.user.id))
            url = notification.url
            if request.user.user_type == 'editor':
                notification.delete()
                return redirect(url)

        except:
            raise Http404("Sa producido un error a la bbdd.")

    else:
        raise Http404("I can't access this page.")
