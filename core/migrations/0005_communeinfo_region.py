
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_communemedia_is_hero_alter_association_logo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='communeinfo',
            name='region',
            field=models.CharField(default='Centre-Val de Loire', max_length=100, verbose_name='Région'),
        ),
    ]
