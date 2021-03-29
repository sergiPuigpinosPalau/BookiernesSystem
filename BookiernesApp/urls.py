from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from BookiernesApp.views import *

app_name = "BookiernesApp"

urlpatterns = [
    path('', mainView),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^writer_published/$', PublishedBooks, name='writer_published_books'),
]