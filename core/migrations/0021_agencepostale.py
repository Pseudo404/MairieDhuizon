
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_municipalcouncilor_comissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencePostale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(default='Agence Postale de Dhuizon', max_length=255, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('telephone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone')),
                ('horaires', models.TextField(blank=True, help_text='Exemple : Lun/Mar/Jeu/Ven 9h-12h', verbose_name="Horaires d'ouverture")),
            ],
            options={
                'verbose_name': 'Agence postale',
                'verbose_name_plural': 'Agences postales',
            },
        ),
    ]
