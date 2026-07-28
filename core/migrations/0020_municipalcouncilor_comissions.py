
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_add_slug_association'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipalcouncilor',
            name='comissions',
            field=models.CharField(blank=True, help_text='Ex: Urbanisme, Environnement, Culture…', max_length=255, verbose_name='Commissions'),
        ),
    ]
