
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_add_gite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Randonnee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nom', models.CharField(max_length=255, verbose_name='Nom de la randonnée')),
                ('slug', models.SlugField(blank=True, help_text='Généré automatiquement si laissé vide.', max_length=255, unique=True, verbose_name='Slug (URL)')),
                ('description_courte', models.CharField(help_text='Affichée sur la carte dans la liste des loisirs.', max_length=500, verbose_name='Description courte')),
                ('description_detaillee', models.TextField(help_text='Affichée sur la page dédiée à la randonnée.', verbose_name='Description détaillée')),
                ('temps_parcours', models.CharField(help_text='Ex: 2h30', max_length=100, verbose_name='Temps de parcours estimé')),
                ('niveau_difficulte', models.CharField(choices=[('facile', 'Facile'), ('moyen', 'Moyen'), ('difficile', 'Difficile')], default='facile', max_length=20, verbose_name='Niveau de difficulté')),
                ('distance_km', models.DecimalField(decimal_places=1, help_text='Ex: 12.5', max_digits=5, verbose_name='Distance (km)')),
                ('adresse_depart', models.CharField(blank=True, help_text='Adresse ou point de repère.', max_length=255, null=True, verbose_name='Lieu de départ')),
                ('image_principale', models.ImageField(blank=True, null=True, upload_to='images/randonnees/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'], message='Format image non autorisé. Utilisez : JPG, PNG, WEBP ou GIF.')], verbose_name='Image de présentation')),
                ('carte_image', models.ImageField(blank=True, null=True, upload_to='images/randonnees/cartes/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'], message='Format image non autorisé. Utilisez : JPG, PNG, WEBP ou GIF.')], verbose_name='Image de la carte du tracé')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Randonnée',
                'verbose_name_plural': 'Randonnées',
                'ordering': ['order', 'nom'],
            },
        ),
        migrations.AlterField(
            model_name='gite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='gite',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='quicklink',
            name='page',
            field=models.CharField(choices=[('accueil', 'Accueil'), ('vie-pratique', 'Vie pratique'), ('loisirs', 'Loisirs'), ('tourisme', 'Tourisme'), ('entreprises', 'Entreprises'), ('decouvrir', 'Découvrir Dhuizon'), ('conseil-municipal', 'Conseil municipal'), ('vie-associative', 'Vie associative'), ('contact', 'Contact')], help_text='Page vers laquelle pointer le lien', max_length=50, verbose_name='Page de destination'),
        ),
    ]
