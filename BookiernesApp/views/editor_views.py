import json
import requests
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, FormView, CreateView
from django.views.generic import TemplateView
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime

from BookiernesApp.decorators import editor_required, book_in_revision
from BookiernesApp.forms import SendBookToDesign, SendImagePetition, TranslatedBookForm

from BookiernesApp.models import *
from BookiernesApp.decorators import *
from BookiernesApp.models import Book, User, Writer, Notification, Message
import datetime

from BookiernesSystem.settings import MEDIA_ROOT


@method_decorator([login_required, editor_required], name='dispatch')
class EditorBookRevision(ListView):
    model = Book
    template_name = 'html_templates/Editor/Editor_BooksToRevise.html'
    # paginate_by = 100  # if pagination is desired


@method_decorator([login_required, editor_required, book_in_revision], name='dispatch')
class EditorBookDetail(DetailView):
    model = Book
    template_name = 'html_templates/Editor/Editor_DetailBookToRevise.html'


@method_decorator([login_required, editor_required], name='dispatch')
class EditorTranslatedBookCreate(SuccessMessageMixin, FormView):
    template_name = 'html_templates/Editor/Editor_TranslateBook.html'
    form_class = TranslatedBookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # import os
        # module_dir = os.path.dirname(__file__)  # get current directory
        # file_path = os.path.join(module_dir, '../../README.md')
        # f = open(file_path)
        # text = f.read()
        # url = "http://192.168.56.1:5000/translate"
        # payload = {"q": text, "source": "en", "target": "es"}
        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        # data_json = json.loads(response.content)
        # context['test'] = data_json['translatedText']
        #context['language_options'] = {'en': 'English', 'es': 'Spanish'}
        return context

    def form_valid(self, form):
        translated_book = Book.objects.get(title=form.cleaned_data['book_title'])
        translated_book.id = None
        translated_book.title = form.cleaned_data['book_title'] + dict(form.LANGUAGE_CHOICES)[form.cleaned_data['target_language']]
        #Translate
        import os
        #module_dir = os.path.abspath(os.path.dirname(__name__))  # get current directory
        file_path = os.path.join(MEDIA_ROOT, translated_book.path.__str__())
        f = open(file_path)
        text = f.read()
        url = "http://192.168.56.1:5000/translate"
        payload = {"q": text, "source": form.cleaned_data['source_language'], "target": form.cleaned_data['target_language']}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data_json = json.loads(response.content)
        self.license_file.save(translated_book.title, ContentFile(data_json['translatedText']))
        #translated_book.save()
        return super(EditorTranslatedBookCreate, self).form_valid(form)



def autocomplete_TranslateBook(request):
    if "term" in request.GET:
        bookstqr = Book.objects.filter(title__istartswith=request.GET.get('term'))
        book_list = list()
        for book in bookstqr:
            book_list.append(book.title)
        return JsonResponse(book_list, safe=False)


@method_decorator([login_required, editor_required], name='dispatch')
class EditorBooksToDesign(TemplateView):
    model = Book
    template_name = 'html_templates/Editor/Editor_BooksToDesign.html'


@method_decorator([login_required, editor_required], name='dispatch')
class EditorImagePetitions(TemplateView):
    model = ImagePetition
    template_name = 'html_templates/Editor/Editor_ImagePetitions.html'


@method_decorator([login_required, editor_required], name='dispatch')
class EditorImagePetitionDetail(DetailView):
    model = ImagePetition
    template_name = 'html_templates/Editor/Editor_DetailPetitionImage.html'


@method_decorator([login_required, editor_required], name='dispatch')
class EditorImagePetitionsCreate(SuccessMessageMixin, CreateView):
    model = ImagePetition
    template_name = 'html_templates/Editor/Editor_CreateImagePetition.html'
    form_class = SendImagePetition
    success_url = '/editor_image_petitions'

    def form_valid(self, form):
        form.instance.editor = self.request.user.editor_profile
        form.instance.date_received = datetime.datetime.now()
        return super(EditorImagePetitionsCreate, self).form_valid(form)


@method_decorator([login_required, editor_required, book_in_design], name='dispatch')
class EditorBookDesignDetail(SuccessMessageMixin, UpdateView):
    model = Book
    template_name = 'html_templates/Editor/Editor_DetailBookToDesign.html'
    form_class = SendBookToDesign

    def get_success_message(self, cleaned_data):
        if self.request.POST['action'] == 'send_to_design':
            return "El llibre %(title)s s'ha enviat a maquetar correctament. " % {'title': self.object.title}
        elif self.request.POST['action'] == 'publish':
            return "El llibre %(title)s s'ha publicat correctament. " % {'title': self.object.title}

    def get_success_url(self, **kwargs):
        if self.request.POST['action'] == 'send_to_design':
            return reverse('BookiernesApp:editor_design_detail', kwargs={'pk': self.object.id})
        elif self.request.POST['action'] == 'publish':
            return reverse_lazy('BookiernesApp:editor_books_to_design')

    def form_valid(self, form):
        response = super().form_valid(form)
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        if self.request.POST['action'] == 'send_to_design':
            book.book_status = 'designing'
        elif self.request.POST['action'] == 'publish':
            book.book_status = 'published'
        book.save()
        return response


@login_required
@editor_required
def accept_or_reject(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.POST['action'] == 'accept':
        book.book_status = 'accepted'
    elif request.POST['action'] == 'reject':
        book.book_status = 'rejected'
        book.main_editor_comment = request.POST['editor_rejected_comment']
    book.save()
    # Redirect
    return redirect('BookiernesApp:editor_book_revision')


@method_decorator([login_required, editor_required], name='dispatch')
class Editor_Chat_Book(TemplateView):
    model = Book
    template_name = 'html_templates/Editor/Chat.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            notification = Notification.objects.filter(destination_user_id=self.request.user.id)
            context['notification_numbers'] = notification.count()
            context['notifications'] = notification
            context['book_numbers'] = Book.objects.count()
            book = Book.objects.get(Q(pk=self.kwargs['pk']))

            if ((book.assigned_to == None and book.author == None) or book.assigned_to.user.id != self.request.user.id):
                raise Http404("I can't access this page.")

            context['book'] = book
            # book.assigned_to
            messages = Message.objects.filter(Q(book_id=book.id) & Q(
                Q(Q(user_id=self.request.user.id) & Q(destination_user_id=book.author.user.id)) | Q(
                    Q(user_id=book.author.user.id) & Q(destination_user_id=self.request.user.id))))

            context['messages'] = messages
            context['messages_numbers'] = messages.count()
            return context
        except:
            raise Http404("I can't access this page.")


@login_required
@editor_required
def editor_post_chat(request, pk):
    if request.method == "POST":
        content = request.POST['content']
        date_received = datetime.now()
        book_id = pk
        user_id = request.user.id
        destination_user_id = Book.objects.get(id=pk).author.user.pk
        notification_type = 'message'
        content_notification = 'Has recibido un mensaje.'

        # if User.objects.get(id=destination_user_id).user_type == "editor" or User.objects.get(id=destination_user_id).user_type == "main_editor":
        url = '/writer_message/get_book/' + book_id
        # else:
        # raise Http404("I can't access this page.")
        try:
            message = Message.objects.create(content=content, date_received=date_received, book_id=book_id,
                                             user_id=user_id, destination_user_id=destination_user_id)
            message.save()

            if not Notification.objects.all().filter(notification_type=notification_type,
                                                     destination_user_id__exact=destination_user_id,
                                                     user_id__exact=user_id, url__exact=url):
                notification = Notification.objects.create(notification_type=notification_type,
                                                           content=content_notification, url=url,
                                                           date_received=date_received, user_id=user_id,
                                                           destination_user_id=destination_user_id)
                notification.save()
        except:
            raise Http404("Sa producido un error a la bbdd.")

        url = '/editor_message/get_book/' + pk
        return redirect(url)
    else:
        raise Http404("I can't access this page.")


@login_required
@editor_required
def editor_notification(request, pk):
    if pk != None:
        try:
            notification = Notification.objects.get(Q(id=pk) & Q(destination_user_id=request.user.id))
            url = notification.url
            notification.delete()
            return redirect(url)

        except:
            raise Http404("Sa producido un error a la bbdd.")

    else:
        raise Http404("I can't access this page.")
