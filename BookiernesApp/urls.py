from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from BookiernesApp.views import *

app_name = "BookiernesApp"

urlpatterns = [
    path('', login_required(mainView), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),

    # http://127.0.0.1:8000/writer_published/
    url(r'^writer_published/$', login_required(PublishedBooks.as_view()), name='writer_published_books'),
    # http://127.0.0.1:8000/writer_published/get_book/1
    url(r'^writer_published/get_book/(?P<pk>\d+)/$', login_required(Get_Books.as_view()), name='books'),

    # http://127.0.0.1:8000/writer_published/add_book/
    url(r'^writer_published/add_book/$', login_required(PublishBook.as_view()), name='writer_publish_book'),
    # http://127.0.0.1:8000/writer_published/edit_book/1
    url(r'^writer_published/edit_book/(?P<pk>\d+)/$', login_required(Edit_Book.as_view()), name='writer_modify_a_book'),
    
    url(r'^editor_book_revision/$', login_required(EditorBookRevision.as_view()), name='editor_book_revision'),
    url(r'^maineditor_book_revision/$', login_required(MainEditorBookRevision.as_view()), name='maineditor_book_revision'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)