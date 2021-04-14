from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import Http404
from django.shortcuts import render , redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin

from datetime import datetime

from BookiernesApp.decorators import mainEditor_required 
from BookiernesApp.models import Book, User, Writer, Editor, Notification , Message 

@method_decorator([login_required, mainEditor_required], name='dispatch')
class MainEditorBookRevision(TemplateView):
    template_name = 'html_templates/MainEditor/MainEditor_LibrosARevisa.html'


@method_decorator([login_required, mainEditor_required ], name='dispatch')
class Maineditor_Chat_Book(TemplateView):
    model = Book
    template_name = 'html_templates/MainEditor/Chat.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            notification=Notification.objects.filter(destination_user_id = self.request.user.id )
            context['notification_numbers'] = notification.count()
            context['notifications'] = notification
            context['book_numbers'] = Book.objects.count()
            book = Book.objects.get( Q(pk=self.kwargs['pk']))

            if ((book.assigned_to == None and book.author == None) or book.assigned_to.user.id != self.request.user.id ) :
                raise Http404("I can't access this page.")

            context['book'] = book
            #book.assigned_to
            messages = Message.objects.filter(Q(book_id=book.id)  & Q( Q( Q(user_id =self.request.user.id ) &  Q(destination_user_id =book.author.user.id) )  | Q( Q(user_id = book.author.user.id ) &  Q(destination_user_id =self.request.user.id) ) ) )
           
            context['messages']=messages
            context['messages_numbers']=messages.count()
            return context
        except:
            raise Http404("I can't access this page.")

@login_required
@mainEditor_required
def maineditor_post_chat(request, pk):
    
    if request.method == "POST":
        content = request.POST['content']
        date_received = datetime.now()
        book_id = pk
        user_id = request.user.id
        destination_user_id = Book.objects.get(id=pk).author.user.pk
        notification_type = 'message'
        content_notification = 'Has recibido un mensaje.'
        url = '/writer_message/get_book/'+book_id

        if destination_user_id == None:
            raise Http404("I can't access this page.")
        try:
            message=Message.objects.create(content= content,date_received=date_received,book_id=book_id,user_id=user_id,destination_user_id=destination_user_id )
            message.save()
            

            notification=Notification.objects.create(notification_type = notification_type, content = content_notification, url = url ,date_received=date_received,user_id=user_id,destination_user_id=destination_user_id)
            notification.save()
        except:
            raise Http404("Sa producido un error a la bbdd.")

        url='/maineditor_message/get_book/'+pk
        return redirect(url)
    else:
        raise Http404("I can't access this page.")

@login_required
@mainEditor_required
def maineditor_notification(request, pk):
    if pk != None:
        try:
            notification=Notification.objects.get( Q(id=pk ) & Q(destination_user_id=request.user.id) )
            url = notification.url
            if  request.user.user_type == 'main_editor':
                notification.delete()
                return redirect(url)

        except:
            raise Http404("Sa producido un error a la bbdd.")
        
    else:
        raise Http404("I can't access this page.")