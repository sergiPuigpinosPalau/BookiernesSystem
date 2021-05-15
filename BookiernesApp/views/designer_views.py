from datetime import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.core.files.storage import FileSystemStorage

from django.contrib import messages
from django.contrib.messages import constants


#@method_decorator([login_required, designer_required], name='dispatch')
from BookiernesApp.models import ImagePetition, User, Book, GraphicDesigner, Notification


class AssignmentListImg(ListView):
    template_name = 'html_templates/Designer/Main/Designer_AssignmentListImg.html'
    model = ImagePetition
    paginate_by = 10

    def get_queryset(self):
        try:
            return ImagePetition.objects.filter(graphic_designer_id__isnull=True)
        except:
            return 0


class AssignmentDetaliImg(DetailView):
    model = ImagePetition
    template_name = 'html_templates/Designer/Main/Main_Designer_DetailImg.html'



class AssignmentListBockMaquetat(ListView):
    template_name = 'html_templates/Designer/Main/Designer_AssignmentListBockMaquetat.html'
    model = Book
    paginate_by = 10

    def get_queryset(self):
        try:
            return Book.objects.filter(designer_assigned_to_id__isnull=True).filter(book_status='designing')
        except:
            return 0


class AssignmentDetaliBockMaquetat(DetailView):
    model = Book
    template_name = 'html_templates/Designer/Main/Main_Designer_DetailBockMaquetat.html'



# disenador



class ListImg(ListView):
    template_name = 'html_templates/Designer/Designer_ListImg.html'
    model = ImagePetition
    paginate_by = 10

    def get_queryset(self):
        try:
            return ImagePetition.objects.filter(graphic_designer_id=GraphicDesigner.objects.get(user_id=self.request.user.id).id)
        except:
            return 0


class DetaliImg(DetailView):
    model = ImagePetition
    template_name = 'html_templates/Designer/Designer_DetailImg.html'



class ListBockMaquetat(ListView):
    template_name = 'html_templates/Designer/Designer_ListBockMaquetat.html'
    model = Book
    paginate_by = 10

    def get_queryset(self):
        try:
            return Book.objects.filter(designer_assigned_to_id=GraphicDesigner.objects.get(user_id=self.request.user.id).id).filter(book_status='designing')
        except:
            return 0


class DetaliBockMaquetat(DetailView):
    model = Book
    template_name = 'html_templates/Designer/Designer_DetailBockMaquetat.html'


def uploadbook(request, pk):
    if pk != None:
        if request.method == 'POST':

            book_designed = request.FILES["book_designed"]
            book = Book.objects.get(id=pk)

            date_received = datetime.now()
            user_id = request.user.id
            destination_user_id = Book.objects.get(id=pk).assigned_to.user.id

            notification_type = 'presented_book_designed'
            content_notification = 'He realizado la maquetacion del libro  %(title)s .'% {'title': book.title}
            url='#' #TODO poner la url del destino.

            if book.book_designed == None:
                fs = FileSystemStorage()
                book.book_designed = book_designed.name
                path = 'book_designed/' + str(book_designed.name)
                fs.save(path, book_designed)
                book.save()
            else:
                fs = FileSystemStorage()
                path = 'book_designed/' + str(book.book_designed)
                fs.delete(path)
                book.book_designed = book_designed.name
                path = 'book_designed/' + str(book_designed.name)
                fs.save(path, book_designed)
                book.save()

            message = "El libro maquetado %(title)s se subio corectamente. " % {'title': book.title}
            messages.add_message(request, constants.SUCCESS, message)

            if not Notification.objects.all().filter(notification_type=notification_type, destination_user_id__exact=destination_user_id, user_id__exact=user_id, url__exact=url):
                notification = Notification.objects.create(notification_type=notification_type,
                                                           content=content_notification, url=url,
                                                           date_received=date_received, user_id=user_id,
                                                           destination_user_id=destination_user_id)
                notification.save()

            return redirect('BookiernesApp:bockmaquetat_list')

    else:
        raise Http404("I can't access this page.")


