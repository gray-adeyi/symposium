# Generated by Django 3.1.7 on 2021-04-08 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_socialaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='source_code_link',
            field=models.URLField(blank=True),
        ),
    ]