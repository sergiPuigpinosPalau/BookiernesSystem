from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from BookiernesApp.models import Book, Theme, Writer


from BookiernesApp.forms import FromUserReader

class Landing_page_List(ListView):
    template_name = 'html_templates/Lector/landing_page.html'
    model = Book
    paginate_by = 6

    def get_queryset(self):
        try:
            return Book.objects.filter( book_status = "presented")
        except:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["themes"]= Theme.objects.all()
        context["writers"]= Writer.objects.all()
        return context


class AssignmentDetaliImg(DetailView):
    model = Book
    template_name = 'html_templates/Lector/info_libro.html'


class RegisterReaders(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'html_templates/Lector/to_register.html'
    form_class = FromUserReader
    success_url = reverse_lazy('BookiernesApp:home')

    def get_success_message(self, cleaned_data):
        return "Compte creat. "

