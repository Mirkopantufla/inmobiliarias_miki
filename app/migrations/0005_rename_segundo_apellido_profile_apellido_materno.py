# Generated by Django 4.2 on 2024-06-04 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_profile_email_remove_profile_primer_apellido_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='segundo_apellido',
            new_name='apellido_materno',
        ),
    ]
