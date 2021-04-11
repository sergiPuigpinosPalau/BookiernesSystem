from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

#TODO anyadir foto perfil
class User(AbstractUser):
    USER_TYPE_CHOICES = [('writer', 'Writer'), ('editor', 'Editor'), ('main_editor', 'Main editor'), ]
    user_type = models.CharField(
        max_length=255,
        choices=USER_TYPE_CHOICES,
        default='writer',
    )

    def get_user_type(self):
        return str(self.user_type)


class Theme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Writer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='writer_profile')
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Editor(models.Model):
    AVAILABILITY_TYPES = [('occupied', 'Ocupat'), ('available', 'Disponible')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='editor_profile')
    assigned_theme = models.ForeignKey(Theme, null=True, on_delete=models.CASCADE)
    availability = models.CharField(null=True, max_length=255, choices=AVAILABILITY_TYPES)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class MainEditor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='main_editor_profile')
    assigned_theme = models.ForeignKey(Theme, null=True, on_delete=models.CASCADE)
    availability = models.CharField(null=True, max_length=255, choices=Editor.AVAILABILITY_TYPES)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

# TODO mira como hacer que no se guarde todo en book si no que crea una carpeta por cada escritor
def user_directory_path(instance, filename):
    return 'book/user_{0}/{1}'.format(instance.user.id, filename)

# TODO revisar nulls
class Book(models.Model):
    BOOK_STATUSES = [('presented', 'Presentat'), ('revised', 'Revisat'), ('modifying', 'Modificant'),
                     ('accepted', 'Aceptat'), ('rejected', 'Rebutjat'), ('published', 'Publicat')]
    title = models.CharField(null=True, max_length=255 ,blank=True)
    author = models.ForeignKey(Writer, null=True, on_delete=models.PROTECT, blank=True)
    assigned_to = models.ForeignKey(Editor, null=True, on_delete=models.PROTECT, related_name='books_assigned', blank=True)
    book_status = models.CharField(null=True, max_length=255, choices=BOOK_STATUSES,blank=True)
    description = models.TextField(null=True,blank=True)
    theme = models.ForeignKey(Theme, null=True, on_delete=models.PROTECT, related_name='books_themes',blank=True)
    path = models.FileField(upload_to = 'book' ,null=True,blank=True)
    main_editor_comment = models.TextField(null=True, blank=True)
    #latest_book = models.ForeignKey("self", null=True, on_delete=models.CASCADE, related_name='old_versions')#TODO test

    def __str__(self):
        return str(self.title)
    
    def __unicode__(self):
         return self.description


class Notification(models.Model):
    NOTIFICATION_CHOICES = [('modification', 'Modificacio'), ('message', 'Missatge'), ('presented', 'Presentat'),
                            ('assigned', 'Assignat')]
    content = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=255, choices=NOTIFICATION_CHOICES)

    def __str__(self):
        return str(self.notification_type)


class NotificationTable(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='user_notifications')
    destination_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='destination_user_notifications')
    date_received = models.DateField()
    notification = models.ForeignKey(Notification, null=True, on_delete=models.PROTECT, related_name='type_of_notification')

    def __str__(self):
        return "Notification " + str(self.id) + "for: " + str(self.destination_user)


class Message(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='user_messages')
    destination_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='destination_user_messages')
    book = models.ForeignKey(Book, null=True, on_delete=models.PROTECT, related_name='book_messages')
    content = models.CharField(max_length=255)
    date_received = models.DateField()


