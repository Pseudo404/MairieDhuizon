
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_communemedia_quicklink'),
    ]

    operations = [
        migrations.AddField(
            model_name='communemedia',
            name='is_hero',
            field=models.BooleanField(default=False, help_text='Cocher pour utiliser cette photo comme fond de la section principale.', verbose_name='Image héro (fond accueil)'),
        ),
        migrations.AlterField(
            model_name='association',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/associations/', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='communemedia',
            name='image',
            field=models.ImageField(upload_to='images/galerie/', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='municipalcouncilreport',
            name='pdf',
            field=models.FileField(upload_to='documents/conseils/', verbose_name='Fichier PDF'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/actualites/', verbose_name='Image principale'),
        ),
        migrations.AlterField(
            model_name='sportfacility',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/sports/', verbose_name='Image'),
        ),
    ]
