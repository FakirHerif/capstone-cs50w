# Generated by Django 4.2.4 on 2023-10-22 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0005_category_categoryimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='sites',
            field=models.CharField(choices=[('DevDocs', 'DevDocs')], default='DevDocs', max_length=30),
        ),
    ]
