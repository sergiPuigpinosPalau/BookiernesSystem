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

    #Escritor
    # http://127.0.0.1:8000/writer_published/
    url(r'^writer_published/$', login_required(PublishedBooks.as_view()), name='writer_published_books'),
    # http://127.0.0.1:8000/writer_published/get_book/33
    url(r'^writer_published/get_book/(?P<pk>\d+)/$', login_required(Get_Books.as_view()), name='books'),
    # http://127.0.0.1:8000/writer_published/add_book/
    url(r'^writer_published/add_book/$', login_required(PublishBook.as_view()), name='writer_publish_book'),
    # http://127.0.0.1:8000/writer_published/edit_book/33
    url(r'^writer_published/edit_book/(?P<pk>\d+)/$', login_required(Edit_Book.as_view()), name='writer_modify_a_book'),
    # http://127.0.0.1:8000/writer_published/edit_book/33
    url(r'^writer_message/get_book/(?P<pk>\d+)/$', login_required(Chat_Book.as_view()), name='chat_book'),
    url(r'^writer_message/post_book/(?P<pk>\d+)/send/$', login_required(post_chat), name='send_message'),
    url(r'^writer_notification/(?P<pk_n>\d+)/(?P<id>\d+)/$', login_required(writer_notification), name='notification'),

    # Editor 
    url(r'^editor_message/get_book/(?P<pk>\d+)/$', login_required(Editor_Chat_Book.as_view()), name='chat_book_editor'),
    url(r'^editor_message/post_book/(?P<pk>\d+)/send/$', login_required(editor_post_chat), name='send_message_editor'),
    url(r'^editor_book_revision/$', login_required(EditorBookRevision.as_view()), name='editor_book_revision'),


    # Main Editor
    url(r'^maineditor_message/get_book/(?P<pk>\d+)/$', login_required(Maineditor_Chat_Book.as_view()), name='chat_book_maineditor'),
    url(r'^maineditor_message/post_book/(?P<pk>\d+)/send/$', login_required(maineditor_post_chat), name='send_message_maineditor'),
    url(r'^maineditor_notification/(?P<pk_n>\d+)/(?P<id>\d+)/$', login_required(maineditor_notification), name='notification_maineditor'),
    

    url(r'^maineditor_book_revision/$', login_required(MainEditorBookRevision.as_view()), name='maineditor_book_revision'),
    
    
    
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)