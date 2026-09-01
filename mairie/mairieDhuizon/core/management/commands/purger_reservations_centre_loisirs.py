from django.core.management.base import BaseCommand

from core.centre_loisirs_admin_views import supprimer_reservations_anciennes


class Command(BaseCommand):
    help = "Supprime les réservations du centre de loisirs datant de plus d'un mois."

    def handle(self, *args, **options):
        deleted = supprimer_reservations_anciennes()
        self.stdout.write(self.style.SUCCESS(f"{deleted} réservation(s) supprimée(s)."))