# Generated by Django 4.1.1 on 2022-11-20 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_photo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Photo',
            new_name='Contest',
        ),
    ]
