
from django.db import migrations

def _table_exists(cursor, vendor, table_name):
    if vendor == "sqlite":
        cursor.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=%s",
            [table_name],
        )
    else:
        cursor.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name=%s",
            [table_name],
        )
    return cursor.fetchone() is not None

def fix_commerce_tables(apps, schema_editor):
    connection = schema_editor.connection
    vendor = connection.vendor

    with connection.cursor() as cursor:
        if _table_exists(cursor, vendor, "core_commerce"):
            return

        if not _table_exists(cursor, vendor, "core_entreprise"):
            return

    if vendor == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE core_entreprise RENAME TO core_commerce")
            if _table_exists(cursor, vendor, "core_entrepriseschedule"):
                cursor.execute(
                    "ALTER TABLE core_entrepriseschedule RENAME TO core_commerceschedule"
                )
                cursor.execute(
                    "ALTER TABLE core_commerceschedule "
                    "RENAME COLUMN entreprise_id TO commerce_id"
                )
                cursor.execute(
                    "DROP INDEX IF EXISTS core_entrepriseschedule_entreprise_id_208c662b"
                )
                cursor.execute(
                    "CREATE INDEX core_commerceschedule_commerce_id_idx "
                    "ON core_commerceschedule (commerce_id)"
                )
    else:
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE core_entreprise RENAME TO core_commerce")
            if _table_exists(cursor, vendor, "core_entrepriseschedule"):
                cursor.execute(
                    "ALTER TABLE core_entrepriseschedule RENAME TO core_commerceschedule"
                )
                cursor.execute(
                    "ALTER TABLE core_commerceschedule "
                    "RENAME COLUMN entreprise_id TO commerce_id"
                )

    Entreprise = apps.get_model("core", "Entreprise")
    EntrepriseSchedule = apps.get_model("core", "EntrepriseSchedule")
    schema_editor.create_model(Entreprise)
    schema_editor.create_model(EntrepriseSchedule)

def reverse_fix(apps, schema_editor):
    connection = schema_editor.connection
    vendor = connection.vendor

    with connection.cursor() as cursor:
        if not _table_exists(cursor, vendor, "core_commerce"):
            return
        if _table_exists(cursor, vendor, "core_entreprise"):
            return

    Entreprise = apps.get_model("core", "Entreprise")
    EntrepriseSchedule = apps.get_model("core", "EntrepriseSchedule")
    schema_editor.delete_model(EntrepriseSchedule)
    schema_editor.delete_model(Entreprise)

    if vendor == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE core_commerce RENAME TO core_entreprise")
            if _table_exists(cursor, vendor, "core_commerceschedule"):
                cursor.execute(
                    "ALTER TABLE core_commerceschedule "
                    "RENAME TO core_entrepriseschedule"
                )
                cursor.execute(
                    "ALTER TABLE core_entrepriseschedule "
                    "RENAME COLUMN commerce_id TO entreprise_id"
                )
    else:
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE core_commerce RENAME TO core_entreprise")
            if _table_exists(cursor, vendor, "core_commerceschedule"):
                cursor.execute(
                    "ALTER TABLE core_commerceschedule "
                    "RENAME TO core_entrepriseschedule"
                )
                cursor.execute(
                    "ALTER TABLE core_entrepriseschedule "
                    "RENAME COLUMN commerce_id TO entreprise_id"
                )

class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ("core", "0030_alter_entreprise_created_at_and_more"),
    ]

    operations = [
        migrations.RunPython(fix_commerce_tables, reverse_fix),
    ]
