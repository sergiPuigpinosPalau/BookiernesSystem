import json

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from BookiernesApp.decorators import subscribed_reader_required
from BookiernesApp.models import Book, Theme, Writer


from BookiernesApp.forms import FromUserReader
import subprocess
from BookiernesSystem.settings import STATIC_URL, MEDIA_URL, BASE_DIR

# para insatalar
import markdown
from xhtml2pdf import pisa

import simplejson as json
from django.http import HttpResponse


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
        context["themes"] = Theme.objects.all()
        context["writers"] = Writer.objects.all()
        return context


class Landing_page_search(ListView):
    template_name = 'html_templates/Lector/landing_page.html'
    model = Book
    paginate_by = 6

    def get_queryset(self):
        try:
            if  self.kwargs['type'] == "1":
                return Book.objects.filter(Q(book_status="presented") & Q(author_id=self.kwargs['pk']))
            elif  self.kwargs['type'] == "2":
                return Book.objects.filter(Q(book_status="presented") & Q(theme_id=self.kwargs['pk']))

        except:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["themes"] = Theme.objects.all()
        context["writers"] = Writer.objects.all()
        return context


class Landing_page_search_from(ListView):
    template_name = 'html_templates/Lector/landing_page.html'
    model = Book
    paginate_by = 6

    def get_queryset(self):
        try:
            return Book.objects.filter(Q(book_status="presented") & Q(title__icontains=self.request.GET.get('search_text') ) )
            #elif  self.kwargs['type'] == "2": //TODO busacr idomas
            #    return Book.objects.filter(Q(book_status="presented") & Q(theme_id=self.kwargs['pk']))

        except:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["themes"] = Theme.objects.all()
        context["writers"] = Writer.objects.all()
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


def book_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Book.objects.filter(title__icontains=q)
        results = []
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

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



            return HttpResponse(pdf, 'application/pdf')
        except:
            raise Http404("Sa producido un error a descaregar el pdf .")

    else:
        raise Http404("I can't access this page.")





