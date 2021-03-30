from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = [('writer', 'Writer'), ('editor', 'Editor'), ('main_editor', 'Main editor'), ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='writer',
    )

    def get_user_type(self):
        return str(self.user_type)


class Writer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='writer_profile')
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='editor_profile')
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

class MainEditor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='main_editor_profile')
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Writer, null=True, on_delete=models.PROTECT)
