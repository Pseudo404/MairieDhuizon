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
                ('semaine', models.DateField(
                    help_text='Indiquez le lundi de la semaine concernee (ex : 02/09/2026).',
                    verbose_name='Date du lundi de la semaine',
                )),
                ('jour', models.CharField(
                    choices=[
                        ('lundi', 'Lundi'),
                        ('mardi', 'Mardi'),
                        ('mercredi', 'Mercredi'),
                        ('jeudi', 'Jeudi'),
                        ('vendredi', 'Vendredi'),
                    ],
                    max_length=10,
                    verbose_name='Jour',
                )),
                ('entree', models.CharField(blank=True, max_length=200, verbose_name='Entree')),
                ('plat_principal', models.CharField(max_length=200, verbose_name='Plat principal')),
                ('accompagnement', models.CharField(blank=True, max_length=200, verbose_name='Accompagnement')),
                ('dessert', models.CharField(blank=True, max_length=200, verbose_name='Dessert')),
                ('laitage', models.CharField(blank=True, max_length=200, verbose_name='Laitage')),
                ('note', models.CharField(blank=True, max_length=300, verbose_name='Note')),
            ],
            options={
                'verbose_name': 'Menu de la cantine',
                'verbose_name_plural': 'Menus de la cantine',
                'ordering': ['semaine', 'jour'],
                'unique_together': {('semaine', 'jour')},
            },
        ),
    ]
