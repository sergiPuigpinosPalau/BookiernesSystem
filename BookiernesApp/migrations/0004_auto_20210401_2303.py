# Generated by Django 3.1.7 on 2021-04-01 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BookiernesApp', '0003_user_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('notification_type', models.CharField(choices=[('modification', 'Modificacio'), ('message', 'Missatge'), ('presented', 'Presentat'), ('assigned', 'Assignat')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='books_assigned', to='BookiernesApp.editor'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_status',
            field=models.CharField(choices=[('presented', 'Presentat'), ('revised', 'Revisat'), ('modifying', 'Modificant'), ('accepted', 'Aceptat'), ('rejected', 'Rebutjat'), ('published', 'Publicat')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='main_editor_comment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='path',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='editor',
            name='availability',
            field=models.CharField(choices=[('occupied', 'Ocupat'), ('available', 'Disponible')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='maineditor',
            name='availability',
            field=models.CharField(choices=[('occupied', 'Ocupat'), ('available', 'Disponible')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='editor',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='maineditor',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('writer', 'Writer'), ('editor', 'Editor'), ('main_editor', 'Main editor')], default='writer', max_length=255),
        ),
        migrations.AlterField(
            model_name='writer',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='NotificationTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateField()),
                ('destination_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_notifications', to=settings.AUTH_USER_MODEL)),
                ('notification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='type_of_notification', to='BookiernesApp.notification')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('date_received', models.DateField()),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='book_messages', to='BookiernesApp.book')),
                ('destination_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='books_themes', to='BookiernesApp.theme'),
        ),
        migrations.AddField(
            model_name='editor',
            name='assigned_theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BookiernesApp.theme'),
        ),
        migrations.AddField(
            model_name='maineditor',
            name='assigned_theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BookiernesApp.theme'),
        ),
    ]
