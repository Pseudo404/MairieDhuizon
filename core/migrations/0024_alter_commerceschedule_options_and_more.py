
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0023_remove_commerceschedule_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commerceschedule',
            options={'ordering': ['commerce', 'jour', 'heure_ouverture'], 'verbose_name': 'Horaire commerce', 'verbose_name_plural': 'Horaires commerce'},
        ),
        migrations.AlterModelOptions(
            name='healthcareprofessional',
            options={'ordering': ['order', 'profession', 'nom', 'prenom'], 'verbose_name': 'Professionnel de santé', 'verbose_name_plural': 'Professionnels de santé'},
        ),
        migrations.AddField(
            model_name='healthcareprofessional',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, help_text='Les professionnels sont triés par ordre croissant, puis par profession et nom.', verbose_name="Ordre d'affichage"),
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('cree', 'Créé'), ('modifie', 'Modifié'), ('supprime', 'Supprimé')], max_length=10, verbose_name='Action')),
                ('section_slug', models.CharField(help_text='Slug de la section concernée (ex : sante-professionnels)', max_length=100, verbose_name='Section du panneau')),
                ('section_label', models.CharField(blank=True, max_length=200, verbose_name='Libellé de la section')),
                ('model_name', models.CharField(help_text='Nom du modèle Django (ex : HealthcareProfessional)', max_length=100, verbose_name='Modèle concerné')),
                ('object_pk', models.CharField(max_length=50, verbose_name="ID de l'objet")),
                ('object_repr', models.CharField(help_text="Valeur __str__ de l'objet au moment de l'action", max_length=500, verbose_name="Représentation de l'objet")),
                ('changes', models.TextField(blank=True, help_text='JSON : champs modifiés avec valeurs avant / après', verbose_name='Détail des modifications')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Date de l'action")),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': "Log d'audit",
                'verbose_name_plural': "Logs d'audit",
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['-created_at'], name='core_auditl_created_1a76fa_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['user'], name='core_auditl_user_id_2ff9b7_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['action'], name='core_auditl_action_d9fb24_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['section_slug'], name='core_auditl_section_5e30ad_idx'),
        ),
    ]
