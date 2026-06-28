from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0036_alter_commerce_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_super_admin', models.BooleanField(
                    default=False,
                    help_text='Les Super Admins peuvent créer et gérer d\'autres administrateurs.',
                    verbose_name='Est Super Admin (Mairie)',
                )),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='admin_account',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Compte administrateur',
                'verbose_name_plural': 'Comptes administrateurs',
                'ordering': ['user__username'],
            },
        ),
    ]
