import re

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction

from BookiernesApp.models import User

from django import forms
from django.core.exceptions import ValidationError

from BookiernesApp.models import User , Writer , Editor ,GraphicDesigner, SubscribedReader, CreditCard


class FormularioUsuario(forms.ModelForm):
    theme = forms.IntegerField(required=False,widget=forms.Select)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'password']

    def clean_username(self):
        user = User.objects.filter(username = self.cleaned_data['username']).count()
        if user == 0:
            return self.cleaned_data['username']
        else:
            raise ValidationError('L\' usuari ja existeix.')

    def clean_password(self):
        password= self.cleaned_data['password']
        if len(password) <=7:
            raise ValidationError('La contrasenya ha de tenir mínim 8 caràcters.')
        else:
            return password



    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        if self.cleaned_data['user_type'] == "editor" or self.cleaned_data['user_type'] == "main_editor":
            if self.cleaned_data['theme'] == "0":
                editor=Editor(user_id=user.id)
                editor.save()
            else:
                editor=Editor(user_id=user.id, assigned_theme_id=self.cleaned_data['theme'])
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


def isValid(str,type):
    # Regex to check valid
    # CVV number.
    if type == "number":
        regex = "^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35d{3})d{11})$"
        p = re.compile(regex)
        if (str == None):
            return False

        if (re.search(p, str)):
            return True
        else:
            return False

    elif type == "mm_aa":
        regex = "^[0-9]{2}\/[0-9]{2}$"
        p = re.compile(regex)
        if (str == None):
            return False

        if (re.search(p, str)):
            return True
        else:
            return False

    elif type == "CVV":
        regex = "^[0-9]{3,4}$"
        p = re.compile(regex)
        if (str == None):
            return False

        if (re.search(p, str)):
            return True
        else:
            return False

class FromUserReader(forms.ModelForm):
    password2 = forms.CharField( widget=forms.PasswordInput)
    card_namber = forms.CharField( widget=forms.TextInput)
    mm_aa = forms.CharField( widget=forms.TextInput)
    CVV = forms.CharField( widget=forms.TextInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',  'password']

    def clean_username(self):
        user = User.objects.filter(username = self.cleaned_data['username']).count()
        if user == 0:
            return self.cleaned_data['username']
        else:
            raise ValidationError('L\' usuari ja existeix.')

    def clean_password(self):
        if len(self.cleaned_data['password']) <=7 :
            raise ValidationError('La contrasenya ha de tenir mínim 8 caràcters.')
        else:
            return self.cleaned_data['password']

    def clean_password2(self):
        if len(self.cleaned_data['password2']) <=7 :
            raise ValidationError('La contrasenya 2 ha de tenir mínim 8 caràcters.')
        else:
            return self.cleaned_data['password2']

    def clean_password2andpassword(self):
        if self.cleaned_data['password'] == self.cleaned_data['password2'] :
            return self.cleaned_data['password']
        else:
            raise ValidationError('Les contrasenya han de se iguals. ')

    def clean_card_namber(self):
        if isValid(self.cleaned_data['card_namber'],'number') == False:
            raise ValidationError('El numero de la tarjeta es icorecto. ')
        else:
            return self.cleaned_data['card_namber']

    def clean_mm_aa(self):

        if isValid(self.cleaned_data['mm_aa'], 'mm_aa') == False:
            raise ValidationError('El MM/AA de la tarjeta es icorecto. ')
        else:
            return self.cleaned_data['mm_aa']


    def clean_CVV(self):

        if isValid(self.cleaned_data['CVV'], 'CVV') == False:
            raise ValidationError('El CVV de la tarjeta es icorecto. ')
        else:
            return self.cleaned_data['CVV']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 'subscribed_reader'


        if commit:
            user.save()

        creditCard=CreditCard(number=self.cleaned_data['card_namber'] , secret_number= self.cleaned_data['mm_aa'] ,date= self.cleaned_data['CVV'] )
        creditCard.save()
        subscribedReader = SubscribedReader(user_id=user.id, credit_card_id=creditCard.id )
        subscribedReader.save()
        return user
