from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_add_can_access_centre_loisirs'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCantine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('annee', models.IntegerField(help_text='Exemple : 2024', verbose_name='Annee')),
                ('numero_semaine', models.IntegerField(help_text='Exemple : 34', verbose_name='Numero de la semaine')),
                ('jour', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi')], max_length=10, verbose_name='Jour')),
                ('entree', models.CharField(blank=True, max_length=200, verbose_name='Entree')),
                ('plat_principal', models.CharField(max_length=200, verbose_name='Plat principal')),
                ('accompagnement', models.CharField(blank=True, max_length=200, verbose_name='Accompagnement')),
                ('dessert', models.CharField(blank=True, max_length=200, verbose_name='Dessert')),
                ('laitage', models.CharField(blank=True, max_length=200, verbose_name='Laitage')),
                ('note', models.CharField(blank=True, max_length=300, verbose_name='Note (allergenes, menu bio...)')),
            ],
            options={
                'verbose_name': 'Menu de la cantine',
                'verbose_name_plural': 'Menus de la cantine',
                'ordering': ['-annee', '-numero_semaine', 'jour'],
                'unique_together': {('annee', 'numero_semaine', 'jour')},
            },
        ),
    ]
