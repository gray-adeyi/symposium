# Generated by Django 3.1.7 on 2021-04-15 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0013_auto_20210415_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='offered_course',
            new_name='course',
        ),
    ]
