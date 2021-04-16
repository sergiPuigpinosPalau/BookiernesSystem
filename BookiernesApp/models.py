from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# TODO anyadir foto perfil
from django.db.models import Q


class User(AbstractUser):
    USER_TYPE_CHOICES = [('writer', 'Escritor'), ('editor', 'Editor'), ('main_editor', 'Escriptor principal'), ]
    user_type = models.CharField(
        max_length=255,
        choices=USER_TYPE_CHOICES,
        default='writer',
    )
    path_profile_photo = models.FileField(upload_to='profile_photo', null=True, blank=True)

    def get_user_type_name(self):
        return dict(self.USER_TYPE_CHOICES)[self.user_type]

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

    def get_user_id(self):
        return self.user.id

    def get_presented_books(self):
        return Book.objects.all().filter(author=self)


class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='editor_profile')
    assigned_theme = models.ForeignKey(Theme, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    def get_user_id(self):
        return self.user.id

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
        return self.books_assigned.all().filter(Q(book_status="revised") | Q(book_status='modifying'))


def user_directory_path(instance, filename):
    return 'book/user_{0}/{1}'.format(instance.user.id, filename)


# TODO revisar nulls
# TODO comprobar blanks
class Book(models.Model):
    BOOK_STATUSES = [('presented', 'Presentat'), ('revised', 'Revisat'), ('modifying', 'Modificant'),
                     ('accepted', 'Aceptat'), ('rejected', 'Rebutjat'), ('published', 'Publicat'),
                     ('new_version', 'New Version')]
    title = models.CharField(null=True, max_length=255, blank=True)
    author = models.ForeignKey(Writer, null=True, on_delete=models.PROTECT, blank=True)
    assigned_to = models.ForeignKey(Editor, null=True, on_delete=models.PROTECT, related_name='books_assigned',
                                    blank=True)
    book_status = models.CharField(null=True, max_length=255, choices=BOOK_STATUSES, blank=True)
    description = models.TextField(null=True, blank=True)
    theme = models.ForeignKey(Theme, null=True, on_delete=models.PROTECT, related_name='books_themes', blank=True)
    path = models.FileField(upload_to='book', null=True, blank=True)
    main_editor_comment = models.TextField(null=True, blank=True)
    #new_book_version = models.OneToOneField("self", null=True, blank=True, on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.title)

    def __unicode__(self):
        return self.description


class Notification(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='user_notifications')
    destination_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT,
                                         related_name='destination_user_notifications')
    date_received = models.DateField()
    NOTIFICATION_CHOICES = [('modification', 'Modificacio'), ('message', 'Missatge'), ('presented', 'Presentat'),
                            ('assigned', 'Assignat')]
    content = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=255, choices=NOTIFICATION_CHOICES)
    url = models.CharField(max_length=255)

    def __str__(self):
        return "Notification " + str(self.id) + "for: " + str(self.destination_user)

    def get_user(self):
        return self.user.first_name + " " + self.user.last_name


class Message(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='user_messages')
    destination_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT,
                                         related_name='destination_user_messages')
    book = models.ForeignKey(Book, null=True, on_delete=models.PROTECT, related_name='book_messages')
    content = models.CharField(max_length=255)
    date_received = models.DateField()

    def get_user_name(self):
        return self.user.first_name + " " + self.user.last_name
