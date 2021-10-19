# Generated by Django 3.2.8 on 2021-10-16 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0004_auto_20210422_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='symposium',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='symposium',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='uni.symposium'),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='course',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='uni.offeredcourse'),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='timetable',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='units', to='uni.timetable'),
        ),
    ]