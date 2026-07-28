
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_histoiredhuizon'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('path', models.CharField(max_length=500, verbose_name='Page visitée')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='Adresse IP')),
                ('country', models.CharField(default='France', max_length=100, verbose_name='Pays')),
                ('user_agent', models.TextField(blank=True, verbose_name='User Agent')),
                ('browser', models.CharField(blank=True, max_length=100, verbose_name='Navigateur')),
                ('device_type', models.CharField(default='desktop', help_text='desktop, mobile ou tablet', max_length=20, verbose_name="Type d'appareil")),
                ('referer', models.URLField(blank=True, null=True, verbose_name="Page d'origine")),
                ('session_key', models.CharField(blank=True, max_length=40, verbose_name='Clé de session')),
                ('time_on_page', models.PositiveIntegerField(blank=True, null=True, verbose_name='Temps sur la page (secondes)')),
            ],
            options={
                'verbose_name': 'Vue de page',
                'verbose_name_plural': 'Vues de pages',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['-created_at'], name='core_pagevi_created_4d45f9_idx'), models.Index(fields=['path'], name='core_pagevi_path_582912_idx'), models.Index(fields=['session_key'], name='core_pagevi_session_3251c9_idx')],
            },
        ),
    ]
