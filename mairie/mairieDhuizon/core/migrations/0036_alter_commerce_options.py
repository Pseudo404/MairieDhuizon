
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_remove_quicklink_anchor_id_remove_quicklink_page_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commerce',
            options={'ordering': ['order', 'nom_activite'], 'verbose_name': 'Commerce', 'verbose_name_plural': 'Commerces'},
        ),
    ]
