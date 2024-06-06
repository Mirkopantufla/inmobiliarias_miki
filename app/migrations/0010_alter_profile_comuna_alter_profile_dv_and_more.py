# Generated by Django 4.2 on 2024-06-05 23:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_profile_comuna_alter_profile_dv_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='comuna',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='app.comuna'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='dv',
            field=models.SmallIntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(11)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='region',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='app.region'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='rut',
            field=models.IntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999999999)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='telefono',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tipo_usuario',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='app.tipousuario'),
            preserve_default=False,
        ),
    ]
