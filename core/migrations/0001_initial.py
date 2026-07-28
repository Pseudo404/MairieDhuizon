
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name="Nom de l'association")),
                ('description', models.TextField(verbose_name='Description')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('site_web', models.URLField(blank=True, verbose_name='Site web')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='associations/logos/', verbose_name='Logo')),
            ],
            options={
                'verbose_name': 'Association',
                'verbose_name_plural': 'Associations',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='CommuneInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('presentation', models.TextField(verbose_name='Texte de présentation de la commune')),
                ('population', models.PositiveIntegerField(verbose_name="Nombre d'habitants")),
                ('superficie_ha', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Superficie (hectares)')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse de la mairie')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email de la mairie')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone de la mairie')),
                ('horaires', models.TextField(help_text='Exemple : Lundi-Vendredi 9h-12h / 14h-17h', verbose_name="Horaires d'ouverture")),
            ],
            options={
                'verbose_name': 'Information commune',
                'verbose_name_plural': 'Informations commune',
            },
        ),
        migrations.CreateModel(
            name='HealthCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Maison de santé',
                'verbose_name_plural': 'Maisons de santé',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='MunicipalCouncilReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('titre', models.CharField(max_length=255, verbose_name='Titre')),
                ('date', models.DateField(verbose_name='Date du conseil')),
                ('pdf', models.FileField(upload_to='council/reports/%Y/', verbose_name='Fichier PDF')),
                ('description', models.TextField(blank=True, help_text='Optionnel – résumé du conseil.', verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Compte rendu de conseil municipal',
                'verbose_name_plural': 'Comptes rendus de conseils municipaux',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('titre', models.CharField(max_length=255, verbose_name='Titre')),
                ('slug', models.SlugField(help_text='Généré automatiquement depuis le titre.', max_length=270, unique=True, verbose_name='Slug (URL)')),
                ('description_courte', models.TextField(help_text='Résumé affiché sur la liste des actualités.', max_length=500, verbose_name='Description courte')),
                ('contenu', models.TextField(verbose_name='Contenu complet')),
                ('image', models.ImageField(blank=True, null=True, upload_to='news/images/%Y/%m/', verbose_name='Image principale')),
                ('date_publication', models.DateField(verbose_name='Date de publication')),
                ('auteur', models.CharField(blank=True, help_text="Optionnel – nom de l'auteur de l'article.", max_length=150, verbose_name='Auteur')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publié')),
            ],
            options={
                'verbose_name': 'Actualité',
                'verbose_name_plural': 'Actualités',
                'ordering': ['-date_publication'],
            },
        ),
        migrations.CreateModel(
            name='Nursery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('horaires', models.TextField(verbose_name="Horaires d'accueil")),
            ],
            options={
                'verbose_name': 'Crèche',
                'verbose_name_plural': 'Crèches',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('horaires', models.TextField(verbose_name="Horaires d'ouverture")),
            ],
            options={
                'verbose_name': 'Pharmacie',
                'verbose_name_plural': 'Pharmacies',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='RecyclingCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Déchetterie',
                'verbose_name_plural': 'Déchetteries',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name="Nom de l'école")),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse postale')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('nom_directrice', models.CharField(max_length=150, verbose_name='Nom de la directrice / directeur')),
                ('nb_eleves', models.PositiveIntegerField(verbose_name="Nombre d'élèves")),
                ('nb_inscrits_rentree', models.PositiveIntegerField(verbose_name='Inscrits à la dernière rentrée')),
                ('horaires_cours', models.TextField(help_text='Exemple : Lun/Mar/Jeu/Ven 8h30-11h30 / 13h30-16h30', verbose_name='Horaires des cours')),
            ],
            options={
                'verbose_name': 'École',
                'verbose_name_plural': 'Écoles',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='SeniorResidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('horaires', models.TextField(blank=True, help_text='Optionnel.', verbose_name="Horaires d'accueil")),
            ],
            options={
                'verbose_name': 'Résidence senior',
                'verbose_name_plural': 'Résidences seniors',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='SportFacilityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=150, unique=True, verbose_name="Type d'équipement")),
                ('icone', models.CharField(blank=True, help_text="Optionnel – ex: 'fas fa-futbol' ou '⚽'", max_length=50, verbose_name='Icône (classe CSS ou emoji)')),
            ],
            options={
                'verbose_name': "Type d'équipement sportif",
                'verbose_name_plural': "Types d'équipements sportifs",
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='HealthcareProfessional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('prenom', models.CharField(max_length=100, verbose_name='Prénom')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('profession', models.CharField(help_text='Exemple : Médecin généraliste, Kinésithérapeute…', max_length=150, verbose_name='Profession')),
                ('telephone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professionnels', to='core.healthcenter', verbose_name='Maison de santé')),
            ],
            options={
                'verbose_name': 'Professionnel de santé',
                'verbose_name_plural': 'Professionnels de santé',
                'ordering': ['centre', 'nom', 'prenom'],
            },
        ),
        migrations.CreateModel(
            name='SportFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name="Nom de l'équipement")),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse / lieu')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude GPS')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude GPS')),
                ('image', models.ImageField(blank=True, null=True, upload_to='sports/images/', verbose_name='Image')),
                ('type_equipement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipements', to='core.sportfacilitytype', verbose_name="Type d'équipement")),
            ],
            options={
                'verbose_name': 'Équipement sportif',
                'verbose_name_plural': 'Équipements sportifs',
                'ordering': ['type_equipement', 'nom'],
            },
        ),
        migrations.CreateModel(
            name='WasteCollectionSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('type_dechet', models.CharField(choices=[('menagers', 'Déchets ménagers'), ('recyclables', 'Recyclables (tri sélectif)'), ('verre', 'Verre'), ('encombrants', 'Encombrants'), ('vegetaux', 'Déchets verts / végétaux'), ('autre', 'Autre')], max_length=20, verbose_name='Type de déchet')),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi')], max_length=10, verbose_name='Jour de collecte')),
                ('heure', models.TimeField(blank=True, help_text='Optionnel.', null=True, verbose_name='Heure de collecte')),
                ('description', models.TextField(blank=True, verbose_name='Description / précisions')),
            ],
            options={
                'verbose_name': 'Planning de collecte des déchets',
                'verbose_name_plural': 'Plannings de collecte des déchets',
                'ordering': ['jour', 'type_dechet'],
                'unique_together': {('type_dechet', 'jour')},
            },
        ),
        migrations.CreateModel(
            name='RecyclingCenterSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('saison', models.CharField(choices=[('ete', 'Été (01/04 → 31/10)'), ('hiver', 'Hiver (01/11 → 31/03)')], max_length=10, verbose_name='Saison')),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], max_length=10, verbose_name='Jour')),
                ('heure_ouverture', models.TimeField(verbose_name="Heure d'ouverture")),
                ('heure_fermeture', models.TimeField(verbose_name='Heure de fermeture')),
                ('ferme', models.BooleanField(default=False, help_text='Cocher si la déchetterie est fermée ce jour-là pour cette saison.', verbose_name='Fermé ce jour')),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires', to='core.recyclingcenter', verbose_name='Déchetterie')),
            ],
            options={
                'verbose_name': 'Horaire de déchetterie',
                'verbose_name_plural': 'Horaires de déchetterie',
                'ordering': ['centre', 'saison', 'jour'],
                'unique_together': {('centre', 'saison', 'jour')},
            },
        ),
    ]
