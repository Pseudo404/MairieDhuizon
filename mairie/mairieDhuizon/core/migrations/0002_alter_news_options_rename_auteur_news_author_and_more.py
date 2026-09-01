
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['event_date'], 'verbose_name': 'Actualité', 'verbose_name_plural': 'Actualités'},
        ),
        migrations.RenameField(
            model_name='news',
            old_name='auteur',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='contenu',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='description_courte',
            new_name='short_description',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='titre',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='news',
            name='date_publication',
        ),
        migrations.AddField(
            model_name='news',
            name='event_date',
            field=models.DateField(default=datetime.date(2026, 1, 1), help_text="Date à laquelle l'événement se déroule.", verbose_name="Date de l'événement"),
            preserve_default=False,
        ),
    ]
