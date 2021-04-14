from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

#TODO anyadir foto perfil
class User(AbstractUser):
    USER_TYPE_CHOICES = [('writer', 'Escritor'), ('editor', 'Editor'), ('main_editor', 'Escriptor principal'), ]
    user_type = models.CharField(
        max_length=255,
        choices=USER_TYPE_CHOICES,
        default='writer',
    )

    def get_user_type_name(self):
        return dict(self.USER_TYPE_CHOICES)[self.user_type]


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='editor_profile')
    assigned_theme = models.ForeignKey(Theme, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    def get_availability(self):
        counter = 0
        for book in self.books_assigned.all():
            if book.book_status != 'presented' or book.book_status != 'new_version':
                counter += 1
        return counter

    def get_presented_books(self):
        if self.user.user_type == 'main_editor':
            return Book.objects.all().filter(book_status="presented")

    def get_books_to_revise(self):
        return self.books_assigned.all().filter(book_status="revised")


# TODO revisar nulls
class Book(models.Model):
    BOOK_STATUSES = [('presented', 'Presentat'), ('revised', 'Revisat'), ('modifying', 'Modificant'),
                     ('accepted', 'Aceptat'), ('rejected', 'Rebutjat'), ('published', 'Publicat'), ('new_version', 'New Version')]
    title = models.CharField(null=False, max_length=255)
    author = models.ForeignKey(Writer, null=True, on_delete=models.PROTECT)
    assigned_to = models.ForeignKey(Editor, null=True, on_delete=models.PROTECT, related_name='books_assigned')
    book_status = models.CharField(null=True, max_length=255, choices=BOOK_STATUSES)
    description = models.TextField(null=True)
    theme = models.ForeignKey(Theme, null=True, on_delete=models.PROTECT, related_name='books_themes')
    path = models.FileField(null=True)
    main_editor_comment = models.TextField(null=True)
    new_book_version = models.OneToOneField("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


class Notification(models.Model):
    NOTIFICATION_CHOICES = [('modification', 'Modificacio'), ('message', 'Missatge'), ('presented', 'Presentat'),
                            ('assigned', 'Assignat')]
    content = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=255, choices=NOTIFICATION_CHOICES)

    def __str__(self):
        return str(self.notification_type)


class NotificationTable(models.Model):
    destination_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='user_notifications')
    date_received = models.DateField()
    notification = models.ForeignKey(Notification, null=True, on_delete=models.PROTECT, related_name='type_of_notification')

    def __str__(self):
        return "Notification " + str(self.id) + "for: " + str(self.destination_user)


class Message(models.Model):
    destination_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='user_messages')
    book = models.ForeignKey(Book, null=True, on_delete=models.PROTECT, related_name='book_messages')
    content = models.CharField(max_length=255)
    date_received = models.DateField()
