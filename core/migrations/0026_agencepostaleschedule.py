
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_mediatheque_options_communeinfoschedule_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencePostaleSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], max_length=10, verbose_name='Jour')),
                ('heure_ouverture', models.TimeField(verbose_name="Heure d'ouverture")),
                ('heure_fermeture', models.TimeField(verbose_name='Heure de fermeture')),
                ('ferme', models.BooleanField(default=False, verbose_name='Fermé ce jour')),
                ('agence_postale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires_planning', to='core.agencepostale', verbose_name='Agence postale')),
            ],
            options={
                'verbose_name': 'Horaire agence postale',
                'verbose_name_plural': 'Horaires agence postale',
                'ordering': ['jour', 'heure_ouverture'],
            },
        ),
    ]
