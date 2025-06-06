# Generated by Django 5.2.1 on 2025-05-31 03:03

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('telefono', models.CharField(blank=True, max_length=20, null=True, verbose_name='teléfono')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True, verbose_name='dirección')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='fecha de registro')),
                ('tipo_financiero', models.CharField(blank=True, choices=[('AH', 'Ahorros'), ('PR', 'Préstamos')], max_length=2, null=True)),
                ('saldo_ahorros', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='saldo de ahorros')),
                ('tipo_vendedor', models.CharField(blank=True, choices=[('RV', 'Vendedor Regular'), ('PV', 'Vendedor Premium')], max_length=2, null=True)),
                ('calificacion', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='calificación')),
                ('tipo_usuario_restaurante', models.CharField(blank=True, choices=[('CL', 'Cliente'), ('RS', 'Restaurante')], max_length=2, null=True)),
                ('reservas_activas', models.IntegerField(default=0, verbose_name='reservas activas')),
                ('puntos_recompensa', models.IntegerField(default=0, verbose_name='puntos de recompensa')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
