# Generated by Django 4.2.4 on 2023-10-22 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='categoryImage',
            field=models.ImageField(blank=True, null=True, upload_to='category_images'),
        ),
    ]
