# Generated by Django 4.2.4 on 2023-10-29 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0012_comment_date_posted_note_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='note',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
