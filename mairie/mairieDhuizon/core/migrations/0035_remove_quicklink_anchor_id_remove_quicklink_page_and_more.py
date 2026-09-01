
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_randonnee_alter_gite_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quicklink',
            name='anchor_id',
        ),
        migrations.RemoveField(
            model_name='quicklink',
            name='page',
        ),
        migrations.AddField(
            model_name='quicklink',
            name='url',
            field=models.CharField(default='/', help_text='URL locale ou externe vers laquelle pointer le lien', max_length=255, verbose_name='Lien (ex: /loisirs/#sport)'),
        ),
    ]
