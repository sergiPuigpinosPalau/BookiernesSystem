from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, CreateView


#@method_decorator([login_required, designer_required], name='dispatch')
from BookiernesApp.models import ImagePetition, User, Book


class AssignmentListImg(ListView):
    template_name = 'html_templates/Designer/Main/Designer_AssignmentListImg.html'
    model = ImagePetition
    paginate_by = 10

    def get_queryset(self):
        try:
            return ImagePetition.objects.filter(graphic_designer_id__isnull=True)
        except:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment_img_count'] = ImagePetition.objects.filter(graphic_designer_id__isnull=True).count()
        context['assignment_BockMaquetat_count'] = Book.objects.filter(designer_assigned_to_id__isnull=True).filter(
            book_status='designing').count()
        return context

class AssignmentDetaliImg(DetailView):
    model = ImagePetition
    template_name = 'html_templates/Designer/Main/Main_Designer_DetailImg.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment_img_count'] = ImagePetition.objects.filter(graphic_designer_id__isnull=True).count()
        context['assignment_BockMaquetat_count'] = Book.objects.filter(designer_assigned_to_id__isnull=True).filter(
            book_status='designing').count()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment_img_count'] = ImagePetition.objects.filter(graphic_designer_id__isnull=True).count()
        context['assignment_BockMaquetat_count'] = Book.objects.filter(designer_assigned_to_id__isnull=True).filter(book_status='designing').count()
        return context

class AssignmentDetaliBockMaquetat(DetailView):
    model = Book
    template_name = 'html_templates/Designer/Main/Main_Designer_DetailBockMaquetat.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment_img_count'] = ImagePetition.objects.filter(graphic_designer_id__isnull=True).count()
        context['assignment_BockMaquetat_count'] = Book.objects.filter(designer_assigned_to_id__isnull=True).filter(book_status='designing').count()
        context['users'] = User.objects.filter(Q(user_type = "graphic_designer") | Q(user_type = "main_graphic_designer")  )
        return context