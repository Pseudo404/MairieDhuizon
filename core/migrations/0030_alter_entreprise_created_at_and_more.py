
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_quicklink_page_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprise',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
