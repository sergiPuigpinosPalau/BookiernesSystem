from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from BookiernesApp.models import *

admin.site.register(User, UserAdmin)
admin.site.register(Writer)
admin.site.register(Book)
admin.site.register(Theme)
admin.site.register(Editor)
admin.site.register(Message)
admin.site.register(GraphicDesigner)