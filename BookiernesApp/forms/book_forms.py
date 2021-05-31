from django import forms
from django.core.exceptions import ValidationError

from BookiernesApp.models import *


class TranslatedBookForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
    ]
    book_title = forms.CharField(label='Llibre a traduir', widget=forms.TextInput(attrs={'class': 'form-control'}))
    source_language = forms.CharField(label='Elegeix idioma del llibre \n',
                                      widget=forms.Select(attrs={
                                          'class': 'custom-select',
                                      }, choices=LANGUAGE_CHOICES))
    target_language = forms.CharField(label='Elegeix idioma al qual es vol traduir el llibre \n',
                                      widget=forms.Select(attrs={
                                          'class': 'custom-select',
                                      }, choices=LANGUAGE_CHOICES))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Add request to the arguments so it can be used later
        super(TranslatedBookForm, self).__init__(*args, **kwargs)

    def clean(self):
        bookstqr = Book.objects.filter(
            Q(title=self.cleaned_data['book_title']) & Q(assigned_to__user=self.request.user) & (
                    Q(book_status="accepted") | Q(book_status="designing") | Q(book_status="published")))
        # Invalid input
        if not bookstqr:
            raise ValidationError(
                'Llibre invalid: %(book)s',
                code='invalid_book',
                params={'book': self.cleaned_data['book_title']},
            )
        elif bookstqr.count() > 1:
            raise ValidationError(
                'S´ha trobat dos llibres amb el mateix nom',
                code='invalid_book',
            )
        elif self.cleaned_data['source_language'] == self.cleaned_data['target_language']:
            raise ValidationError(
                'Idioma del llibre ha de ser diferent del idioma que es vol traduir',
                code='invalid_book',
            )
        # Title already done
        language = dict(self.LANGUAGE_CHOICES)[self.cleaned_data['target_language']]
        new_name = self.cleaned_data['book_title'] + " (" + language + ")"
        if Book.objects.filter(title=new_name):
            raise ValidationError(
                'Llibre %(book)s ja ha sigut traduït al %(language)s amb el nom de  " %(translated_book)s "',
                code='book_already_translated',
                params={'book': self.cleaned_data['book_title'], 'language': language, 'translated_book': new_name},
            )
        return self.cleaned_data


class SendImagePetition(forms.ModelForm):
    class Meta:
        model = ImagePetition
        fields = ['title', 'description']


class SendBookToDesign(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_to_design']


class Present_Book(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['author', 'title', 'theme', 'description', 'path', 'book_status']

        widgets = {
            'author': forms.TextInput(
                attrs={
                    'class': 'invisible',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'titleCheck',
                }
            ),
            'theme': forms.Select(
                attrs={
                    'class': 'custom-select',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'name': 'content',
                    'id': 'editor',
                }
            ),
            'path': forms.FileInput(
                attrs={
                    'accept': '.md',

                }
            ),
            'book_status': forms.TextInput(
                attrs={
                    'class': 'invisible',
                }
            ),

        }


class Edit_Book(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['author', 'title', 'theme', 'description', 'path', 'book_status']

        widgets = {
            'author': forms.TextInput(
                attrs={
                    'class': 'invisible',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'titleCheck',
                }
            ),
            'theme': forms.Select(
                attrs={
                    'class': 'custom-select',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'name': 'content',
                    'id': 'editor',
                }
            ),
            'path': forms.FileInput(
                attrs={
                    'accept': '.md',

                }
            ),
            'book_status': forms.TextInput(
                attrs={
                    'class': 'invisible',
                }
            ),

        }
