from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = [('writer', 'Writer'), ('editor', 'Editor'), ('main_editor', 'Main editor'), ]
    user_type = USER_TYPE_CHOICES


class Writer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='writer_profile')
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Writer, null=True, on_delete=models.PROTECT)
