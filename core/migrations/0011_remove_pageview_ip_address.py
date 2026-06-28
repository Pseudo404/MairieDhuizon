# Generated migration to remove ip_address from PageView (RGPD compliance)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_nouveaux_modeles_et_corrections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageview',
            name='ip_address',
        ),
    ]
