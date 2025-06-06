# Generated by Django 5.2.1 on 2025-05-31 03:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=200)),
                ('categoria', models.CharField(max_length=100)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurantes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Restaurante',
                'verbose_name_plural': 'Restaurantes',
                'ordering': ['nombre'],
            },
        ),
    ]
