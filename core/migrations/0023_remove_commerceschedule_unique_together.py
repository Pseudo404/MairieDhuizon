from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_commerce_schedule'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commerceschedule',
            unique_together=set(),
        ),
    ]
