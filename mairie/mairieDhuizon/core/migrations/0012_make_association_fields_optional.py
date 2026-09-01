
from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_pageview_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='email',
            field=models.EmailField(
                blank=True,
                max_length=254,
                validators=[django.core.validators.EmailValidator()],
                verbose_name='Email'
            ),
        ),
        migrations.AlterField(
            model_name='association',
            name='telephone',
            field=models.CharField(
                blank=True,
                max_length=20,
                verbose_name='Téléphone'
            ),
        ),
    ]
