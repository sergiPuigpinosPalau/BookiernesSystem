from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from xhtml2pdf import pisa

from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from BookiernesApp.decorators import subscribed_reader_required
from BookiernesApp.models import Book, Theme, Writer


from BookiernesApp.forms import FromUserReader
import subprocess
from BookiernesSystem.settings import STATIC_URL, MEDIA_URL, BASE_DIR

import markdown
import pdfkit

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

@login_required
@subscribed_reader_required
def dowload_pdf(request ,pk):
    if pk != None:
        try:
            filename = Book.objects.get(id=pk).book_designed

            input_filename = './media/book_designed/'+str(filename)

            f = open(input_filename, 'r')
            text_md = f.read()
            f.close()
            text_html = markdown.markdown(text_md)
            archivo='./media/tmp/pdf_'+request.user.username+'_'+str(filename)+'_fin.pdf'
            file = open(str(archivo), "w+b")
            pisaStatus = pisa.CreatePDF(text_html.encode('utf-8'), dest=file,
                                        encoding='utf-8')

            file.seek(0)
            pdf = file.read()
            file.close()

            fs = FileSystemStorage()
            fs.delete(str(archivo))

            return HttpResponse(pdf, 'application/pdf')
        except:
            raise Http404("Sa producido un error a descaregar el pdf .")

    else:
        raise Http404("I can't access this page.")





