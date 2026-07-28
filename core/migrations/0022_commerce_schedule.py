
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_agencepostale'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommerceSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], max_length=10, verbose_name='Jour')),
                ('heure_ouverture', models.TimeField(blank=True, help_text='Laisser vide si fermé toute la journée.', null=True, verbose_name="Heure d'ouverture")),
                ('heure_fermeture', models.TimeField(blank=True, help_text='Laisser vide si fermé toute la journée.', null=True, verbose_name='Heure de fermeture')),
                ('ferme', models.BooleanField(default=False, help_text='Cocher si le commerce est fermé ce jour-là.', verbose_name='Fermé ce jour')),
                ('commerce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires', to='core.commerceprofessionnel', verbose_name='Commerce')),
            ],
            options={
                'verbose_name': 'Horaire commerce',
                'verbose_name_plural': 'Horaires commerce',
                'ordering': ['jour', 'heure_ouverture'],
                'unique_together': {('commerce', 'jour')},
            },
        ),
    ]
