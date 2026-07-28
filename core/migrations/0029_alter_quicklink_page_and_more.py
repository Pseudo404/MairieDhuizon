
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_demarcheadministrative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quicklink',
            name='page',
            field=models.CharField(choices=[('accueil', 'Accueil'), ('vie-pratique', 'Vie pratique'), ('tourisme', 'Tourisme'), ('entreprises', 'Entreprises'), ('decouvrir', 'Découvrir Dhuizon'), ('conseil-municipal', 'Conseil municipal'), ('vie-associative', 'Vie associative'), ('contact', 'Contact')], help_text='Page vers laquelle pointer le lien', max_length=50, verbose_name='Page de destination'),
        ),
        migrations.RenameModel(
            old_name='CommerceProfessionnel',
            new_name='Commerce',
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom_activite', models.CharField(max_length=255, verbose_name="Nom de l'activité")),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('personnel', models.CharField(blank=True, help_text='Nom(s) du ou des responsables / gérants.', max_length=255, verbose_name='Personnel / Responsable')),
                ('telephone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Entreprise',
                'verbose_name_plural': 'Entreprises',
                'ordering': ['order', 'nom_activite'],
            },
        ),
        migrations.CreateModel(
            name='EntrepriseSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('jour_index', models.PositiveSmallIntegerField(default=1, editable=False)),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], max_length=10, verbose_name='Jour')),
                ('heure_ouverture', models.TimeField(blank=True, help_text='Laisser vide si fermé toute la journée.', null=True, verbose_name="Heure d'ouverture")),
                ('heure_fermeture', models.TimeField(blank=True, help_text='Laisser vide si fermé toute la journée.', null=True, verbose_name='Heure de fermeture')),
                ('ferme', models.BooleanField(default=False, help_text="Cocher si l'entreprise est fermée ce jour-là.", verbose_name='Fermé ce jour')),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires', to='core.entreprise', verbose_name='Entreprise')),
            ],
            options={
                'verbose_name': 'Horaire entreprise',
                'verbose_name_plural': 'Horaires entreprise',
                'ordering': ['entreprise', 'jour_index', 'heure_ouverture'],
            },
        ),
    ]
