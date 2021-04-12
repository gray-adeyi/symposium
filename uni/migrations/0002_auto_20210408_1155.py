# Generated by Django 3.1.7 on 2021-04-08 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('r', 'Rather not say')], max_length=1),
        ),
        migrations.AddField(
            model_name='student',
            name='religion',
            field=models.CharField(blank=True, choices=[('c', 'Christianity'), ('i', 'Islam'), ('r', 'Rather not say')], max_length=1),
        ),
    ]