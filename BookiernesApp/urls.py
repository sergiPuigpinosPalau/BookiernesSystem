from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from BookiernesApp.views import *

app_name = "BookiernesApp"

urlpatterns = [
    path('', login_required(mainView), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^writer_published/$', login_required(PublishedBooks.as_view()), name='writer_published_books'),
    url(r'^editor_book_revision/$', login_required(EditorBookRevision.as_view()), name='editor_book_revision'),
    url(r'^maineditor_book_revision/$', login_required(MainEditorBookRevision), name='maineditor_book_revision'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]