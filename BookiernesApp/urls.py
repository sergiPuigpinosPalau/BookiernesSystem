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
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]