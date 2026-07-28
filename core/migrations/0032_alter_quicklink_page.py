
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_fix_commerce_entreprise_tables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quicklink',
            name='page',
            field=models.CharField(choices=[('accueil', 'Accueil'), ('vie-pratique', 'Vie pratique'), ('tourisme', 'Tourisme'), ('entreprises', 'Entreprises'), ('commerces', 'Commerces & Professionnels'), ('decouvrir', 'Découvrir Dhuizon'), ('conseil-municipal', 'Conseil municipal'), ('vie-associative', 'Vie associative'), ('contact', 'Contact')], help_text='Page vers laquelle pointer le lien', max_length=50, verbose_name='Page de destination'),
        ),
    ]
