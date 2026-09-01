
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_communeinfo_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoireDhuizon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('date_label', models.CharField(help_text="Texte affiché comme repère temporel (ex: 1000, XIXe siècle, Aujourd'hui…)", max_length=100, verbose_name='Date / période')),
                ('evenement', models.TextField(help_text="Description de l'événement historique.", verbose_name='Événement')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Les événements sont affichés par ordre croissant.', verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Événement historique',
                'verbose_name_plural': 'Événements historiques',
                'ordering': ['order', 'date_label'],
            },
        ),
    ]
