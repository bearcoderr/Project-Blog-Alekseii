# Generated by Django 5.0.6 on 2024-07-10 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_alter_formsnews_options_alter_formsnews_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='feetbicke',
        ),
        migrations.AddField(
            model_name='news',
            name='feetbicke',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='News.formsnews', verbose_name='Отзыв'),
        ),
    ]
