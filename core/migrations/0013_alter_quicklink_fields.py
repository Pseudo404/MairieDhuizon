# Generated migration for QuickLink model changes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_make_association_fields_optional'),
    ]

    operations = [
        # Supprimer le champ 'url' et le champ 'icon' existant
        migrations.RemoveField(
            model_name='quicklink',
            name='url',
        ),
        migrations.AlterField(
            model_name='quicklink',
            name='icon',
            field=models.CharField(
                choices=[
                    ('school', '🎓 École'),
                    ('sports_soccer', '⚽ Sports'),
                    ('local_pharmacy', '💊 Pharmacie'),
                    ('home', '🏠 Accueil'),
                    ('info', 'ℹ️ Infos'),
                    ('location_on', '📍 Localisation'),
                    ('phone', '☎️ Téléphone'),
                    ('email', '✉️ Email'),
                    ('people', '👥 Associations'),
                    ('event', '📅 Événements'),
                    ('library_books', '📚 Médiathèque'),
                    ('elderly_woman', '👵 Seniors'),
                    ('child_care', '👶 Crèche'),
                    ('trash', '♻️ Déchets'),
                    ('medical_services', '🏥 Santé'),
                    ('public_transportation', '🚌 Transports'),
                    ('restaurant', '🍽️ Restauration'),
                    ('shopping_cart', '🛒 Commerce'),
                    ('park', '🌳 Loisirs'),
                    ('directions', '🗺️ Carte'),
                ],
                max_length=50,
                verbose_name='Icône',
                help_text='Sélectionnez une icône prédéfinie',
            ),
        ),
        # Ajouter les nouveaux champs
        migrations.AddField(
            model_name='quicklink',
            name='page',
            field=models.CharField(
                choices=[
                    ('accueil', 'Accueil'),
                    ('actualites', 'Actualités'),
                    ('vie-pratique', 'Vie pratique'),
                    ('jeunesse', 'Jeunesse'),
                    ('pharmacie', 'Pharmacie'),
                    ('seniors', 'Résidence seniors'),
                    ('collecte', 'Collecte déchets'),
                    ('decheterie', 'Déchèterie'),
                    ('mairie-mediatheque', 'Mairie & Médiathèque'),
                    ('contact', 'Contact'),
                    ('conseil-municipal', 'Conseil municipal'),
                    ('comptes-rendus', 'Comptes-rendus'),
                    ('elus', 'Les élus'),
                    ('conseil-jeunes', 'Conseil des jeunes'),
                    ('decouvrir', 'Découvrir Dhuizon'),
                    ('histoire', 'Histoire'),
                    ('patrimoine', 'Patrimoine'),
                    ('vie-associative', 'Vie associative'),
                ],
                default='accueil',
                max_length=50,
                verbose_name='Page de destination',
                help_text='Page vers laquelle pointer le lien',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quicklink',
            name='anchor_id',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=100,
                verbose_name='Ancrage (ID de section)',
                help_text='Optionnel - ID de la section pour un lien d\'ancrage (ex: actualite, jeunesse…)',
            ),
        ),
    ]
