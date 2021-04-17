# Generated by Django 3.2 on 2021-04-16 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0002_auto_20210416_0444'),
    ]

    operations = [
        migrations.CreateModel(
            name='SymposiumBroadcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=220)),
                ('message_from', models.CharField(choices=[('G', 'Governor'), ('D', 'Deputy Governor')], default='G', max_length=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('archive', models.BooleanField(default=False)),
                ('symposium', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='broadcast', to='uni.symposium')),
            ],
        ),
    ]
