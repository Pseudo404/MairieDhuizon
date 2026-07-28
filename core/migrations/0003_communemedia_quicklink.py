
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_news_options_rename_auteur_news_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommuneMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('title', models.CharField(max_length=200, verbose_name='Titre / légende')),
                ('image', models.ImageField(upload_to='commune/gallery/%Y/', verbose_name='Photo')),
                ('description', models.TextField(blank=True, help_text='Optionnel – description détaillée de la photo.', verbose_name='Description')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Photo de la commune',
                'verbose_name_plural': 'Photos de la commune',
                'ordering': ['order', 'title'],
            },
        ),
        migrations.CreateModel(
            name='QuickLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('label', models.CharField(help_text="Texte affiché sous l'icône (ex: École, Sport…)", max_length=100, verbose_name='Libellé')),
                ('icon', models.CharField(help_text="Nom de l'icône Google Material Symbols (ex: school, sports_soccer…)", max_length=100, verbose_name='Icône Material Symbols')),
                ('url', models.CharField(blank=True, help_text='Lien de destination du raccourci (ex: /ecole/ ou https://…)', max_length=255, verbose_name='Lien (URL ou chemin)')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Raccourci infos pratiques',
                'verbose_name_plural': 'Raccourcis infos pratiques',
                'ordering': ['order', 'label'],
            },
        ),
    ]
