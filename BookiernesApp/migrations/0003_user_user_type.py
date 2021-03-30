# Generated by Django 3.1.7 on 2021-03-30 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookiernesApp', '0002_editor_maineditor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('writer', 'Writer'), ('editor', 'Editor'), ('main_editor', 'Main editor')], default='writer', max_length=20),
        ),
    ]