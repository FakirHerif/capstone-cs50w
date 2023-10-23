# Generated by Django 4.2.4 on 2023-10-22 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0007_site_remove_input_sites_remove_input_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categoryComment', to='capstone.category'),
        ),
    ]