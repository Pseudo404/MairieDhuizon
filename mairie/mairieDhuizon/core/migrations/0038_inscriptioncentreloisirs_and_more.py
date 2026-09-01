
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_adminaccount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InscriptionCentreLoisirs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nom_enfant', models.CharField(max_length=100, verbose_name="Nom de l'enfant")),
                ('prenom_enfant', models.CharField(max_length=100, verbose_name="Prénom de l'enfant")),
                ('date_naissance', models.DateField(verbose_name='Date de naissance')),
                ('nom_responsable_1', models.CharField(max_length=100, verbose_name='Nom (Responsable 1)')),
                ('prenom_responsable_1', models.CharField(max_length=100, verbose_name='Prénom (Responsable 1)')),
                ('adresse_responsable_1', models.CharField(max_length=255, verbose_name='Adresse (Responsable 1)')),
                ('code_postal_1', models.CharField(max_length=20, verbose_name='Code postal (Responsable 1)')),
                ('ville_1', models.CharField(max_length=100, verbose_name='Ville (Responsable 1)')),
                ('telephone_1', models.CharField(blank=True, max_length=20, verbose_name='Téléphone (Responsable 1)')),
                ('portable_1', models.CharField(max_length=20, verbose_name='Portable (Responsable 1)')),
                ('email_1', models.EmailField(max_length=254, verbose_name='Email (Responsable 1)')),
                ('nom_responsable_2', models.CharField(blank=True, max_length=100, verbose_name='Nom (Responsable 2)')),
                ('prenom_responsable_2', models.CharField(blank=True, max_length=100, verbose_name='Prénom (Responsable 2)')),
                ('adresse_responsable_2', models.CharField(blank=True, max_length=255, verbose_name='Adresse (Responsable 2)')),
                ('code_postal_2', models.CharField(blank=True, max_length=20, verbose_name='Code postal (Responsable 2)')),
                ('ville_2', models.CharField(blank=True, max_length=100, verbose_name='Ville (Responsable 2)')),
                ('telephone_2', models.CharField(blank=True, max_length=20, verbose_name='Téléphone (Responsable 2)')),
                ('portable_2', models.CharField(blank=True, max_length=20, verbose_name='Portable (Responsable 2)')),
                ('email_2', models.EmailField(blank=True, max_length=254, verbose_name='Email (Responsable 2)')),
                ('coefficient_familial', models.CharField(blank=True, max_length=50, verbose_name='Coefficient familial')),
                ('livret_famille', models.BooleanField(default=False, verbose_name='Livret de famille fourni')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Inscription au centre de loisirs',
                'verbose_name_plural': 'Inscriptions au centre de loisirs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='adminaccount',
            name='is_centre_loisirs',
            field=models.BooleanField(default=False, help_text='Accès restreint au panneau de gestion du centre de loisirs.', verbose_name='Est Admin Centre de Loisirs'),
        ),
        migrations.AddField(
            model_name='leisurecenter',
            name='capacite_max',
            field=models.PositiveIntegerField(default=30, help_text="Nombre maximum d'enfants pouvant être accueillis par jour.", verbose_name='Capacité journalière maximale'),
        ),
        migrations.CreateModel(
            name='LeisureDayStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('status', models.CharField(choices=[('ouvert', 'Ouvert'), ('ferme', 'Fermé'), ('ferie', 'Férié')], default='ouvert', max_length=20, verbose_name='Statut')),
                ('motif_fermeture', models.CharField(blank=True, max_length=255, verbose_name='Motif de fermeture (optionnel)')),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jours_statuts', to='core.leisurecenter')),
            ],
            options={
                'verbose_name': 'Statut journalier du centre de loisirs',
                'verbose_name_plural': 'Statuts journaliers du centre de loisirs',
                'ordering': ['-date'],
                'unique_together': {('centre', 'date')},
            },
        ),
        migrations.CreateModel(
            name='ReservationCentreLoisirs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(verbose_name='Date réservée')),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('validee', 'Validée'), ('refusee', 'Refusée'), ('annulee', 'Annulée')], default='en_attente', max_length=20, verbose_name='Statut')),
                ('token_annulation', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date_validation', models.DateTimeField(blank=True, null=True, verbose_name='Date de validation/refus')),
                ('motif_refus', models.CharField(blank=True, max_length=255, verbose_name='Motif de refus')),
                ('inscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='core.inscriptioncentreloisirs')),
                ('validee_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations_validees', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Réservation centre de loisirs',
                'verbose_name_plural': 'Réservations centre de loisirs',
                'ordering': ['-date'],
                'unique_together': {('inscription', 'date')},
            },
        ),
    ]
