from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import RedirectView, ListView

from BookiernesApp.views import *

app_name = "BookiernesApp"

urlpatterns = [
    path('', login_required(mainView), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    #writer
    url(r'^writer_published/$', login_required(PublishedBooks.as_view()), name='writer_published_books'),
    #editor urls
    url(r'^editor_book_revision/$', login_required(EditorBookRevision.as_view()), name='editor_book_revision'),
    #main editor urls
    # TODO create date_presented attribute to sort books
    #TODO decorator in url
    url(r'^maineditor__books_presented_in_editorial/$',
        login_required(
            ListView.as_view(queryset=Book.objects.all().filter(book_status="presented"),
                             context_object_name='book_list',  # variable where is stored
                             template_name='html_templates/MainEditor/MainEditor_PresentedBooks.html')), name='maineditor_books_presented'),

]