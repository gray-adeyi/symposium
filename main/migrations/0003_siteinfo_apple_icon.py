# Generated by Django 3.1.7 on 2021-04-08 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210408_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='apple_icon',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]