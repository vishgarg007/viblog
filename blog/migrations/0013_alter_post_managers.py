# Generated by Django 4.1.1 on 2022-10-28 03:02

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_comment_email'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('pub', django.db.models.manager.Manager()),
            ],
        ),
    ]