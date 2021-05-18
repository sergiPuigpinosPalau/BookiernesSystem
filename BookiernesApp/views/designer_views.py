from datetime import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.core.files.storage import FileSystemStorage

from django.contrib import messages
from django.contrib.messages import constants


#@method_decorator([login_required, designer_required], name='dispatch')
from BookiernesApp.models import ImagePetition, User, Book, GraphicDesigner, Notification, Image, Message


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = '0'
        context['users'] = User.objects.filter(Q(user_type = "graphic_designer") | Q(user_type = "main_graphic_designer")  )
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = '1'
        context['users'] = User.objects.filter(Q(user_type = "graphic_designer") | Q(user_type = "main_graphic_designer")  )
        return context


def asignarGraphicDesigner(request):

    if request.method == 'POST':

        notification_type = 'to_assign'
        content_notification=""
        url=""
        date_received = datetime.now()
        user_id = request.user.id
        destination_user = GraphicDesigner.objects.get(user_id=int(request.POST["graphic_designer"])).user_id
        url_redirect=""

        graphic_designer = GraphicDesigner.objects.get(user_id=int(request.POST["graphic_designer"]))
        comment = request.POST["comment"]
        pk = request.POST["pk"]
        type = request.POST["type"]

        if type == "1" :
            url_redirect='BookiernesApp:main_bockmaquetat_list'
            book = Book.objects.get(id=pk)

            book.designer_assigned_to_id=graphic_designer
            book.main_graphic_designer_comment=comment
            book.save()

            destination_user = Book.objects.get(id=pk).designer_assigned_to.user


            content_notification = 'Te he asignado el libro  %(title)s .' % {'title': book.title }
            url = '/graphic_designer/bockmaquetat/'

            message = "El libro maquetado %(title)s se asigno corectamente." % {'title': book.title }
            messages.add_message(request, constants.SUCCESS, message)

        elif type == "0" :
            url_redirect = 'BookiernesApp:main_petitionview_list'
            img = ImagePetition.objects.get(id=pk)

            img.graphic_designer = graphic_designer
            img.main_graphic_designer_comment = comment
            img.save()

            destination_user = ImagePetition.objects.get(id=pk).editor.user

            content_notification = 'Te he asignado el la solicitut de imagenes %(title)s .' % {'title': img.title}
            url = '/graphic_designer/petitionview/'

            message = "La solicitut de imagenes %(title)s se asigno . " % {'title': img.title }
            messages.add_message(request, constants.SUCCESS, message)


        if not Notification.objects.all().filter(notification_type=notification_type,
                                                     destination_user_id__exact=destination_user.id,
                                                     user_id__exact=user_id, url__exact=url):
            notification = Notification.objects.create(notification_type=notification_type,
                                                           content=content_notification, url=url,
                                                           date_received=date_received, user_id=user_id,
                                                           destination_user_id=destination_user.id)
            notification.save()


        return redirect(url_redirect)


    else:
        raise Http404("I can't access this page.")



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

def uploadimg(request):

    if request.method == 'POST':

        files = [request.FILES.get('file[%d]' % i)
                 for i in range(0, len(request.FILES))]

        id = request.POST['id']
        obj_imagePetition=ImagePetition.objects.get(id=id).title
        date_received = datetime.now()
        user_id = request.user.id
        destination_user_id = Book.objects.get(id=id).assigned_to.user.id

        notification_type = 'presented_img'
        content_notification = 'He subido las fotos de la solicitut de imagenes   %(title)s .' % {'title': obj_imagePetition}
        url = '/editor_image_petitions/image_petition_detail/'+id

        fs = FileSystemStorage()
        for f in files:
            path = 'images/' + str(f.name)
            fs.save(path, f)
            image = Image(path=f.name, petition_id = id )
            image.save()

        message = "La Fotos de la Solictudes de Imágenes %(title)s se subio todas corectamente. " % {'title': obj_imagePetition}
        messages.add_message(request, constants.SUCCESS, message)

        if not Notification.objects.all().filter(notification_type=notification_type,
                                                 destination_user_id__exact=destination_user_id, user_id__exact=user_id,
                                                 url__exact=url):
            notification = Notification.objects.create(notification_type=notification_type,
                                                       content=content_notification, url=url,
                                                       date_received=date_received, user_id=user_id,
                                                       destination_user_id=destination_user_id)
            notification.save()

        return redirect('BookiernesApp:bockmaquetat_list')

        data = {'status': 'success'}
        response = JsonResponse(data)
        return response
    else:
        raise Http404("I can't access this page.")


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
            url='/editor_books_to_design/book_design_detail/' +pk

            if book.book_designed == None or book.book_designed=='':
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
    else:
        raise Http404("I can't access this page.")


def designer_notification(request, pk):
    if pk != None:
        try:

            notification=Notification.objects.get( Q(id=pk ) & Q(destination_user_id=request.user.id) )
            url = notification.url
            notification.delete()
            return redirect(url)

        except:
           raise Http404("Sa producido un error a la bbdd.")

    else:
        raise Http404("I can't access this page.")



class Graphic_designer_Chat_Book(TemplateView):
    model = Book
    template_name = 'html_templates/Designer/Chat.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            graphicdesigne = GraphicDesigner.objects.get(user_id=self.request.user.id).id
            book = Book.objects.get(Q(designer_assigned_to_id=graphicdesigne) & Q(pk=self.kwargs['pk']))
            if book.designer_assigned_to == None :
                raise Http404("I can't access this page.")

            context['book'] = book
            messages = Message.objects.filter(Q(book_id=book.id) & Q(
                Q(Q(user_id=self.request.user.id) & Q(destination_user_id=book.assigned_to.user.id)) | Q(
                    Q(user_id=book.assigned_to.user.id) & Q(destination_user_id=self.request.user.id))))
            context['messages'] = messages
            context['messages_numbers'] = messages.count()
            return context
        except:
            raise Http404("I can't access this page.")


def graphic_designer_post_chat(request, pk):
    if request.method == "POST":
        content = request.POST['content']
        date_received = datetime.now()
        book_id = pk
        user_id = request.user.id
        destination_user_id = Book.objects.get(id=pk).assigned_to.user.id

        notification_type = 'message'
        content_notification = 'Has recibido un mensaje.'

        if User.objects.get(id=destination_user_id).user_type == "editor" or User.objects.get(id=destination_user_id).user_type == "main_editor":
            url = '#'  #TODO aqui poner la ruta de destino + book_id
        else:
            raise Http404("I can't access this page.")

        if destination_user_id == None:
            raise Http404("I can't access this page.")
        try:
            message = Message.objects.create(content=content, date_received=date_received, book_id=book_id,
                                             user_id=user_id, destination_user_id=destination_user_id)
            message.save()

            if not Notification.objects.all().filter(notification_type=notification_type, destination_user_id__exact=destination_user_id, user_id__exact=user_id, url__exact=url):
                notification = Notification.objects.create(notification_type=notification_type,
                                                           content=content_notification, url=url,
                                                           date_received=date_received, user_id=user_id,
                                                           destination_user_id=destination_user_id)
                notification.save()
        except:
            raise Http404("Sa producido un error a la bbdd.")

        url = '/graphic_designer_message/get_book/' + pk
        return redirect(url)
    else:
        raise Http404("I can't access this page.")



class GalleryImg(ListView):
    template_name = 'html_templates/Designer/Designer_DetailListImg.html'
    model = Image
    paginate_by = 3

    def get_queryset(self):
        try:
            return Image.objects.filter(petition_id=ImagePetition.objects.get(Q(graphic_designer_id=GraphicDesigner.objects.get(user_id=self.request.user.id).id) & Q(id=self.kwargs['pk'])).id)
        except:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imagepetition'] = ImagePetition.objects.get(Q(graphic_designer_id=GraphicDesigner.objects.get(user_id=self.request.user.id).id) & Q(id=self.kwargs['pk']))
        return context


def delete_img(request, pk):
    if pk != None:
        try:

            img = Image.objects.get(Q(id=pk))
            fs = FileSystemStorage()
            path = 'images/' + str(img.path)
            fs.delete(path)
            img.delete()
            message = "La imagen se borro. "
            messages.add_message(request, constants.SUCCESS, message)
            url='/graphic_designer/petitionview/'
            return redirect(url)

        except:
            raise Http404("Sa producido un error a la bbdd.")

    else:
        raise Http404("I can't access this page.")
