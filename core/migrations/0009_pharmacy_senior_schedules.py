
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_adminallowedip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacy',
            name='horaires',
            field=models.TextField(
                blank=True,
                help_text='Ex. : garde de nuit, fermetures exceptionnelles… Les horaires pour le statut « ouvert / fermé » se gèrent ci-dessous.',
                verbose_name='Informations complémentaires',
            ),
        ),
        migrations.AlterField(
            model_name='seniorresidence',
            name='horaires',
            field=models.TextField(
                blank=True,
                help_text="Précisions d'accueil. Les horaires pour le statut « ouvert / fermé » se gèrent ci-dessous.",
                verbose_name='Informations complémentaires',
            ),
        ),
        migrations.CreateModel(
            name='PharmacySchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], max_length=10, verbose_name='Jour')),
                ('heure_ouverture', models.TimeField(verbose_name="Heure d'ouverture")),
                ('heure_fermeture', models.TimeField(verbose_name='Heure de fermeture')),
                ('ferme', models.BooleanField(default=False, verbose_name='Fermé ce jour')),
                ('pharmacie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires_planning', to='core.pharmacy', verbose_name='Pharmacie')),
            ],
            options={
                'verbose_name': 'Horaire pharmacie',
                'verbose_name_plural': 'Horaires pharmacie',
                'ordering': ['jour', 'heure_ouverture'],
            },
        ),
        migrations.CreateModel(
            name='SeniorResidenceSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], max_length=10, verbose_name='Jour')),
                ('heure_ouverture', models.TimeField(verbose_name="Heure d'ouverture")),
                ('heure_fermeture', models.TimeField(verbose_name='Heure de fermeture')),
                ('ferme', models.BooleanField(default=False, verbose_name='Fermé ce jour')),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires_planning', to='core.seniorresidence', verbose_name='Résidence')),
            ],
            options={
                'verbose_name': 'Horaire résidence seniors',
                'verbose_name_plural': 'Horaires résidence seniors',
                'ordering': ['jour', 'heure_ouverture'],
            },
        ),
    ]
