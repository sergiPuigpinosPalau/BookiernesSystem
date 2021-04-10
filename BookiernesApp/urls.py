from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import RedirectView, ListView

from BookiernesApp.views import *

app_name = "BookiernesApp"

urlpatterns = [
    # TODO check login only view
    path('', login_required(mainView), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # writer
    url(r'^writer_published/$', PublishedBooks.as_view(), name='writer_published_books'),
    # editor urls
    url(r'^editor_book_revision/$', EditorBookRevision.as_view(), name='editor_book_revision'),
    url(r'^editor_book_revision/book_revision_detail/(?P<pk>\d+)/$',
        EditorBookDetail.as_view(), name='editor_book_detail'),
    # main editor urls
    # TODO create date_presented attribute to sort books
    url(r'^maineditor__books_presented_in_editorial/$',
        MainEditorBooksPresentedInEditorial.as_view(), name='maineditor_books_presented_editorial'),
    url(r'^maineditor__books_presented_in_editorial/book_presented_detail/(?P<pk>\d+)/$',
        EditorBookDetail.as_view(), name='maineditor_book_presented_detail'),

]
