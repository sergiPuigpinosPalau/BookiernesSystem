from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import Http404
from django.shortcuts import render , redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime

from BookiernesApp.decorators import editor_required
from BookiernesApp.models import Book, User, Writer, Notification , Message, NotificationTable



@method_decorator([login_required, editor_required], name='dispatch')
class EditorBookRevision(TemplateView):
    template_name = 'html_templates/Editor/Editor_LibrosARevisa.html'


@method_decorator([login_required, editor_required ], name='dispatch')
class Editor_Chat_Book(TemplateView):
    model = Book
    template_name = 'html_templates/Editor/Chat.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['book_numbers'] = Book.objects.count()

            book = Book.objects.get( Q(pk=self.kwargs['pk']))
            if ((book.assigned_to == None and book.author == None) or book.assigned_to.id != self.request.user.id ) :
                raise Http404("I can't access this page.")

            context['book'] = book
            #book.assigned_to
            messages = Message.objects.filter(Q(book_id=book.id)  & Q( Q( Q(user_id =self.request.user.id ) &  Q(destination_user_id =book.author.user.pk) )  | Q( Q(user_id = book.author.user.pk ) &  Q(destination_user_id =self.request.user.id) ) ) )
           
            context['messages']=messages
            context['messages_numbers']=messages.count()
            return context
        except:
            raise Http404("I can't access this page.")
@login_required
@editor_required
def editor_post_chat(request, pk):
    model = Book
    template_name = 'html_templates/MainEditor/Chat.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            notification=NotificationTable.objects.filter(destination_user_id = self.request.user.id )
            context['notification_numbers'] = notification.count()
            context['notifications'] = notification
            context['book_numbers'] = Book.objects.count()
            book = Book.objects.get( Q(pk=self.kwargs['pk']))

            if ((book.assigned_to == None and book.author == None) or book.assigned_to.id != self.request.user.id ) :
                raise Http404("I can't access this page.")

            context['book'] = book
            #book.assigned_to
            messages = Message.objects.filter(Q(book_id=book.id)  & Q( Q( Q(user_id =self.request.user.id ) &  Q(destination_user_id =book.author.user.pk) )  | Q( Q(user_id = book.author.user.pk ) &  Q(destination_user_id =self.request.user.id) ) ) )
           
            context['messages']=messages
            context['messages_numbers']=messages.count()
            return context
        except:
            raise Http404("I can't access this page.")


@login_required
@editor_required
def maineditor_post_chat(request, pk):
    
    if request.method == "POST":
        content = request.POST['content']
        date_received = datetime.now()
        book_id = pk
        user_id = request.user.id
        destination_user_id = Book.objects.get(id=pk).author.user.pk

        if destination_user_id == None:
            raise Http404("I can't access this page.")

        #try:
        message=Message.objects.create(content= content,date_received=date_received,book_id=book_id,user_id=user_id,destination_user_id=destination_user_id )
        message.save()
            
        notification=NotificationTable.objects.create(notification_id= 2 ,date_received=date_received,user_id=user_id,destination_user_id=destination_user_id)
        notification.save()
        #except:
        #    raise Http404("Sa producido un error a la bbdd.")

        url='/maineditor_message/get_book/'+pk
        return redirect(url)
    else:
        raise Http404("I can't access this page.")