from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.http import Http404

from datetime import datetime

from BookiernesApp.decorators import writer_required
from BookiernesApp.models import Book, User, Writer, Notification, Message
from BookiernesApp.forms.book_forms import *


@method_decorator([login_required, writer_required], name='dispatch')
class PublishedBooks(TemplateView):
    template_name = 'html_templates/Escriptor/Escriptor_LibrosPresentados.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     notification = Notification.objects.filter(destination_user_id=self.request.user.id)
    #     self.request.user.writer_profile.get_presented_books()
    #     context['notification_numbers'] = notification.count()
    #     context['notifications'] = notification
    #     context['book_numbers'] = Book.objects.count()
    #     context['books'] = Book.objects.filter(author_id=Writer.objects.get(user_id=self.request.user.id).id)
    #     # etc
    #     return context


@method_decorator([login_required, writer_required], name='dispatch')
class PublishBook(SuccessMessageMixin, CreateView):
    model = Book
    template_name = 'html_templates/Escriptor/Escriptor_PresentaLibro.html'
    form_class = Present_Book
    success_url = '/writer_published'

    def get_initial(self, *args, **kwargs):
        initial = super(PublishBook, self).get_initial(**kwargs)
        author = Writer.objects.get(user_id=self.request.user.id)
        initial['author'] = author.id
        initial['book_status'] = 'presented'
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notification = Notification.objects.filter(destination_user_id=self.request.user.id)
        context['notification_numbers'] = notification.count()
        context['notifications'] = notification
        context['book_numbers'] = Book.objects.count()
        return context

    def get_success_message(self, cleaned_data):
        return "El libro %(title)s se presento corectamente. " % {'title': self.object.title}

    # def form_valid(self, form):
    # guardar en la taula noticias


@method_decorator([login_required, writer_required], name='dispatch')
class Edit_Book(SuccessMessageMixin, UpdateView):
    model = Book
    template_name = 'html_templates/Escriptor/Escriptor_LibroModifca.html'
    form_class = Edit_Book

    def get_success_url(self, **kwargs):
        return reverse('BookiernesApp:writer_modify_a_book', kwargs={'pk': self.object.id})

    def get_initial(self, *args, **kwargs):
        initial = super(Edit_Book, self).get_initial(**kwargs)
        initial['book_status'] = 'modifying'
        return initial

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            author = Writer.objects.get(user_id=self.request.user.id)
            book = Book.objects.get(Q(author_id=author) & Q(pk=self.kwargs['pk']))
            notification = Notification.objects.filter(destination_user_id=self.request.user.id)
            context['notification_numbers'] = notification.count()
            context['notifications'] = notification

            if book.assigned_to == None:
                raise Http404("I can't access this page.")
            context['book'] = book
            context['book_numbers'] = Book.objects.count()
            book_path = str(book.path).split("/")
            context['path'] = book_path[len(book_path) - 1]
            return context
        except:
            raise Http404("I can't access this page.")

    def get_success_message(self, cleaned_data):
        return "El libro %(title)s se re-entrego corectamente. " % {'title': self.object.title}


@method_decorator([login_required, writer_required], name='dispatch')
class Get_Books(TemplateView):
    model = Book
    template_name = 'html_templates/Escriptor/Escriptor_LibroConcreto.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['book_numbers'] = Book.objects.count()
            notification = Notification.objects.filter(destination_user_id=self.request.user.id)
            context['notification_numbers'] = notification.count()
            context['notifications'] = notification
            author = Writer.objects.get(user_id=self.request.user.id).id
            context['book'] = Book.objects.get(Q(author_id=author) & Q(pk=self.kwargs['pk']))
            return context
        except:
            raise Http404("I can't access this page.")


@method_decorator([login_required, writer_required], name='dispatch')
class Chat_Book(TemplateView):
    model = Book
    template_name = 'html_templates/Escriptor/Chat.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['book_numbers'] = Book.objects.count()
            notification = Notification.objects.filter(destination_user_id=self.request.user.id)
            context['notification_numbers'] = notification.count()
            context['notifications'] = notification
            author = Writer.objects.get(user_id=self.request.user.id).id
            book = Book.objects.get(Q(author_id=author) & Q(pk=self.kwargs['pk']))
            if book.assigned_to == None and book.author != self.request.user.id:
                raise Http404("I can't access this page.")

            context['book'] = book
            # book.assigned_to
            messages = Message.objects.filter(Q(book_id=book.id) & Q(
                Q(Q(user_id=self.request.user.id) & Q(destination_user_id=book.assigned_to.user.id)) | Q(
                    Q(user_id=book.assigned_to.user.id) & Q(destination_user_id=self.request.user.id))))
            context['messages'] = messages
            context['messages_numbers'] = messages.count()
            return context
        except:
            raise Http404("I can't access this page.")


@login_required
@writer_required
def post_chat(request, pk):
    if request.method == "POST":
        content = request.POST['content']
        date_received = datetime.now()
        book_id = pk
        user_id = request.user.id
        destination_user_id = Book.objects.get(id=pk).assigned_to.user.id

        notification_type = 'message'
        content_notification = 'Has recibido un mensaje.'
        if User.objects.get(id=destination_user_id).user_type == "editor":
            url = '/editor_message/get_book/' + book_id
        elif User.objects.get(id=destination_user_id).user_type == "main_editor":
            url = '/maineditor_message/get_book/' + book_id

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

        url = '/writer_message/get_book/' + pk
        return redirect(url)
    else:
        raise Http404("I can't access this page.")


@login_required
@writer_required
def writer_notification(request, pk):
    if pk != None:
        # try:
        # notification=Notification.objects.get( Q(id=pk ) & Q(destination_user_id=request.user.id) )
        notification = Notification.objects.all().filter(pk=pk, destination_user_id__exact=request.user.id)
        url = notification.url
        if request.user.user_type == 'writer':
            notification.delete()
            return redirect(url)

        # except:
        #    raise Http404("Sa producido un error a la bbdd.")

    else:
        raise Http404("I can't access this page.")
