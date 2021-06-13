from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from BookiernesApp.models import Book


def book_in_revision(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])
        if book.book_status == 'revised' or book.book_status == 'modifying':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    return wrap


def book_presented(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])
        if book.book_status == 'presented':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    return wrap


def book_in_design(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])
        if book.book_status == 'accepted' or book.book_status == 'designing':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    return wrap


def writer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    """
    Decorator for views that checks that the logged in user is a writer,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 'writer',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def subscribed_reader_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    """
    Decorator for views that checks that the logged in user is a writer,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 'subscribed_reader',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def editor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    """
    Decorator for views that checks that the logged in user is a editor,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.user_type == 'editor' or u.user_type == 'main_editor'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def mainEditor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    """
    Decorator for views that checks that the logged in user is a main editor,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 'main_editor',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def it_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    """
    Decorator for views that checks that the logged in user is a main editor,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 'it',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator