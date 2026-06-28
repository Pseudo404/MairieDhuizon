# Generated manually for AdminAllowedIP

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_pageview'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAllowedIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('label', models.CharField(help_text='Ex. : Mairie de Dhuizon, Bureau du maire…', max_length=120, verbose_name='Libellé')),
                ('ip_address', models.GenericIPAddressField(help_text='IPv4 ou IPv6 publique de la mairie (ex. 203.0.113.42).', verbose_name='Adresse IP')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('notes', models.CharField(blank=True, max_length=255, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'IP autorisée (/admin/)',
                'verbose_name_plural': 'IP autorisées (/admin/)',
                'ordering': ['label', 'ip_address'],
            },
        ),
    ]
