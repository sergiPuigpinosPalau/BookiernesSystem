import re

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction

from BookiernesApp.models import User

from django import forms
from django.core.exceptions import ValidationError

from BookiernesApp.models import User , Writer , Editor ,GraphicDesigner


class FormularioUsuario(forms.ModelForm):
    #theme = forms.IntegerField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'password']

    def clean_username(self):
        user = User.objects.filter(username = self.cleaned_data['username']).count()
        if user == 0:
            return self.cleaned_data['username']
        else:
            raise ValidationError('El usuario existe.')

    def clean_password(self):
        password= self.cleaned_data['password']
        if len(password) <=7:
            raise ValidationError('La password tiene que tener 8 caracteres.')
        else:
            return password



    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        if self.cleaned_data['user_type'] == "editor" or self.cleaned_data['user_type'] == "main_editor":
            #if self.cleaned_data['theme'] == "0":
            #    editor=Editor(user_id=user.id)
            #    editor.save()
            #else:
            #    editor=Editor(user_id=user.id, assigned_theme_id=self.cleaned_data['theme'])
            #    editor.save()
            editor = Editor(user_id=user.id)
            editor.save()
        elif self.cleaned_data['user_type'] == "main_graphic_designer" or self.cleaned_data['user_type'] == "graphic_designer":
            graphicDesigner=GraphicDesigner(user_id=user.id)
            graphicDesigner.save()

        elif self.cleaned_data['user_type'] == "writer":
            writer=Writer(user_id=user.id)
            writer.save()

        elif self.cleaned_data['user_type'] == "it":
            user.is_superuser=1
            user.save()

        return user