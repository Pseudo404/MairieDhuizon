
from django.db import migrations

def fix_icons(apps, schema_editor):
    """Corriger les anciennes icônes vers les nouvelles valeurs prédéfinies."""
    QuickLink = apps.get_model('core', 'QuickLink')
    
    icon_mapping = {
        'wb_sunny': 'home',  # Météo → Accueil
        'elderly': 'elderly_woman',
        'local_hospital': 'medical_services',
        'delete': 'trash',
        'account_balance': 'people',
    }
    
    for old_icon, new_icon in icon_mapping.items():
        QuickLink.objects.filter(icon=old_icon).update(icon=new_icon)

def reverse_fix(apps, schema_editor):
    """Annuler les changements (pas nécessaire, juste pour la cohérence)."""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_quicklink_fields'),
    ]

    operations = [
        migrations.RunPython(fix_icons, reverse_fix),
    ]
