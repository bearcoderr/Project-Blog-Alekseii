# Generated by Django 5.0.6 on 2024-07-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worck', '0004_alter_worcksite_gallery_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worcksite',
            name='imgWorck',
            field=models.ImageField(upload_to='photos/worck/', verbose_name='Главное изображение'),
        ),
    ]
