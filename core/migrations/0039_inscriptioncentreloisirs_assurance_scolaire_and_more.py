
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_inscriptioncentreloisirs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='assurance_scolaire',
            field=models.FileField(blank=True, null=True, upload_to='inscriptions_cl/', verbose_name='Assurance extra-scolaire'),
        ),
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='jugement_familial',
            field=models.FileField(blank=True, null=True, upload_to='inscriptions_cl/', verbose_name='Jugement familial'),
        ),
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='justificatif_quotient_familial',
            field=models.FileField(blank=True, null=True, upload_to='inscriptions_cl/', verbose_name='Justificatif quotient familial'),
        ),
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='livret_famille_doc',
            field=models.FileField(blank=True, null=True, upload_to='inscriptions_cl/', verbose_name='Livret de famille (Document)'),
        ),
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='pai_sante',
            field=models.TextField(blank=True, verbose_name='PAI informations de santé (lunettes, fauteuil, etc.)'),
        ),
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='personnes_habilitees_identite',
            field=models.FileField(blank=True, null=True, upload_to='inscriptions_cl/', verbose_name="Pièce d'identité (Personnes habilitées)"),
        ),
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='personnes_habilitees_texte',
            field=models.TextField(blank=True, verbose_name="Personnes habilitées à venir chercher l'enfant"),
        ),
        migrations.AddField(
            model_name='inscriptioncentreloisirs',
            name='vaccins',
            field=models.FileField(blank=True, null=True, upload_to='inscriptions_cl/', verbose_name='Vaccins'),
        ),
        migrations.AlterField(
            model_name='inscriptioncentreloisirs',
            name='livret_famille',
            field=models.BooleanField(default=False, verbose_name='Livret de famille fourni (Ancien)'),
        ),
    ]
