from django import forms
from django.core.exceptions import ValidationError



from BookiernesApp.models import *




class TranslatedBookForm(forms.Form):
        LANGUAGE_CHOICES = [
            ('en', 'English'),
            ('es', 'Spanish'),
        ]
        book_title = forms.CharField(label='Llibre a traduir')
        source_language = forms.CharField(label='Elegeix idioma del llibre \n',
                                         widget=forms.Select(choices=LANGUAGE_CHOICES))
        target_language = forms.CharField(label='Elegeix idioma al qual es vol traduir el llibre \n',
                                          widget=forms.Select(choices=LANGUAGE_CHOICES))




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
        fields = ['author','title','theme','description','path','book_status']

        widgets = {
            'author': forms.TextInput(
                attrs = {
                    'class':'invisible',
                }
            ),
            'title': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'id':'titleCheck',
                }
            ),
            'theme': forms.Select(
                attrs = {
                    'class':'custom-select',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'name':'content',
                    'id':'editor',
                }
            ),
            'path': forms.FileInput(
                attrs = {
                    'accept':'.md',
                    
                }
            ),
            'book_status': forms.TextInput(
                attrs = {
                    'class':'invisible',
                }
            ),
            
        }

        
class Edit_Book(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['author','title','theme','description','path','book_status']

        widgets = {
            'author': forms.TextInput(
                attrs = {
                    'class':'invisible',
                }
            ),
            'title': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'id':'titleCheck',
                }
            ),
            'theme': forms.Select(
                attrs = {
                    'class':'custom-select',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'name':'content',
                    'id':'editor',
                }
            ),
            'path': forms.FileInput(
                attrs = {
                    'accept':'.md',
                    
                }
            ),
            'book_status': forms.TextInput(
                attrs = {
                    'class':'invisible',
                }
            ),
            
        }