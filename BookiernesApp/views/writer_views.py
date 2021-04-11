from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView
from django.shortcuts import render , redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.http import HttpResponse, Http404


from BookiernesApp.decorators import writer_required
from BookiernesApp.models import Book, User, Writer, Notification
from BookiernesApp.forms.book_forms import *


@method_decorator([login_required, writer_required], name='dispatch')
class PublishedBooks(TemplateView):
    template_name = 'html_templates/Escriptor/Escriptor_LibrosPresentados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_numbers'] = Book.objects.count()
        context['books'] = Book.objects.filter(author_id = Writer.objects.get(user_id=self.request.user.id ).id)
        #etc
        return context


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
        context['book_numbers'] = Book.objects.count()
        #context['notification_numbers'] = Notification.objects.filter(self.request.user.id).cont()
        return context
    
    def get_success_message(self, cleaned_data):
        return "El libro %(title)s se presento corectamente. " % {'title': self.object.title}

    #def form_valid(self, form):
        # guardar en la taula noticias

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
            author = Writer.objects.get(user_id=self.request.user.id )
            book = Book.objects.get(Q(author_id=author) & Q(pk=self.kwargs['pk']))
            context['book'] = book
            if book.assigned_to == None:
                raise Http404("I can't access this page.")
            context['book_numbers'] = Book.objects.count()
            book_path=str(book.path).split("/")
            context['path'] = book_path[len(book_path)-1]
            return context
        except:
            raise Http404("I can't access this page.")

    def get_success_message(self, cleaned_data):
        return "El libro %(title)s se re-entrego corectamente. " % {'title': self.object.title}


class Get_Books(TemplateView):
    model = Book
    template_name = 'html_templates/Escriptor/Escriptor_LibroConcreto.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['book_numbers'] = Book.objects.count()
            author =Writer.objects.get(user_id=self.request.user.id ).id
            context['book'] = Book.objects.get(Q(author_id=author) & Q(pk=self.kwargs['pk']))
            return context
        except:
            raise Http404("I can't access this page.")



        

