
import core.validators
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_alter_quicklink_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom du gîte')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('telephone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('site_web', models.URLField(blank=True, validators=[core.validators.validate_safe_link_url], verbose_name='Site web')),
                ('capacite', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Capacité (personnes)')),
                ('tarif', models.CharField(blank=True, help_text='Ex : À partir de 80 € / nuit', max_length=100, verbose_name='Tarif indicatif')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/tourisme/gites/', validators=[core.validators.validate_image_upload], verbose_name='Photo')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Gîte',
                'verbose_name_plural': 'Gîtes',
                'ordering': ['order', 'nom'],
            },
        ),
    ]
