from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, CreateView


#@method_decorator([login_required, designer_required], name='dispatch')
from BookiernesApp.models import ImagePetition, User, Book, GraphicDesigner


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

