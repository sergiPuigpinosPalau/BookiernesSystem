from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction

from BookiernesApp.models import *


class SignUpForm(UserCreationForm):
    user_type = forms.CharField(label='Type of account: ', widget=forms.Select(choices=User.USER_TYPE_CHOICES))
    name = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get('user_type')
        user.save()
        if user.user_type == 'writer':
            writer = Writer.objects.create(user=user)  # Create associated Model
            writer.name = self.cleaned_data.get('name')
            writer.save()
        elif user.user_type == 'editor' or user.user_type == 'main_editor':
            editor = Editor.objects.create(user=user)  # Create associated Model
            editor.name = self.cleaned_data.get('name')
            editor.save()
        return user
